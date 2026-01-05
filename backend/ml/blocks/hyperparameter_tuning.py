"""
Butterfly ML Block - Hyperparameter Tuning

Optuna-based hyperparameter optimization.
Sixth block in canonical pipeline.
"""
from backend.domain import ExecutionContext


def hyperparameter_tuning_block(context: ExecutionContext):
    """
    Hyperparameter tuning using Optuna.
    
    Responsibilities:
    - Define search spaces per model
    - Run optimization trials
    - Select best hyperparameters
    
    Note: Basic implementation for v1.
    For now, we use default hyperparameters.
    Full Optuna integration can be added later.
    """
    context.log("Starting hyperparameter tuning...")
    
    # For v1, skip tuning and use default hyperparameters
    # This keeps the implementation simple while maintaining the pipeline structure
    context.log("Using default hyperparameters (tuning can be enabled via hooks)")
    
    context.log("Hyperparameter tuning completed")
