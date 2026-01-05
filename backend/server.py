"""
Butterfly Backend Server

FastAPI application serving HTTP + WebSocket APIs.
Follows 07_backend_responsibilities.md.

=============================================================================
ARCHITECTURE: API LAYER
=============================================================================

This file contains ONLY HTTP routing logic.
NO ML LOGIC should exist here.

Responsibilities:
- Define FastAPI routes
- Validate HTTP requests
- Call execution/storage layers
- Return HTTP responses
- Handle WebSocket connections

Rules:
- NEVER execute ML directly
- NEVER manipulate execution context
- NEVER implement business logic
- Delegate to execution layer (executor.py)
- Delegate to storage layer (stores)

Layer Separation:
API (this file) → Execution (executor.py) → ML Blocks (ml/blocks/)
                → Storage (stores)

=============================================================================
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional
import asyncio
import uvicorn

from backend.domain import (
    Workspace, Dataset, Experiment, TaskType, Run, Hook, HookType, HookSource,
    BlockType
)
from backend.storage import (
    WorkspaceStore, DatasetStore, ExperimentStore, RunStore, ArtifactStore
)
from backend.execution import Executor
from backend.ml.blocks import *


# Pydantic models for API
class CreateExperimentRequest(BaseModel):
    name: str
    dataset_id: str
    task_type: str = "auto_detect"


class CreateRunRequest(BaseModel):
    experiment_id: str
    seed: Optional[int] = 42


class CreateHookRequest(BaseModel):
    block_id: str
    hook_type: str  # "before", "after", "override"
    code: str


# Initialize FastAPI app
app = FastAPI(title="Butterfly", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage layer
workspace_store = WorkspaceStore()
workspace = workspace_store.get_or_create_default()

dataset_store = DatasetStore(workspace.datasets_path)
experiment_store = ExperimentStore(workspace.experiments_path)
run_store = RunStore(workspace.runs_path)
artifact_store = ArtifactStore(workspace.runs_path)

# Initialize executor
executor = Executor(dataset_store, experiment_store, run_store, artifact_store)

# Register ML block implementations
executor.register_block_implementation(BlockType.DATA_INGESTION, data_ingestion_block)
executor.register_block_implementation(BlockType.TASK_RESOLUTION, task_resolution_block)
executor.register_block_implementation(BlockType.PREPROCESSING, preprocessing_block)
executor.register_block_implementation(BlockType.FEATURE_ENGINEERING, feature_engineering_block)
executor.register_block_implementation(BlockType.MODEL_SELECTION, model_selection_block)
executor.register_block_implementation(BlockType.HYPERPARAMETER_TUNING, hyperparameter_tuning_block)
executor.register_block_implementation(BlockType.TRAINING, training_block)
executor.register_block_implementation(BlockType.EVALUATION, evaluation_block)
executor.register_block_implementation(BlockType.EXPLAINABILITY, explainability_block)
executor.register_block_implementation(BlockType.OUTPUT_PACKAGING, output_packaging_block)


# ============================================================================
# Workspace Endpoints
# ============================================================================

@app.get("/api/workspace")
async def get_workspace():
    """Get current workspace info"""
    return workspace.to_dict()


# ============================================================================
# Dataset Endpoints
# ============================================================================

@app.get("/api/datasets")
async def list_datasets():
    """List all datasets in workspace"""
    datasets = dataset_store.list_all(workspace.id)
    return [d.to_dict() for d in datasets]


@app.get("/api/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    """Get dataset by ID"""
    dataset = dataset_store.load(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset.to_dict()


@app.get("/api/datasets/{dataset_id}/preview")
async def get_dataset_preview(dataset_id: str):
    """Get dataset preview (first 10 rows)"""
    df = dataset_store.get_preview(dataset_id, n_rows=10)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return df.to_dict(orient="records")


@app.get("/api/datasets/{dataset_id}/statistics")
async def get_dataset_statistics(dataset_id: str):
    """Get dataset statistics"""
    stats = dataset_store.get_statistics(dataset_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return stats


@app.post("/api/datasets/import")
async def import_dataset(file: UploadFile = File(...), name: Optional[str] = None):
    """Import CSV dataset"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    # Save uploaded file temporarily
    temp_path = Path(f"/tmp/{file.filename}")
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create dataset
    dataset = Dataset(
        name=name or file.filename,
        workspace_id=workspace.id
    )
    
    # Import into workspace
    dataset = dataset_store.import_csv(temp_path, dataset)
    
    # Clean up temp file
    temp_path.unlink()
    
    return dataset.to_dict()


# ============================================================================
# Experiment Endpoints
# ============================================================================

@app.get("/api/experiments")
async def list_experiments():
    """List all experiments in workspace"""
    experiments = experiment_store.list_all(workspace.id)
    return [e.to_dict() for e in experiments]


