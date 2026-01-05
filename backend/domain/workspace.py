"""
Butterfly Domain Model - Workspace

Represents the top-level container for all user activity.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


@dataclass
class Workspace:
    """
    Top-level container for datasets, experiments, and runs.
    
    Responsibilities:
    - Own datasets, experiments, and runs
    - Define storage location
    - Persist all state locally
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "default"
    root_path: Path = field(default_factory=lambda: Path("workspaces/default"))
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Ensure root_path is a Path object"""
        if isinstance(self.root_path, str):
            self.root_path = Path(self.root_path)
    
    @property
    def datasets_path(self) -> Path:
        """Path to datasets directory"""
        return self.root_path / "datasets"
    
    @property
    def experiments_path(self) -> Path:
        """Path to experiments directory"""
        return self.root_path / "experiments"
    
    @property
    def runs_path(self) -> Path:
        """Path to runs directory"""
        return self.root_path / "runs"
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "root_path": str(self.root_path),
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Workspace":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            root_path=Path(data["root_path"]),
            created_at=datetime.fromisoformat(data["created_at"])
        )
