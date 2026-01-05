"""
Butterfly Domain Model - Pipeline

Represents the ordered ML workflow definition.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any
import hashlib
import json
import uuid

from .block import Block, BlockType


@dataclass
class Pipeline:
    """
    Ordered ML workflow definition.
    
    Responsibilities:
    - Define execution order
    - Hold block configuration
    - Serve as the blueprint for runs
    
    Invariants:
    - Pipelines are mutable only in draft state
    - Snapshotted pipelines are immutable
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    blocks: List[Block] = field(default_factory=list)
    global_config: Dict[str, Any] = field(default_factory=dict)
    version_hash: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Initialize with canonical block order if empty"""
        if not self.blocks:
            self._initialize_canonical_blocks()
        if not self.version_hash:
            self.version_hash = self.compute_hash()
    
    def _initialize_canonical_blocks(self):
        """
        Create canonical pipeline blocks in order.
        From 09_execution_rules.md section 4.1.
        """
        canonical_order = [
            BlockType.DATA_INGESTION,
            BlockType.TASK_RESOLUTION,
            BlockType.PREPROCESSING,
            BlockType.FEATURE_ENGINEERING,
            BlockType.MODEL_SELECTION,
            BlockType.HYPERPARAMETER_TUNING,
            BlockType.TRAINING,
            BlockType.EVALUATION,
            BlockType.EXPLAINABILITY,
            BlockType.OUTPUT_PACKAGING
        ]
        
        self.blocks = [
            Block(type=block_type, position=i)
            for i, block_type in enumerate(canonical_order)
        ]
    
    def compute_hash(self) -> str:
        """
        Compute version hash for pipeline snapshot.
        Hash includes block order, configs, and hook references.
        """
        # Create deterministic representation
        pipeline_repr = {
            "blocks": [block.to_dict() for block in sorted(self.blocks, key=lambda b: b.position)],
            "global_config": self.global_config
        }
        
        # Serialize to JSON with sorted keys for determinism
        json_str = json.dumps(pipeline_repr, sort_keys=True)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
    
    def snapshot(self) -> "Pipeline":
        """
        Create immutable snapshot for run execution.
        Updates version hash to reflect current state.
        """
        snapshot = Pipeline(
            id=str(uuid.uuid4()),  # New ID for snapshot
            blocks=[Block.from_dict(b.to_dict()) for b in self.blocks],  # Deep copy
            global_config=self.global_config.copy(),
            created_at=datetime.utcnow()
        )
        snapshot.version_hash = snapshot.compute_hash()
        return snapshot
    
    def get_block_by_type(self, block_type: BlockType) -> Block | None:
        """Get block by type"""
        for block in self.blocks:
            if block.type == block_type:
                return block
        return None
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "blocks": [block.to_dict() for block in self.blocks],
            "global_config": self.global_config,
            "version_hash": self.version_hash,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Pipeline":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            blocks=[Block.from_dict(b) for b in data["blocks"]],
            global_config=data["global_config"],
            version_hash=data["version_hash"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
