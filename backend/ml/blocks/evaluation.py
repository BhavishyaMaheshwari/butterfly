"""
Butterfly ML Block - Evaluation

Evaluates trained models and selects best.
Eighth block in canonical pipeline.
"""
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score
)
from backend.domain import ExecutionContext


def evaluation_block(context: ExecutionContext):
    """
    Evaluate all trained models and select best.
    
    Responsibilities:
    - Compute metrics for each model
    - Rank models by performance
    - Select best model
    """
    context.log("Starting model evaluation...")
    
    # Get test data
    X_test = context.test_data[context.feature_names]
    y_test = context.test_data[context.target_column]
    
    context.log(f"Evaluating on {len(X_test)} test samples")
    
    results = []
    
    for name, model in context.trained_models:
        try:
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Compute metrics based on task type
            if context.detected_task == "classification":
                metrics = {
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
                    "recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
                    "f1": f1_score(y_test, y_pred, average='weighted', zero_division=0)
                }
                primary_metric = metrics["accuracy"]
            
            else:  # regression
                metrics = {
                    "mse": mean_squared_error(y_test, y_pred),
                    "mae": mean_absolute_error(y_test, y_pred),
                    "r2": r2_score(y_test, y_pred)
                }
                primary_metric = metrics["r2"]
            
            results.append({
                "name": name,
                "model": model,
                "metrics": metrics,
                "primary_metric": primary_metric
            })
            
            context.log(f"  {name}: {metrics}")
        
        except Exception as e:
            context.log(f"  ✗ {name} evaluation failed: {str(e)}")
    
    if not results:
        raise ValueError("All models failed evaluation")
    
    # Select best model
    if context.detected_task == "classification":
        # Higher is better for accuracy
        best_result = max(results, key=lambda r: r["primary_metric"])
    else:
        # Higher is better for R2
        best_result = max(results, key=lambda r: r["primary_metric"])
    
    context.best_model = best_result["model"]
    context.metrics = {
        "best_model": best_result["name"],
        "best_metrics": best_result["metrics"],
        "all_results": {r["name"]: r["metrics"] for r in results}
    }
    
    context.log(f"Best model: {best_result['name']}")
    context.log(f"Best metrics: {best_result['metrics']}")
    context.log("Evaluation completed")
