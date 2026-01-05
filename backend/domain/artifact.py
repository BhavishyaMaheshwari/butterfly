"""
Butterfly Domain Model - Artifact

Represents any output produced by a run.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional
import uuid


class ArtifactType(str, Enum):
    """Types of artifacts produced by runs"""
    MODEL = "model"                    # Trained model file
    METRICS = "metrics"                # Evaluation metrics
    PLOT = "plot"                      # Visualization
    EXPLAINABILITY = "explainability"  # SHAP, feature importance
    NOTEBOOK = "notebook"              # Generated notebook
    LOG = "log"                        # Execution logs
    OTHER = "other"                    # Custom artifacts


@dataclass
class Artifact:
    """
    Output produced by a run.
    
    Examples:
    - Trained model file
    - Metrics report
    - Plots
    - Explainability outputs
    - Generated notebook
    
    Responsibilities:
    - Store execution outputs
    - Enable inspection and export
    
    Invariants:
    - Artifacts are read-only
    - Artifacts are tied to specific runs
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: ArtifactType = ArtifactType.OTHER
    run_id: str = ""
    file_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Ensure file_path is a Path object if provided"""
        if self.file_path and isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)
    
    @property
    def exists(self) -> bool:
        """Check if artifact file exists"""
        return self.file_path is not None and self.file_path.exists()
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "run_id": self.run_id,
            "file_path": str(self.file_path) if self.file_path else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Artifact":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            type=ArtifactType(data["type"]),
            run_id=data["run_id"],
            file_path=Path(data["file_path"]) if data.get("file_path") else None,
            metadata=data["metadata"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
