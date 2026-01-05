"""
Butterfly ML Block - Data Ingestion

Loads and validates dataset.
First block in canonical pipeline.
"""
import pandas as pd
from backend.domain import ExecutionContext


def data_ingestion_block(context: ExecutionContext):
    """
    Load and validate dataset.
    
    Responsibilities:
    - Load data from dataset path
    - Perform basic validation
    - Store in context
    """
    context.log(f"Loading dataset from {context.dataset_path}")
    
    # Load CSV
    df = pd.read_csv(context.dataset_path)
    context.raw_data = df
    
    context.log(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    context.log(f"Columns: {list(df.columns)}")
    
    # Basic validation
    if df.empty:
        raise ValueError("Dataset is empty")
    
    context.log("Data ingestion completed")
