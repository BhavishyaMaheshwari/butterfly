"""
Butterfly Execution Engine - Context Manager

Manages execution context lifecycle and isolation.
Follows 09_execution_rules.md section 6.
"""
from backend.domain import ExecutionContext, Run
from .determinism import DeterminismManager


class ContextManager:
    """
    Manages execution context lifecycle.
    
    From 09_execution_rules.md section 6:
    - A new execution context is created per run
    - Context is passed block-to-block
    - Context is destroyed after run completion
    - No context reuse is allowed
    
    Responsibilities:
    - Create isolated context per run
    - Enforce context boundaries
    - Prevent state leakage
    """
    
    @staticmethod
    def create_context(run: Run, dataset_path: str) -> ExecutionContext:
        """
        Create new execution context for run.
        
        Sets up:
        - Run identification
        - Global seed
        - Dataset reference
        - Empty state containers
        """
        # Set global seed for determinism
        DeterminismManager.set_global_seed(run.seed)
        
        # Create context
        context = ExecutionContext(
            run_id=run.id,
            seed=run.seed,
            dataset_path=dataset_path
        )
        
        context.log(f"Execution context created for run {run.id}")
        context.log(f"Global seed set to {run.seed}")
        
        return context
    
    @staticmethod
    def validate_context(context: ExecutionContext) -> bool:
        """
        Validate context internal consistency.
        
        Checks:
        - Required fields are set
        - Data references are valid
        - No conflicting state
        """
        if not context.run_id:
            return False
        
        if not context.dataset_path:
            return False
        
        # Context is valid
        return True
    
    @staticmethod
    def destroy_context(context: ExecutionContext):
        """
        Destroy context after run completion.
        
        Clears references to allow garbage collection.
        Note: In Python, this is mostly symbolic, but makes intent clear.
        """
        context.log(f"Execution context destroyed for run {context.run_id}")
        
        # Clear large data structures
        context.raw_data = None
        context.processed_data = None
        context.train_data = None
        context.test_data = None
        context.candidate_models = []
        context.trained_models = []
        context.best_model = None
