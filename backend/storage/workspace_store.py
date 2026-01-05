"""
Butterfly Storage Layer - Workspace Store

Manages workspace directory structure and persistence.
Follows 07_backend_responsibilities.md.
"""
from pathlib import Path
from typing import Optional
import json

from backend.domain import Workspace


class WorkspaceStore:
    """
    Manages workspace directory structure and metadata persistence.
    
    Responsibilities:
    - Create, load, and persist workspaces
    - Maintain workspace directory structure
    - Manage workspace metadata
    
    Guarantees:
    - Workspace state is always recoverable
    - No workspace data is mutated implicitly
    """
    
    def __init__(self, base_path: Path = Path("workspaces")):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def create(self, workspace: Workspace) -> Workspace:
        """
        Create a new workspace with directory structure.
        
        Directory structure:
        workspace/
          ├── workspace.json (metadata)
          ├── datasets/
          ├── experiments/
          └── runs/
        """
        # Create workspace directory
        workspace.root_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        workspace.datasets_path.mkdir(exist_ok=True)
        workspace.experiments_path.mkdir(exist_ok=True)
        workspace.runs_path.mkdir(exist_ok=True)
        
        # Save metadata
        self._save_metadata(workspace)
        
        return workspace
    
    def load(self, workspace_id: str) -> Optional[Workspace]:
        """Load workspace by ID"""
        # Search for workspace in base path
        for workspace_dir in self.base_path.iterdir():
            if not workspace_dir.is_dir():
                continue
            
            metadata_file = workspace_dir / "workspace.json"
            if not metadata_file.exists():
                continue
            
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            
            if data["id"] == workspace_id:
                return Workspace.from_dict(data)
        
        return None
    
    def load_by_name(self, name: str) -> Optional[Workspace]:
        """Load workspace by name"""
        workspace_path = self.base_path / name
        metadata_file = workspace_path / "workspace.json"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
        
        return Workspace.from_dict(data)
    
    def get_or_create_default(self) -> Workspace:
        """Get or create the default workspace"""
        workspace = self.load_by_name("default")
        
        if workspace is None:
            workspace = Workspace(
                name="default",
                root_path=self.base_path / "default"
            )
            workspace = self.create(workspace)
        
        return workspace
    
    def list_all(self) -> list[Workspace]:
        """List all workspaces"""
        workspaces = []
        
        for workspace_dir in self.base_path.iterdir():
            if not workspace_dir.is_dir():
                continue
            
            metadata_file = workspace_dir / "workspace.json"
            if not metadata_file.exists():
                continue
            
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            
            workspaces.append(Workspace.from_dict(data))
        
        return workspaces
    
    def _save_metadata(self, workspace: Workspace):
        """Save workspace metadata to JSON"""
        metadata_file = workspace.root_path / "workspace.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(workspace.to_dict(), f, indent=2)