@app.get("/api/experiments/{experiment_id}")
async def get_experiment(experiment_id: str):
    """Get experiment by ID"""
    experiment = experiment_store.load(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment.to_dict()


@app.post("/api/experiments")
async def create_experiment(request: CreateExperimentRequest):
    """Create new experiment"""
    # Validate dataset exists
    dataset = dataset_store.load(request.dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create experiment
    experiment = Experiment(
        name=request.name,
        dataset_id=request.dataset_id,
        task_type=TaskType(request.task_type),
        workspace_id=workspace.id
    )
    
    experiment = experiment_store.create(experiment)
    return experiment.to_dict()


@app.put("/api/experiments/{experiment_id}")
async def update_experiment(experiment_id: str, experiment_data: dict):
    """Update experiment (draft pipeline)"""
    experiment = experiment_store.load(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    # Update fields (pipeline config, etc.)
    # For now, just save back
    experiment_store.save(experiment)
    return experiment.to_dict()


# ============================================================================
# Hook Endpoints
# ============================================================================

@app.get("/api/experiments/{experiment_id}/hooks")
async def list_hooks(experiment_id: str):
    """List all hooks for experiment"""
    hooks = experiment_store.list_hooks(experiment_id)
    return [h.to_dict() for h in hooks]


@app.post("/api/experiments/{experiment_id}/hooks")
async def create_hook(experiment_id: str, request: CreateHookRequest):
    """Create hook for experiment"""
    hook = Hook(
        type=HookType(request.hook_type),
        block_id=request.block_id,
        source=HookSource.INLINE,
        code=request.code
    )
    
    experiment_store.save_hook(experiment_id, hook)
    return hook.to_dict()


@app.delete("/api/experiments/{experiment_id}/hooks/{hook_id}")
async def delete_hook(experiment_id: str, hook_id: str):
    """Delete hook"""
    experiment_store.delete_hook(experiment_id, hook_id)
    return {"status": "deleted"}


# ============================================================================
# Run Endpoints
# ============================================================================

@app.get("/api/experiments/{experiment_id}/runs")
async def list_runs(experiment_id: str):
    """List all runs for experiment"""
    runs = run_store.list_by_experiment(experiment_id)
    return [r.to_dict() for r in runs]


@app.get("/api/runs/recent")
async def list_recent_runs(limit: int = 10):
    """List recent runs across all experiments"""
    runs = run_store.list_recent(limit)
    return [r.to_dict() for r in runs]


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str):
    """Get run by ID"""
    run = run_store.load(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run.to_dict()


@app.get("/api/runs/{run_id}/logs")
async def get_run_logs(run_id: str):
    """Get execution logs for run"""
    logs = run_store.get_logs(run_id)
    return {"logs": logs}


@app.get("/api/runs/{run_id}/artifacts")
async def list_run_artifacts(run_id: str):
    """List artifacts for run"""
    artifacts = artifact_store.list_by_run(run_id)
    return [a.to_dict() for a in artifacts]


@app.post("/api/runs")
async def create_and_execute_run(request: CreateRunRequest):
    """Create and execute a new run"""
    # Load experiment and dataset
    experiment = experiment_store.load(request.experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    dataset = dataset_store.load(experiment.dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create run
    run = executor.create_run(experiment, dataset, request.seed)
    
    # Execute in background (non-blocking)
    asyncio.create_task(execute_run_async(run.id))
    
    return run.to_dict()


async def execute_run_async(run_id: str):
    """Execute run asynchronously"""
    run = run_store.load(run_id)
    if run:
        executor.execute_run(run)


# ============================================================================
# WebSocket for real-time updates
# ============================================================================

@app.websocket("/ws/runs/{run_id}")
async def websocket_run_logs(websocket: WebSocket, run_id: str):
    """Stream run logs via WebSocket"""
    await websocket.accept()
    
    try:
        # Send existing logs
        logs = run_store.get_logs(run_id)
        for log in logs:
            await websocket.send_text(log)
        
        # Poll for new logs (simple implementation)
        last_log_count = len(logs)
        
        while True:
            await asyncio.sleep(0.5)  # Poll every 500ms
            
            current_logs = run_store.get_logs(run_id)
            if len(current_logs) > last_log_count:
                # Send new logs
                for log in current_logs[last_log_count:]:
                    await websocket.send_text(log)
                last_log_count = len(current_logs)
            
            # Check if run is complete
            run = run_store.load(run_id)
            if run and run.is_immutable:
                await websocket.send_text("__RUN_COMPLETE__")
                break
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


# ============================================================================
# Health check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "workspace": workspace.name}


# ============================================================================
# Main entry point
# ============================================================================

def start_server(host: str = "127.0.0.1", port: int = 8000):
    """Start the Butterfly backend server"""
    print(f"🦋 Butterfly backend starting on http://{host}:{port}")
    print(f"   Workspace: {workspace.root_path}")
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    start_server()
