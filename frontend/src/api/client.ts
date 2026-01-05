/**
 * Butterfly Frontend - API Client
 * 
 * Handles all communication with the backend.
 */

const API_BASE = '/api';

export interface Dataset {
    id: string;
    name: string;
    row_count: number;
    schema: Record<string, string>;
    content_hash: string;
}

export interface Experiment {
    id: string;
    name: string;
    dataset_id: string;
    task_type: string;
    pipeline: any;
    created_at: string;
}

export interface Run {
    id: string;
    experiment_id: string;
    status: 'created' | 'running' | 'completed' | 'failed';
    seed: number;
    created_at: string;
    started_at?: string;
    completed_at?: string;
    error_message?: string;
}

export interface Artifact {
    id: string;
    type: string;
    run_id: string;
    file_path?: string;
    metadata: any;
}

export interface Hook {
    id: string;
    type: 'before' | 'after' | 'override';
    block_id: string;
    source: 'inline' | 'file';
    code: string;
    code_hash: string;
}

class APIClient {
    // Datasets
    async listDatasets(): Promise<Dataset[]> {
        const response = await fetch(`${API_BASE}/datasets`);
        return response.json();
    }

    async getDataset(id: string): Promise<Dataset> {
        const response = await fetch(`${API_BASE}/datasets/${id}`);
        return response.json();
    }

    async getDatasetPreview(id: string): Promise<any[]> {
        const response = await fetch(`${API_BASE}/datasets/${id}/preview`);
        return response.json();
    }

    async importDataset(file: File, name?: string): Promise<Dataset> {
        const formData = new FormData();
        formData.append('file', file);
        if (name) formData.append('name', name);

        const response = await fetch(`${API_BASE}/datasets/import`, {
            method: 'POST',
            body: formData,
        });
        return response.json();
    }

    // Experiments
    async listExperiments(): Promise<Experiment[]> {
        const response = await fetch(`${API_BASE}/experiments`);
        return response.json();
    }

    async getExperiment(id: string): Promise<Experiment> {
        const response = await fetch(`${API_BASE}/experiments/${id}`);
        return response.json();
    }

    async createExperiment(data: {
        name: string;
        dataset_id: string;
        task_type: string;
    }): Promise<Experiment> {
        const response = await fetch(`${API_BASE}/experiments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        return response.json();
    }

    // Hooks
    async listHooks(experimentId: string): Promise<Hook[]> {
        const response = await fetch(`${API_BASE}/experiments/${experimentId}/hooks`);
        return response.json();
    }

    async createHook(experimentId: string, data: {
        block_id: string;
        hook_type: string;
        code: string;
    }): Promise<Hook> {
        const response = await fetch(`${API_BASE}/experiments/${experimentId}/hooks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        return response.json();
    }

    async deleteHook(experimentId: string, hookId: string): Promise<void> {
        await fetch(`${API_BASE}/experiments/${experimentId}/hooks/${hookId}`, {
            method: 'DELETE',
        });
    }

    // Runs
    async listRuns(experimentId: string): Promise<Run[]> {
        const response = await fetch(`${API_BASE}/experiments/${experimentId}/runs`);
        return response.json();
    }

    async getRun(id: string): Promise<Run> {
        const response = await fetch(`${API_BASE}/runs/${id}`);
        return response.json();
    }

    async createRun(experimentId: string, seed?: number): Promise<Run> {
        const response = await fetch(`${API_BASE}/runs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ experiment_id: experimentId, seed }),
        });
        return response.json();
    }

    async getRunLogs(id: string): Promise<string[]> {
        const response = await fetch(`${API_BASE}/runs/${id}/logs`);
        const data = await response.json();
        return data.logs;
    }

    async getRunArtifacts(id: string): Promise<Artifact[]> {
        const response = await fetch(`${API_BASE}/runs/${id}/artifacts`);
        return response.json();
    }

    // WebSocket for real-time logs
    connectToRunLogs(runId: string, onMessage: (log: string) => void): WebSocket {
        const ws = new WebSocket(`ws://localhost:8000/ws/runs/${runId}`);
        ws.onmessage = (event) => onMessage(event.data);
        return ws;
    }
}

export const apiClient = new APIClient();
