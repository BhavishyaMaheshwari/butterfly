"""
Butterfly ML Block - Task Resolution

Auto-detects or uses manual task type.
Second block in canonical pipeline.
"""
import pandas as pd
import numpy as np
from backend.domain import ExecutionContext


def task_resolution_block(context: ExecutionContext):
    """
    Determine ML task type (classification vs regression).
    
    Responsibilities:
    - Auto-detect task from data if needed
    - Respect manual override
    - Identify target column
    """
    df = context.raw_data
    
    if context.task_type == "auto_detect":
        context.log("Auto-detecting task type...")
        
        # Simple heuristic: find column with most unique values as features
        # and column with least unique values as potential target
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns found for task detection")
        
        # Assume last column is target (common convention)
        target_col = df.columns[-1]
        context.target_column = target_col
        
        # Detect task type based on target
        unique_values = df[target_col].nunique()
        total_values = len(df[target_col])
        target_dtype = df[target_col].dtype
        
        # Classification if:
        # 1. Target is non-numeric (object/string type), OR
        # 2. Target has few unique values relative to total
        if target_dtype == 'object' or (unique_values < 20 and unique_values / total_values < 0.5):
            context.detected_task = "classification"
            context.log(f"Detected classification task (target: {target_col}, {unique_values} classes)")
        else:
            context.detected_task = "regression"
            context.log(f"Detected regression task (target: {target_col})")
    
    else:
        # Manual task type specified
        context.detected_task = context.task_type
        context.log(f"Using manual task type: {context.task_type}")
        
        # Still need to identify target column
        if not context.target_column:
            context.target_column = df.columns[-1]
            context.log(f"Using last column as target: {context.target_column}")
    
    # Store feature names (all columns except target)
    context.feature_names = [col for col in df.columns if col != context.target_column]
    context.log(f"Features: {context.feature_names}")
    
    context.log("Task resolution completed")
