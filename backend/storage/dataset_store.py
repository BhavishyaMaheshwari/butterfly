"""
Butterfly Storage Layer - Dataset Store

Manages dataset files and metadata persistence.
Follows 07_backend_responsibilities.md.
"""
from pathlib import Path
from typing import List, Optional
import json
import shutil
import pandas as pd

from backend.domain import Dataset


class DatasetStore:
    """
    Manages dataset files and metadata.
    
    Responsibilities:
    - Import datasets into workspace
    - Validate dataset integrity
    - Infer schema and basic statistics
    - Compute content-based hashes
    
    Guarantees:
    - Datasets are immutable after import
    - Dataset hashes uniquely identify content
    """
    
    def __init__(self, datasets_path: Path):
        self.datasets_path = datasets_path
        self.datasets_path.mkdir(parents=True, exist_ok=True)
    
    def import_csv(self, source_file: Path, dataset: Dataset) -> Dataset:
        """
        Import CSV file into workspace.
        
        Steps:
        1. Copy file to workspace
        2. Compute content hash
        3. Infer schema
        4. Save metadata
        """
        # Create dataset directory
        dataset_dir = self.datasets_path / dataset.id
        dataset_dir.mkdir(exist_ok=True)
        
        # Copy file
        dest_file = dataset_dir / "data.csv"
        shutil.copy2(source_file, dest_file)
        dataset.source_path = dest_file
        
        # Compute hash
        dataset.content_hash = Dataset.compute_hash(dest_file)
        
        # Infer schema and stats
        df = pd.read_csv(dest_file)
        dataset.row_count = len(df)
        dataset.schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # Save metadata
        self._save_metadata(dataset, dataset_dir)
        
        return dataset
    
    def load(self, dataset_id: str) -> Optional[Dataset]:
        """Load dataset by ID"""
        dataset_dir = self.datasets_path / dataset_id
        metadata_file = dataset_dir / "metadata.json"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
        
        return Dataset.from_dict(data)
    
    def list_all(self, workspace_id: str) -> List[Dataset]:
        """List all datasets in workspace"""
        datasets = []
        
        for dataset_dir in self.datasets_path.iterdir():
            if not dataset_dir.is_dir():
                continue
            
            metadata_file = dataset_dir / "metadata.json"
            if not metadata_file.exists():
                continue
            
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            
            dataset = Dataset.from_dict(data)
            if dataset.workspace_id == workspace_id:
                datasets.append(dataset)
        
        return datasets
    
    def get_dataframe(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """Load dataset as pandas DataFrame"""
        dataset = self.load(dataset_id)
        if dataset is None or not dataset.source_path.exists():
            return None
        
        return pd.read_csv(dataset.source_path)
    
    def get_preview(self, dataset_id: str, n_rows: int = 10) -> Optional[pd.DataFrame]:
        """Get preview of dataset (first n rows)"""
        dataset = self.load(dataset_id)
        if dataset is None or not dataset.source_path.exists():
            return None
        
        return pd.read_csv(dataset.source_path, nrows=n_rows)
    
    def get_statistics(self, dataset_id: str) -> Optional[dict]:
        """Get basic statistics for dataset"""
        df = self.get_dataframe(dataset_id)
        if df is None:
            return None
        
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
    
    def _save_metadata(self, dataset: Dataset, dataset_dir: Path):
        """Save dataset metadata to JSON"""
        metadata_file = dataset_dir / "metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(dataset.to_dict(), f, indent=2)
