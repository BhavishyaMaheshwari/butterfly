"""
Butterfly Domain Model - Hook

Represents user-provided code injected into pipeline execution.
Follows 06_domain_model.md specification.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import hashlib
import uuid


class HookType(str, Enum):
    """Hook types following execution rules"""
    BEFORE = "before"  # Runs before system logic
    AFTER = "after"    # Runs after system logic
    OVERRIDE = "override"  # Replaces system logic


class HookSource(str, Enum):
    """Where the hook code comes from"""
    INLINE = "inline"  # Code written in UI
    FILE = "file"      # Uploaded .py file


@dataclass
class Hook:
    """
    User-provided code injected into pipeline execution.
    
    Responsibilities:
    - Modify or replace system behavior
    - Operate on execution context
    
    Hook Precedence (from 09_execution_rules.md):
    1. override hooks (skip system logic)
    2. before hooks
    3. system block logic
    4. after hooks
    
    Invariants:
    - Hooks are versioned via code hashing
    - Hooks affect only the current run
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: HookType = HookType.BEFORE
    block_id: str = ""  # Which block this hook is attached to
    source: HookSource = HookSource.INLINE
    code: str = ""
    code_hash: str = ""
    file_path: Optional[str] = None  # If source is FILE
    
    def __post_init__(self):
        """Compute code hash if not provided"""
        if not self.code_hash and self.code:
            self.code_hash = self.compute_hash(self.code)
    
    @staticmethod
    def compute_hash(code: str) -> str:
        """
        Compute deterministic hash of hook code for versioning.
        Uses SHA-256 for consistency with dataset hashing.
        """
        return hashlib.sha256(code.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "block_id": self.block_id,
            "source": self.source.value,
            "code": self.code,
            "code_hash": self.code_hash,
            "file_path": self.file_path
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Hook":
        """Deserialize from dictionary"""
        return cls(
            id=data["id"],
            type=HookType(data["type"]),
            block_id=data["block_id"],
            source=HookSource(data["source"]),
            code=data["code"],
            code_hash=data["code_hash"],
            file_path=data.get("file_path")
        )
