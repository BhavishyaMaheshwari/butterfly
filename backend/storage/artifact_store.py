"""
Butterfly Storage Layer - Artifact Store

Manages artifact file storage and retrieval.
Follows 07_backend_responsibilities.md.
"""
from pathlib import Path
from typing import List, Optional
import json
import shutil

from backend.domain import Artifact


class ArtifactStore:
    """
    Manages artifact files.
    
    Responsibilities:
    - Store run artifacts locally
    - Organize artifacts by run
    - Provide export paths
    
    Guarantees:
    - Artifacts are immutable
    - Artifacts are tied to a specific run
    """
    
    def __init__(self, runs_path: Path):
        self.runs_path = runs_path
    
    def save(self, artifact: Artifact, source_file: Optional[Path] = None) -> Artifact:
        """
        Save artifact metadata and optionally copy file.
        
        Args:
            artifact: Artifact metadata
            source_file: Optional source file to copy into artifact storage
        """
        run_dir = self.runs_path / artifact.run_id
        artifacts_dir = run_dir / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy file if provided
        if source_file and source_file.exists():
            dest_file = artifacts_dir / source_file.name
            shutil.copy2(source_file, dest_file)
            artifact.file_path = dest_file
        
        # Save metadata
        metadata_file = artifacts_dir / f"{artifact.id}.json"
        with open(metadata_file, 'w') as f:
            json.dump(artifact.to_dict(), f, indent=2)
        
        return artifact
    
    def load(self, run_id: str, artifact_id: str) -> Optional[Artifact]:
        """Load artifact by ID"""
        run_dir = self.runs_path / run_id
        metadata_file = run_dir / "artifacts" / f"{artifact_id}.json"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
        
        return Artifact.from_dict(data)
    
    def list_by_run(self, run_id: str) -> List[Artifact]:
        """List all artifacts for a run"""
        run_dir = self.runs_path / run_id
        artifacts_dir = run_dir / "artifacts"
        
        if not artifacts_dir.exists():
            return []
        
        artifacts = []
        for metadata_file in artifacts_dir.glob("*.json"):
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            artifacts.append(Artifact.from_dict(data))
        
        return artifacts
    
    def get_file_path(self, run_id: str, artifact_id: str) -> Optional[Path]:
        """Get file path for artifact"""
        artifact = self.load(run_id, artifact_id)
        if artifact and artifact.file_path:
            return artifact.file_path
        return None
