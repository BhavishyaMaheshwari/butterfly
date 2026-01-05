import React from 'react';
import { DataInsights } from './DataInsights';
import { DataVisualization } from './DataVisualization';
import { ModelConfigPanel } from './ModelConfigPanel';
import { Button } from './Button';
import { Card } from './Card';
import { ArrowLeft, Play, Download } from 'lucide-react';
import './DatasetDetailView.css';

interface DatasetDetailViewProps {
    dataset: {
        id: string;
        name: string;
        row_count: number;
        schema: Record<string, string>;
    };
    preview: any[];
    onBack: () => void;
    onCreateExperiment: (datasetId: string) => void;
}

export const DatasetDetailView: React.FC<DatasetDetailViewProps> = ({
    dataset,
    preview,
    onBack,
    onCreateExperiment
}) => {
    const handleDownloadCSV = () => {
        // Create CSV from preview data
        if (preview.length === 0) return;

        const headers = Object.keys(preview[0]);
        const csvContent = [
            headers.join(','),
            ...preview.map(row => headers.map(h => row[h]).join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${dataset.name}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="dataset-detail-view">
            <div className="dataset-detail-view__header">
                <Button
                    variant="ghost"
                    icon={<ArrowLeft size={16} />}
                    onClick={onBack}
                >
                    Back to Workspace
                </Button>

                <div className="dataset-detail-view__actions">
                    <Button
                        variant="secondary"
                        icon={<Download size={16} />}
                        onClick={handleDownloadCSV}
                    >
                        Download CSV
                    </Button>
                    <Button
                        variant="primary"
                        icon={<Play size={16} />}
                        onClick={() => onCreateExperiment(dataset.id)}
                    >
                        Create Experiment
                    </Button>
                </div>
            </div>

            <div className="dataset-detail-view__title">
                <h2>{dataset.name}</h2>
                <p className="text-secondary">Explore your dataset with AI-powered insights</p>
            </div>

            {/* Data Insights Component */}
            <DataInsights dataset={dataset} preview={preview} />

            {/* Data Visualizations */}
            <DataVisualization data={preview} schema={dataset.schema} />

            {/* Model Configuration Panel */}
            <ModelConfigPanel />

            {/* Data Preview */}
            <Card className="data-preview-card">
                <h4>Data Preview (First 10 rows)</h4>
                <div className="data-preview-table-container">
                    <table className="data-preview-table">
                        <thead>
                            <tr>
                                {Object.keys(dataset.schema).map(col => (
                                    <th key={col}>{col}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {preview.slice(0, 10).map((row, idx) => (
                                <tr key={idx}>
                                    {Object.keys(dataset.schema).map(col => (
                                        <td key={col}>{row[col]?.toString() || '—'}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    );
};
