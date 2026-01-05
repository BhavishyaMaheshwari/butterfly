"""
Butterfly Execution Engine - Main Executor

Orchestrates run creation and pipeline execution.
Follows 09_execution_rules.md strictly.

=============================================================================
ARCHITECTURE: EXECUTION LAYER
=============================================================================

This file contains ONLY execution orchestration logic.
NO HTTP/API knowledge should exist here.

Responsibilities:
- Create immutable Runs from Experiments
- Freeze pipeline state (snapshot)
- Execute blocks in canonical order
- Manage execution context lifecycle
- Save artifacts and metrics
- Handle execution failures

Rules:
- NEVER handle HTTP requests/responses
- NEVER know about FastAPI/WebSockets
- Pure Python business logic only
- Delegate to block_executor for block execution
- Delegate to stores for persistence

Layer Separation:
API (server.py) → Execution (this file) → Block Executor → ML Blocks
                                        → Storage (stores)

=============================================================================
"""
from typing import Callable, Dict, Optional
from pathlib import Path
import traceback

from backend.domain import (
    Run, RunStatus, Experiment, Dataset, BlockType,
    ExecutionContext, Artifact, ArtifactType
)
from backend.storage import (
    DatasetStore, ExperimentStore, RunStore, ArtifactStore
)
from .context_manager import ContextManager
from .block_executor import BlockExecutor


