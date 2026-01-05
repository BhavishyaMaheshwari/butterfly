"""
Butterfly ML Block - Explainability

Generates model explanations and feature importance.
Ninth block in canonical pipeline.
"""
import numpy as np
from backend.domain import ExecutionContext


def explainability_block(context: ExecutionContext):
    """
    Generate model explanations.
    
    Responsibilities:
    - Compute feature importance
    - Generate SHAP values (if applicable)
    - Create explainability outputs
    
    Note: Basic implementation for v1.
    Full SHAP integration can be added later.
    """
    context.log("Starting explainability...")
    
    # Try to get feature importance from model
    if hasattr(context.best_model, 'feature_importances_'):
        # Tree-based models have feature_importances_
        importances = context.best_model.feature_importances_
        context.feature_importance = dict(zip(context.feature_names, importances.tolist()))
        
        context.log("Feature importance:")
        # Sort by importance
        sorted_features = sorted(context.feature_importance.items(), key=lambda x: x[1], reverse=True)
        for feat, imp in sorted_features[:10]:  # Top 10
            context.log(f"  {feat}: {imp:.4f}")
    
    elif hasattr(context.best_model, 'coef_'):
        # Linear models have coefficients
        coef = context.best_model.coef_
        if len(coef.shape) > 1:
            # Multi-class: use mean absolute coefficient
            importances = np.abs(coef).mean(axis=0)
        else:
            importances = np.abs(coef)
        
        context.feature_importance = dict(zip(context.feature_names, importances.tolist()))
        
        context.log("Feature importance (from coefficients):")
        sorted_features = sorted(context.feature_importance.items(), key=lambda x: x[1], reverse=True)
        for feat, imp in sorted_features[:10]:
            context.log(f"  {feat}: {imp:.4f}")
    
    else:
        context.log("Model does not support feature importance")
        context.feature_importance = {}
    
    context.log("Explainability completed")
