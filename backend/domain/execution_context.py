"""
Butterfly Domain Model - Execution Context

Represents the shared state passed through pipeline execution.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import pandas as pd


@dataclass
class ExecutionContext:
    """
    Shared state passed through pipeline execution.
    
    Responsibilities:
    - Carry data, models, and metadata between stages
    - Enforce determinism
    - Provide controlled access to state
    
    Key Properties from 06_domain_model.md:
    - Dataset reference
    - Intermediate data
    - Feature representations
    - Model objects
    - Metrics
    - Logs
    
    Lifecycle:
    - Created per run
    - Passed block-to-block
    - Destroyed after run completion
    
    Invariants:
    - Context isolation between runs
    - No state leakage across executions
    """
    # Run identification
    run_id: str = ""
    seed: int = 42
    
    # Data
    dataset_path: str = ""
    raw_data: Optional[pd.DataFrame] = None
    processed_data: Optional[pd.DataFrame] = None
    train_data: Optional[pd.DataFrame] = None
    test_data: Optional[pd.DataFrame] = None
    
    # Features
    feature_names: List[str] = field(default_factory=list)
    target_column: Optional[str] = None
    
    # Task information
    task_type: str = "auto_detect"  # classification, regression, etc.
    detected_task: Optional[str] = None
    
    # Models
    candidate_models: List[Any] = field(default_factory=list)
    trained_models: List[Any] = field(default_factory=list)
    best_model: Optional[Any] = None
    
    # Metrics
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Explainability
    feature_importance: Dict[str, float] = field(default_factory=dict)
    shap_values: Optional[Any] = None
    
    # Logs and metadata
    logs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Block execution tracking
    completed_blocks: List[str] = field(default_factory=list)
    current_block: Optional[str] = None
    
    def log(self, message: str):
        """Add log message"""
        self.logs.append(message)
    
    def mark_block_complete(self, block_id: str):
        """Mark a block as completed"""
        if block_id not in self.completed_blocks:
            self.completed_blocks.append(block_id)
        self.current_block = None
    
    def set_current_block(self, block_id: str):
        """Set currently executing block"""
        self.current_block = block_id
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of context state (for serialization)"""
        return {
            "run_id": self.run_id,
            "seed": self.seed,
            "task_type": self.task_type,
            "detected_task": self.detected_task,
            "feature_names": self.feature_names,
            "target_column": self.target_column,
            "num_candidate_models": len(self.candidate_models),
            "num_trained_models": len(self.trained_models),
            "has_best_model": self.best_model is not None,
            "metrics": self.metrics,
            "completed_blocks": self.completed_blocks,
            "current_block": self.current_block,
            "num_logs": len(self.logs)
        }
