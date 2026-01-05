"""
Butterfly Storage Layer - Experiment Store

Manages experiment and pipeline state persistence.
Follows 07_backend_responsibilities.md.
"""
from pathlib import Path
from typing import List, Optional
import json

from backend.domain import Experiment, Pipeline, Hook


class ExperimentStore:
    """
    Manages experiment and pipeline state.
    
    Responsibilities:
    - Create and persist experiments
    - Manage draft pipeline state
    - Validate pipeline structure
    - Store hooks
    
    Guarantees:
    - Draft pipelines are editable
    - Snapshotted pipelines are immutable
    - Experiments cleanly separate draft and run states
    """
    
    def __init__(self, experiments_path: Path):
        self.experiments_path = experiments_path
        self.experiments_path.mkdir(parents=True, exist_ok=True)
    
    def create(self, experiment: Experiment) -> Experiment:
        """Create new experiment"""
        experiment_dir = self.experiments_path / experiment.id
        experiment_dir.mkdir(exist_ok=True)
        
        # Create hooks directory
        (experiment_dir / "hooks").mkdir(exist_ok=True)
        
        self._save_metadata(experiment, experiment_dir)
        return experiment
    
    def save(self, experiment: Experiment):
        """Save experiment (update draft pipeline)"""
        experiment_dir = self.experiments_path / experiment.id
        if not experiment_dir.exists():
            raise ValueError(f"Experiment {experiment.id} does not exist")
        
        self._save_metadata(experiment, experiment_dir)
    
    def load(self, experiment_id: str) -> Optional[Experiment]:
        """Load experiment by ID"""
        experiment_dir = self.experiments_path / experiment_id
        metadata_file = experiment_dir / "metadata.json"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
        
        return Experiment.from_dict(data)
    
    def list_all(self, workspace_id: str) -> List[Experiment]:
        """List all experiments in workspace"""
        experiments = []
        
        for experiment_dir in self.experiments_path.iterdir():
            if not experiment_dir.is_dir():
                continue
            
            metadata_file = experiment_dir / "metadata.json"
            if not metadata_file.exists():
                continue
            
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            
            experiment = Experiment.from_dict(data)
            if experiment.workspace_id == workspace_id:
                experiments.append(experiment)
        
        return experiments
    
    def save_hook(self, experiment_id: str, hook: Hook):
        """Save hook for experiment"""
        experiment_dir = self.experiments_path / experiment_id
        hooks_dir = experiment_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        hook_file = hooks_dir / f"{hook.id}.json"
        with open(hook_file, 'w') as f:
            json.dump(hook.to_dict(), f, indent=2)
    
    def load_hook(self, experiment_id: str, hook_id: str) -> Optional[Hook]:
        """Load hook by ID"""
        experiment_dir = self.experiments_path / experiment_id
        hook_file = experiment_dir / "hooks" / f"{hook_id}.json"
        
        if not hook_file.exists():
            return None
        
        with open(hook_file, 'r') as f:
            data = json.load(f)
        
        return Hook.from_dict(data)
    
    def list_hooks(self, experiment_id: str) -> List[Hook]:
        """List all hooks for experiment"""
        experiment_dir = self.experiments_path / experiment_id
        hooks_dir = experiment_dir / "hooks"
        
        if not hooks_dir.exists():
            return []
        
        hooks = []
        for hook_file in hooks_dir.glob("*.json"):
            with open(hook_file, 'r') as f:
                data = json.load(f)
            hooks.append(Hook.from_dict(data))
        
        return hooks
    
    def delete_hook(self, experiment_id: str, hook_id: str):
        """Delete hook"""
        experiment_dir = self.experiments_path / experiment_id
        hook_file = experiment_dir / "hooks" / f"{hook_id}.json"
        
        if hook_file.exists():
            hook_file.unlink()
    
    def _save_metadata(self, experiment: Experiment, experiment_dir: Path):
        """Save experiment metadata to JSON"""
        metadata_file = experiment_dir / "metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(experiment.to_dict(), f, indent=2)