class Executor:
    """
    Main execution orchestrator.
    
    From 09_execution_rules.md:
    - All execution happens via immutable Runs
    - Pipeline is snapshotted before execution
    - Blocks execute sequentially in canonical order
    - Failures are contained per run
    - No implicit execution
    
    Responsibilities:
    - Create and manage runs
    - Freeze execution state
    - Execute pipeline stages in order
    - Emit execution events
    - Handle failures gracefully
    
    Guarantees:
    - Deterministic execution
    - Clear run state transitions
    - No partial mutation of completed runs
    """
    
    def __init__(
        self,
        dataset_store: DatasetStore,
        experiment_store: ExperimentStore,
        run_store: RunStore,
        artifact_store: ArtifactStore
    ):
        self.dataset_store = dataset_store
        self.experiment_store = experiment_store
        self.run_store = run_store
        self.artifact_store = artifact_store
        self.block_executor = BlockExecutor(experiment_store)
        
        # System block implementations (will be set by ML engine)
        self.block_implementations: Dict[BlockType, Callable] = {}
    
    def register_block_implementation(
        self,
        block_type: BlockType,
        implementation: Callable[[ExecutionContext], None]
    ):
        """Register system implementation for a block type"""
        self.block_implementations[block_type] = implementation
    
    def create_run(
        self,
        experiment: Experiment,
        dataset: Dataset,
        seed: Optional[int] = None
    ) -> Run:
        """
        Create a new run.
        
        From 09_execution_rules.md section 3:
        At run creation time:
        - The pipeline is snapshotted
        - All block configurations are frozen
        - All user-injected code is hashed
        - A global seed is fixed
        - Dataset version is locked
        
        Once created, a run is immutable.
        """
        # Snapshot the pipeline (creates immutable copy)
        pipeline_snapshot = experiment.pipeline.snapshot()
        
        # Create run with frozen state
        run = Run(
            experiment_id=experiment.id,
            pipeline_snapshot=pipeline_snapshot,
            dataset_hash=dataset.content_hash,
            seed=seed if seed is not None else 42,
            status=RunStatus.CREATED
        )
        
        # Persist run
        self.run_store.create(run)
        
        return run
    
    def execute_run(self, run: Run) -> bool:
        """
        Execute a run.
        
        From 09_execution_rules.md section 4:
        - Blocks execute sequentially in canonical order
        - No implicit parallel execution
        - Failures stop execution immediately
        
        Returns:
            True if successful, False if failed
        """
        # Validate run can be executed
        if run.status != RunStatus.CREATED:
            raise ValueError(f"Cannot execute run in status {run.status}")
        
        # Start run
        run.start()
        self.run_store.save(run)
        self.run_store.append_log(run.id, f"Run {run.id} started")
        
        # Load dataset
        dataset = self.dataset_store.load(
            self._get_dataset_id_from_experiment(run.experiment_id)
        )
        if not dataset:
            run.fail("Dataset not found")
            self.run_store.save(run)
            return False
        
        # Create execution context
        context = ContextManager.create_context(run, str(dataset.source_path))
        
        # Save initial logs
        for log in context.logs:
            self.run_store.append_log(run.id, log)
        
        try:
            # Execute blocks in canonical order
            # From 09_execution_rules.md section 4.1
            for block in sorted(run.pipeline_snapshot.blocks, key=lambda b: b.position):
                # Get system implementation
                system_impl = self.block_implementations.get(block.type)
                if not system_impl:
                    # Use no-op if not implemented
                    system_impl = lambda ctx: None
                
                # Execute block with hook precedence
                success, error_msg = self.block_executor.execute_block(
                    block=block,
                    context=context,
                    system_logic=system_impl,
                    experiment_id=run.experiment_id
                )
                
                # Save logs after each block
                for log in context.logs:
                    self.run_store.append_log(run.id, log)
                context.logs = []  # Clear logs
                
                # Handle failure
                if not success:
                    run.fail(error_msg or "Unknown error", block.id)
                    self.run_store.save(run)
                    self.run_store.append_log(run.id, f"Run failed at block {block.type.value}")
                    return False
            
            # All blocks completed successfully
            run.complete()
            self.run_store.save(run)
            self.run_store.append_log(run.id, f"Run {run.id} completed successfully")
            
            # Save artifacts
            self._save_run_artifacts(run, context)
            
            # Destroy context
            ContextManager.destroy_context(context)
            
            return True
        
        except Exception as e:
            error_msg = f"Run execution failed: {str(e)}\n{traceback.format_exc()}"
            run.fail(error_msg)
            self.run_store.save(run)
            self.run_store.append_log(run.id, error_msg)
            return False
    
    def _get_dataset_id_from_experiment(self, experiment_id: str) -> str:
        """Get dataset ID from experiment"""
        experiment = self.experiment_store.load(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
        return experiment.dataset_id
    
    def _save_run_artifacts(self, run: Run, context: ExecutionContext):
        """Save artifacts from execution context"""
        artifacts_dir = self.run_store.get_artifacts_dir(run.id)
        
        # Save metrics as artifact
        if context.metrics:
            import json
            metrics_file = artifacts_dir / "metrics.json"
            with open(metrics_file, 'w') as f:
                json.dump(context.metrics, f, indent=2)
            
            artifact = Artifact(
                type=ArtifactType.METRICS,
                run_id=run.id,
                file_path=metrics_file,
                metadata={"metrics": context.metrics}
            )
            self.artifact_store.save(artifact)
        
        # Save feature importance
        if context.feature_importance:
            import json
            fi_file = artifacts_dir / "feature_importance.json"
            with open(fi_file, 'w') as f:
                json.dump(context.feature_importance, f, indent=2)
            
            artifact = Artifact(
                type=ArtifactType.EXPLAINABILITY,
                run_id=run.id,
                file_path=fi_file,
                metadata={"type": "feature_importance"}
            )
            self.artifact_store.save(artifact)
        
        # Save model if present
        if context.best_model:
            try:
                import joblib
                model_file = artifacts_dir / "model.pkl"
                joblib.dump(context.best_model, model_file)
                
                artifact = Artifact(
                    type=ArtifactType.MODEL,
                    run_id=run.id,
                    file_path=model_file,
                    metadata={"model_type": type(context.best_model).__name__}
                )
                self.artifact_store.save(artifact)
            except Exception as e:
                # Log but don't fail if model save fails
                self.run_store.append_log(run.id, f"Warning: Could not save model: {str(e)}")
