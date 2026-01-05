"""
Butterfly Domain Model - Block

Represents a single stage in the ML pipeline.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class BlockType(str, Enum):
    """Canonical pipeline block types"""
    DATA_INGESTION = "data_ingestion"
    TASK_RESOLUTION = "task_resolution"
    PREPROCESSING = "preprocessing"
    FEATURE_ENGINEERING = "feature_engineering"
    MODEL_SELECTION = "model_selection"
    HYPERPARAMETER_TUNING = "hyperparameter_tuning"
    TRAINING = "training"
    EVALUATION = "evaluation"
    EXPLAINABILITY = "explainability"
    OUTPUT_PACKAGING = "output_packaging"


class BlockStatus(str, Enum):
    """Block execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Block:
    """
    Single stage in the ML pipeline.
    
    Responsibilities:
    - Encapsulate stage logic
    - Expose configuration
    - Accept user code overrides
    
    Note: Blocks are the smallest executable unit.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: BlockType = BlockType.DATA_INGESTION
    position: int = 0  # Position in pipeline
    config: Dict[str, Any] = field(default_factory=dict)
    status: BlockStatus = BlockStatus.IDLE
    enabled: bool = True
    
    # Hook references (hook IDs)
    before_hooks: List[str] = field(default_factory=list)
    after_hooks: List[str] = field(default_factory=list)
    override_hooks: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "position": self.position,
            "config": self.config,
            "status": self.status.value,
            "enabled": self.enabled,
            "before_hooks": self.before_hooks,
            "after_hooks": self.after_hooks,
            "override_hooks": self.override_hooks
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            type=BlockType(data["type"]),
            position=data["position"],
            config=data["config"],
            status=BlockStatus(data["status"]),
            enabled=data["enabled"],
            before_hooks=data.get("before_hooks", []),
            after_hooks=data.get("after_hooks", []),
            override_hooks=data.get("override_hooks", [])
        )
