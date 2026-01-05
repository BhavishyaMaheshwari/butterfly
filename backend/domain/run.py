"""
Butterfly Domain Model - Run

Represents a single immutable execution of a pipeline.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

from .pipeline import Pipeline


class RunStatus(str, Enum):
    """Run execution status"""
    CREATED = "created"      # Run created, not started
    RUNNING = "running"      # Currently executing
    COMPLETED = "completed"  # Successfully completed
    FAILED = "failed"        # Failed with error


@dataclass
class Run:
    """
    Single immutable execution of a pipeline.
    
    Responsibilities:
    - Execute a frozen snapshot of the pipeline
    - Produce artifacts
    - Store metrics and logs
    
    Key Properties from 09_execution_rules.md:
    - Immutable once completed
    - Pipeline snapshotted at creation
    - Dataset hash locked
    - Global seed fixed
    
    Invariants (NON-NEGOTIABLE):
    - Completed runs cannot be modified
    - Same seed + same input = same output
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    experiment_id: str = ""
    pipeline_snapshot: Pipeline = field(default_factory=Pipeline)
    dataset_hash: str = ""  # Locked dataset version
    seed: int = 42  # Global seed for determinism
    status: RunStatus = RunStatus.CREATED
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Error tracking
    error_message: Optional[str] = None
    failed_block_id: Optional[str] = None
    
    def start(self):
        """Mark run as started. Can only be called once."""
        if self.status != RunStatus.CREATED:
            raise ValueError(f"Cannot start run in status {self.status}")
        self.status = RunStatus.RUNNING
        self.started_at = datetime.utcnow()
    
    def complete(self):
        """Mark run as completed. Enforces immutability."""
        if self.status != RunStatus.RUNNING:
            raise ValueError(f"Cannot complete run in status {self.status}")
        self.status = RunStatus.COMPLETED
        self.completed_at = datetime.utcnow()
    
    def fail(self, error_message: str, failed_block_id: Optional[str] = None):
        """Mark run as failed with error details."""
        if self.status not in [RunStatus.CREATED, RunStatus.RUNNING]:
            raise ValueError(f"Cannot fail run in status {self.status}")
        self.status = RunStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
        self.failed_block_id = failed_block_id
    
    @property
    def is_immutable(self) -> bool:
        """Check if run is immutable (completed or failed)"""
        return self.status in [RunStatus.COMPLETED, RunStatus.FAILED]
    
    @property
    def is_running(self) -> bool:
        """Check if run is currently executing"""
        return self.status == RunStatus.RUNNING
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "experiment_id": self.experiment_id,
            "pipeline_snapshot": self.pipeline_snapshot.to_dict(),
            "dataset_hash": self.dataset_hash,
            "seed": self.seed,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "failed_block_id": self.failed_block_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Run":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            experiment_id=data["experiment_id"],
            pipeline_snapshot=Pipeline.from_dict(data["pipeline_snapshot"]),
            dataset_hash=data["dataset_hash"],
            seed=data["seed"],
            status=RunStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            error_message=data.get("error_message"),
            failed_block_id=data.get("failed_block_id")
        )
