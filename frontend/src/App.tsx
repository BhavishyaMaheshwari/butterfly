/**
 * Butterfly Frontend - Main Application
 * Beautiful, visual, pipeline-first ML application
 */
import { useState, useEffect } from 'react';
import { apiClient, Dataset, Experiment, Run } from './api/client';
import { PipelineCanvas } from './components/PipelineCanvas';
import { RunView } from './components/RunView';
import { DatasetDetailView } from './components/DatasetDetailView';
import { Card } from './components/Card';
import { Button } from './components/Button';
import { Badge } from './components/Badge';
import {
    Database, Folder, Play, Upload, ChevronRight, Clock
} from 'lucide-react';
import './App.css';

function App() {
    const [view, setView] = useState<'home' | 'experiment' | 'run' | 'dataset'>('home');
    const [datasets, setDatasets] = useState<Dataset[]>([]);
    const [experiments, setExperiments] = useState<Experiment[]>([]);
    const [currentExperiment, setCurrentExperiment] = useState<Experiment | null>(null);
    const [currentDataset, setCurrentDataset] = useState<Dataset | null>(null);
    const [datasetPreview, setDatasetPreview] = useState<any[]>([]);
    const [currentRun, setCurrentRun] = useState<Run | null>(null);
    const [runs, setRuns] = useState<Run[]>([]);
    const [logs, setLogs] = useState<string[]>([]);

    // Load initial data
    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        const [datasetsData, experimentsData] = await Promise.all([
            apiClient.listDatasets(),
            apiClient.listExperiments(),
        ]);
        setDatasets(datasetsData);
        setExperiments(experimentsData);
    };

    // Dataset import
    const handleImportDataset = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        try {
            await apiClient.importDataset(file);
            await loadData();
        } catch (error) {
            console.error('Failed to import dataset:', error);
        }
    };

    // Create experiment
    const handleCreateExperiment = async (datasetId: string) => {
        const name = prompt('Experiment name:');
        if (!name) return;

        try {
            const experiment = await apiClient.createExperiment({
                name,
                dataset_id: datasetId,
                task_type: 'auto_detect',
            });
            setCurrentExperiment(experiment);
            setView('experiment');
            await loadData();
        } catch (error) {
            console.error('Failed to create experiment:', error);
        }
    };

    // Run experiment
    const handleRunExperiment = async () => {
        if (!currentExperiment) return;

        try {
            const run = await apiClient.createRun(currentExperiment.id);
            setCurrentRun(run);
            setLogs([]);
            // Stay on experiment view to show live pipeline updates

            // Connect to WebSocket for real-time logs
            const ws = apiClient.connectToRunLogs(run.id, (log) => {
                if (log === '__RUN_COMPLETE__') {
                    apiClient.getRun(run.id).then(setCurrentRun);
                } else {
                    setLogs((prev) => [...prev, log]);
                }
            });

            return () => ws.close();
        } catch (error) {
            console.error('Failed to start run:', error);
            alert('Failed to start run. Please check the console for details.');
        }
    };

    // View dataset details
    const handleViewDataset = async (dataset: Dataset) => {
        setCurrentDataset(dataset);
        const preview = await apiClient.getDatasetPreview(dataset.id);
        setDatasetPreview(preview);
        setView('dataset');
    };

    // Load experiment details
    const handleViewExperiment = async (experiment: Experiment) => {
        setCurrentExperiment(experiment);
        const runsData = await apiClient.listRuns(experiment.id);
        setRuns(runsData);
        setView('experiment');
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="app-header__brand">
                    <h1>🦋 Butterfly</h1>
                    <p className="text-tertiary">Local-First Visual ML</p>
                </div>
                <nav className="app-header__nav">
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setView('home')}
                    >
                        Workspace
                    </Button>
                </nav>
            </header>

            {/* Main Content */}
            <main className="app-main">
                {view === 'home' && (
                    <HomeView
                        datasets={datasets}
                        experiments={experiments}
                        onImportDataset={handleImportDataset}
                        onCreateExperiment={handleCreateExperiment}
                        onViewExperiment={handleViewExperiment}
                        onViewDataset={handleViewDataset}
                    />
                )}

                {view === 'dataset' && currentDataset && (
                    <DatasetDetailView
                        dataset={currentDataset}
                        preview={datasetPreview}
                        onBack={() => setView('home')}
                        onCreateExperiment={handleCreateExperiment}
                    />
                )}

                {view === 'experiment' && currentExperiment && (
                    <ExperimentView
                        experiment={currentExperiment}
                        runs={runs}
                        currentRun={currentRun}
                        logs={logs}
                        onRunExperiment={handleRunExperiment}
                        onViewRun={(run) => {
                            setCurrentRun(run);
                            setView('run');
                        }}
                    />
                )}

                {view === 'run' && currentRun && (
                    <RunView run={currentRun} logs={logs} />
                )}
            </main>
        </div>
    );
}

