"""
Butterfly ML Block - Model Selection

Recommends models based on task and data.
Fifth block in canonical pipeline.
"""
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor

from backend.domain import ExecutionContext


def model_selection_block(context: ExecutionContext):
    """
    Select candidate models based on task type.
    
    Responsibilities:
    - Recommend models based on task and data
    - Create candidate model instances
    - Allow manual override via hooks
    """
    context.log("Starting model selection...")
    
    task = context.detected_task
    n_samples = len(context.train_data)
    n_features = len(context.feature_names)
    
    context.log(f"Task: {task}, Samples: {n_samples}, Features: {n_features}")
    
    # Select models based on task
    if task == "classification":
        context.log("Selecting classification models")
        
        candidate_models = [
            ("Logistic Regression", LogisticRegression(random_state=context.seed, max_iter=1000)),
            ("Random Forest", RandomForestClassifier(random_state=context.seed, n_estimators=100)),
            ("XGBoost", XGBClassifier(random_state=context.seed, n_estimators=100, verbosity=0)),
            ("LightGBM", LGBMClassifier(random_state=context.seed, n_estimators=100, verbose=-1))
        ]
    
    elif task == "regression":
        context.log("Selecting regression models")
        
        candidate_models = [
            ("Ridge Regression", Ridge(random_state=context.seed)),
            ("Random Forest", RandomForestRegressor(random_state=context.seed, n_estimators=100)),
            ("XGBoost", XGBRegressor(random_state=context.seed, n_estimators=100, verbosity=0)),
            ("LightGBM", LGBMRegressor(random_state=context.seed, n_estimators=100, verbose=-1))
        ]
    
    else:
        raise ValueError(f"Unknown task type: {task}")
    
    context.candidate_models = candidate_models
    context.log(f"Selected {len(candidate_models)} candidate models:")
    for name, _ in candidate_models:
        context.log(f"  - {name}")
    
    context.log("Model selection completed")
