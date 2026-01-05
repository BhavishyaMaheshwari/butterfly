"""
Butterfly Storage Layer - Run Store

Manages run metadata, logs, and artifacts persistence.
Follows 07_backend_responsibilities.md.
"""
from pathlib import Path
from typing import List, Optional
import json

from backend.domain import Run, Artifact


class RunStore:
    """
    Manages run metadata, logs, and artifacts.
    
    Responsibilities:
    - Persist run metadata
    - Store execution logs
    - Track lineage
    - Support run comparison queries
    
    Guarantees:
    - Full reproducibility
    - Accurate lineage derivation
    """
    
    def __init__(self, runs_path: Path):
        self.runs_path = runs_path
        self.runs_path.mkdir(parents=True, exist_ok=True)
    
    def create(self, run: Run) -> Run:
        """Create new run"""
        run_dir = self.runs_path / run.id
        run_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (run_dir / "artifacts").mkdir(exist_ok=True)
        (run_dir / "logs").mkdir(exist_ok=True)
        
        self._save_metadata(run, run_dir)
        return run
    
    def save(self, run: Run):
        """
        Save run metadata.
        
        Note: Enforces immutability - completed runs cannot be modified.
        """
        run_dir = self.runs_path / run.id
        if not run_dir.exists():
            raise ValueError(f"Run {run.id} does not exist")
        
        # Load existing run to check immutability
        existing_run = self.load(run.id)
        if existing_run and existing_run.is_immutable:
            raise ValueError(f"Cannot modify completed run {run.id}")
        
        self._save_metadata(run, run_dir)
    
    def load(self, run_id: str) -> Optional[Run]:
        """Load run by ID"""
        run_dir = self.runs_path / run_id
        metadata_file = run_dir / "metadata.json"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
        
        return Run.from_dict(data)
    
    def list_by_experiment(self, experiment_id: str) -> List[Run]:
        """List all runs for an experiment"""
        runs = []
        
        for run_dir in self.runs_path.iterdir():
            if not run_dir.is_dir():
                continue
            
            metadata_file = run_dir / "metadata.json"
            if not metadata_file.exists():
                continue
            
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            
            run = Run.from_dict(data)
            if run.experiment_id == experiment_id:
                runs.append(run)
        
        # Sort by creation time (newest first)
        runs.sort(key=lambda r: r.created_at, reverse=True)
        return runs
    
    def list_recent(self, limit: int = 10) -> List[Run]:
        """List recent runs across all experiments"""
        runs = []
        
        for run_dir in self.runs_path.iterdir():
            if not run_dir.is_dir():
                continue
            
            metadata_file = run_dir / "metadata.json"
            if not metadata_file.exists():
                continue
            
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            
            runs.append(Run.from_dict(data))
        
        # Sort by creation time (newest first) and limit
        runs.sort(key=lambda r: r.created_at, reverse=True)
        return runs[:limit]
    
    def append_log(self, run_id: str, message: str):
        """Append log message to run"""
        run_dir = self.runs_path / run_id
        log_file = run_dir / "logs" / "execution.log"
        
        with open(log_file, 'a') as f:
            f.write(message + '\n')
    
    def get_logs(self, run_id: str) -> List[str]:
        """Get all log messages for run"""
        run_dir = self.runs_path / run_id
        log_file = run_dir / "logs" / "execution.log"
        
        if not log_file.exists():
            return []
        
        with open(log_file, 'r') as f:
            return f.readlines()
    
    def get_artifacts_dir(self, run_id: str) -> Path:
        """Get artifacts directory for run"""
        return self.runs_path / run_id / "artifacts"
    
    def _save_metadata(self, run: Run, run_dir: Path):
        """Save run metadata to JSON"""
        metadata_file = run_dir / "metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(run.to_dict(), f, indent=2)
