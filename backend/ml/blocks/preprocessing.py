"""
Butterfly ML Block - Preprocessing

Handles missing values, encoding, and scaling.
Third block in canonical pipeline.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from backend.domain import ExecutionContext


def preprocessing_block(context: ExecutionContext):
    """
    Preprocess data for ML.
    
    Responsibilities:
    - Handle missing values
    - Encode categorical variables
    - Scale numeric features
    - Split train/test
    """
    df = context.raw_data.copy()
    context.log("Starting preprocessing...")
    
    # Handle missing values
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        context.log(f"Found missing values: {missing_counts[missing_counts > 0].to_dict()}")
        
        # Simple strategy: drop rows with missing values
        # (More sophisticated strategies can be added via hooks)
        df = df.dropna()
        context.log(f"Dropped rows with missing values, {len(df)} rows remaining")
    
    # Separate features and target
    X = df[context.feature_names]
    y = df[context.target_column]
    
    # Encode categorical features
    categorical_cols = X.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        context.log(f"Encoding categorical columns: {list(categorical_cols)}")
        
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
    
    # Encode target if classification
    if context.detected_task == "classification":
        if y.dtype == 'object':
            context.log("Encoding target column")
            le = LabelEncoder()
            y = le.fit_transform(y)
            context.label_encoder = le  # Store for later decoding
            context.log(f"Target classes: {list(le.classes_)}")
    
    # Scale numeric features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    context.log("Features scaled using StandardScaler")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=context.seed,
        stratify=y if context.detected_task == "classification" else None
    )
    
    context.log(f"Train/test split: {len(X_train)} train, {len(X_test)} test")
    
    # Store processed data
    context.train_data = pd.concat([X_train, pd.Series(y_train, name=context.target_column, index=X_train.index)], axis=1)
    context.test_data = pd.concat([X_test, pd.Series(y_test, name=context.target_column, index=X_test.index)], axis=1)
    context.processed_data = df
    
    context.log("Preprocessing completed")
