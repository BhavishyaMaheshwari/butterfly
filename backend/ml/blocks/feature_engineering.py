"""
Butterfly ML Block - Feature Engineering

Feature selection and transformation.
Fourth block in canonical pipeline.
"""
from backend.domain import ExecutionContext


def feature_engineering_block(context: ExecutionContext):
    """
    Feature selection and transformation.
    
    Responsibilities:
    - Feature selection (if needed)
    - Feature transformation
    - Feature creation
    
    Note: Basic implementation for v1.
    Advanced feature engineering can be added via hooks.
    """
    context.log("Starting feature engineering...")
    
    # For v1, we keep all features after preprocessing
    # Advanced feature engineering can be done via hooks
    
    context.log(f"Using {len(context.feature_names)} features")
    context.log("Feature engineering completed (using all preprocessed features)")
