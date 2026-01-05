"""
Butterfly Domain Model - Dataset

Represents a versioned input data source.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import uuid


@dataclass
class Dataset:
    """
    Versioned input data source.
    
    Responsibilities:
    - Store dataset metadata
    - Provide consistent data access
    - Enable lineage and reproducibility
    
    Invariants:
    - Datasets are immutable once imported
    - Hash uniquely identifies content
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source_path: Path = field(default_factory=Path)
    schema: Dict[str, str] = field(default_factory=dict)  # column_name -> type
    row_count: int = 0
    content_hash: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    workspace_id: str = ""
    
    def __post_init__(self):
        """Ensure source_path is a Path object"""
        if isinstance(self.source_path, str):
            self.source_path = Path(self.source_path)
    
    @staticmethod
    def compute_hash(file_path: Path) -> str:
        """
        Compute content-based hash for lineage tracking.
        Uses SHA-256 for deterministic hashing.
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "source_path": str(self.source_path),
            "schema": self.schema,
            "row_count": self.row_count,
            "content_hash": self.content_hash,
            "created_at": self.created_at.isoformat(),
            "workspace_id": self.workspace_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Dataset":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            source_path=Path(data["source_path"]),
            schema=data["schema"],
            row_count=data["row_count"],
            content_hash=data["content_hash"],
            created_at=datetime.fromisoformat(data["created_at"]),
            workspace_id=data["workspace_id"]
        )