// Home View - Workspace
function HomeView({
    datasets,
    experiments,
    onImportDataset,
    onCreateExperiment,
    onViewExperiment,
    onViewDataset
}: {
    datasets: Dataset[];
    experiments: Experiment[];
    onImportDataset: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onCreateExperiment: (datasetId: string) => void;
    onViewExperiment: (experiment: Experiment) => void;
    onViewDataset: (dataset: Dataset) => void;
}) {
    return (
        <div className="workspace">
            <div className="workspace__header">
                <h2>Workspace</h2>
                <p className="text-secondary">Manage your datasets and experiments</p>
            </div>

            {/* Datasets Section */}
            <section className="workspace__section">
                <div className="section-header">
                    <div className="section-header__title">
                        <Database size={20} />
                        <h3>Datasets</h3>
                        <Badge variant="default" size="sm">{datasets.length}</Badge>
                    </div>
                    <label className="upload-btn">
                        <Upload size={16} />
                        <span>Import CSV</span>
                        <input
                            type="file"
                            accept=".csv"
                            onChange={onImportDataset}
                            style={{ display: 'none' }}
                        />
                    </label>
                </div>

                {datasets.length === 0 ? (
                    <Card className="empty-state">
                        <Database size={48} className="empty-state__icon" />
                        <h4>No datasets yet</h4>
                        <p className="text-secondary">Import a CSV file to get started</p>
                    </Card>
                ) : (
                    <div className="grid">
                        {datasets.map((dataset) => (
                            <Card
                                key={dataset.id}
                                hoverable
                                className="dataset-card"
                                onClick={() => onViewDataset(dataset)}
                            >
                                <div className="dataset-card__header">
                                    <Database size={20} />
                                    <h4>{dataset.name}</h4>
                                </div>
                                <div className="dataset-card__stats">
                                    <span className="text-secondary">
                                        {dataset.row_count} rows • {Object.keys(dataset.schema).length} columns
                                    </span>
                                </div>
                                <Button
                                    variant="primary"
                                    size="sm"
                                    onClick={(e) => {
                                        e?.stopPropagation();
                                        onCreateExperiment(dataset.id);
                                    }}
                                    icon={<Play size={14} />}
                                >
                                    Create Experiment
                                </Button>
                            </Card>
                        ))}
                    </div>
                )}
            </section>

            {/* Experiments Section */}
            <section className="workspace__section">
                <div className="section-header">
                    <div className="section-header__title">
                        <Folder size={20} />
                        <h3>Experiments</h3>
                        <Badge variant="default" size="sm">{experiments.length}</Badge>
                    </div>
                </div>

                {experiments.length === 0 ? (
                    <Card className="empty-state">
                        <Folder size={48} className="empty-state__icon" />
                        <h4>No experiments yet</h4>
                        <p className="text-secondary">Create an experiment from a dataset</p>
                    </Card>
                ) : (
                    <div className="grid">
                        {experiments.map((experiment) => (
                            <Card
                                key={experiment.id}
                                hoverable
                                onClick={() => onViewExperiment(experiment)}
                                className="experiment-card"
                            >
                                <div className="experiment-card__header">
                                    <Folder size={20} />
                                    <h4>{experiment.name}</h4>
                                </div>
                                <p className="text-secondary">Task: {experiment.task_type}</p>
                                <div className="experiment-card__footer">
                                    <span className="text-tertiary">View details</span>
                                    <ChevronRight size={16} />
                                </div>
                            </Card>
                        ))}
                    </div>
                )}
            </section>
        </div>
    );
}

// Experiment View - Pipeline Canvas
function ExperimentView({
    experiment,
    runs,
    currentRun,
    logs,
    onRunExperiment,
    onViewRun,
}: {
    experiment: Experiment;
    runs: Run[];
    currentRun: Run | null;
    logs: string[];
    onRunExperiment: () => void;
    onViewRun: (run: Run) => void;
}) {
    return (
        <div className="experiment-view">
            <div className="experiment-view__header">
                <div>
                    <h2>{experiment.name}</h2>
                    <p className="text-secondary">Task: {experiment.task_type}</p>
                </div>
                <Button
                    variant="primary"
                    icon={<Play size={18} />}
                    onClick={onRunExperiment}
                >
                    Run Experiment
                </Button>
            </div>

            {/* Visual Pipeline Canvas */}
            <PipelineCanvas experimentId={experiment.id} currentRun={currentRun} />

            {/* Live Execution Logs */}
            {currentRun && currentRun.status === 'running' && (
                <Card className="live-logs-card">
                    <h3>Live Execution</h3>
                    <div className="live-logs-container">
                        <pre className="live-logs-content">
                            {logs.length === 0 ? 'Waiting for execution to start...' : logs.join('')}
                        </pre>
                    </div>
                </Card>
            )}

            {/* Recent Runs */}
            {runs.length > 0 && (
                <section className="runs-section">
                    <h3>Recent Runs</h3>
                    <div className="runs-list">
                        {runs.map((run) => (
                            <Card
                                key={run.id}
                                hoverable
                                onClick={() => onViewRun(run)}
                                className="run-card"
                            >
                                <div className="run-card__header">
                                    <div className="run-card__info">
                                        <Clock size={16} />
                                        <span>Run {run.id.substring(0, 8)}</span>
                                    </div>
                                    <Badge variant={getRunStatusVariant(run.status)} size="sm">
                                        {run.status}
                                    </Badge>
                                </div>
                                <ChevronRight size={16} className="run-card__arrow" />
                            </Card>
                        ))}
                    </div>
                </section>
            )}
        </div>
    );
}

// Helper function
function getRunStatusVariant(status: string): 'default' | 'success' | 'warning' | 'error' {
    switch (status) {
        case 'completed': return 'success';
        case 'running': return 'warning';
        case 'failed': return 'error';
        default: return 'default';
    }
}

export default App;
