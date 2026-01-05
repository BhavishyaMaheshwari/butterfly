"""
Butterfly Domain Model - Experiment

Represents a logical setup for running ML workflows on a dataset.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

from .pipeline import Pipeline


class TaskType(str, Enum):
    """ML task types"""
    AUTO_DETECT = "auto_detect"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    TIME_SERIES = "time_series"
    NLP = "nlp"
    COMPUTER_VISION = "computer_vision"


@dataclass
class Experiment:
    """
    Logical setup for running ML workflows on a dataset.
    
    Responsibilities:
    - Own a draft pipeline
    - Group related runs
    - Act as a comparison boundary
    
    Relationships:
    - One Experiment → one Dataset
    - One Experiment → one Pipeline (draft)
    - One Experiment → many Runs
    
    Invariants:
    - Experiments are editable; runs are not
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    dataset_id: str = ""
    task_type: TaskType = TaskType.AUTO_DETECT
    pipeline: Pipeline = field(default_factory=Pipeline)
    created_at: datetime = field(default_factory=datetime.utcnow)
    workspace_id: str = ""
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "dataset_id": self.dataset_id,
            "task_type": self.task_type.value,
            "pipeline": self.pipeline.to_dict(),
            "created_at": self.created_at.isoformat(),
            "workspace_id": self.workspace_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Experiment":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            dataset_id=data["dataset_id"],
            task_type=TaskType(data["task_type"]),
            pipeline=Pipeline.from_dict(data["pipeline"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            workspace_id=data["workspace_id"]
        )
