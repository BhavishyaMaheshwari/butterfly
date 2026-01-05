"""
Butterfly ML Block - Training

Trains all candidate models.
Seventh block in canonical pipeline.
"""
from backend.domain import ExecutionContext


def training_block(context: ExecutionContext):
    """
    Train all candidate models.
    
    Responsibilities:
    - Train each candidate model
    - Handle training errors gracefully
    - Store trained models
    """
    context.log("Starting model training...")
    
    # Get training data
    X_train = context.train_data[context.feature_names]
    y_train = context.train_data[context.target_column]
    
    context.log(f"Training on {len(X_train)} samples")
    
    trained_models = []
    
    for name, model in context.candidate_models:
        try:
            context.log(f"Training {name}...")
            model.fit(X_train, y_train)
            trained_models.append((name, model))
            context.log(f"  ✓ {name} trained successfully")
        
        except Exception as e:
            context.log(f"  ✗ {name} training failed: {str(e)}")
            # Continue with other models
    
    if not trained_models:
        raise ValueError("All models failed to train")
    
    context.trained_models = trained_models
    context.log(f"Training completed: {len(trained_models)}/{len(context.candidate_models)} models trained")
