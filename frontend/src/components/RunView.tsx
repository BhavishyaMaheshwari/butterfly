import React, { useEffect, useRef, useState } from 'react';
import { Card } from './Card';
import { Button } from './Button';
import { Badge } from './Badge';
import { CheckCircle2, XCircle, Clock, Download, Copy, ChevronsDown, ChevronsUp } from 'lucide-react';
import './RunView.css';

interface RunViewProps {
    run: {
        id: string;
        status: 'created' | 'running' | 'completed' | 'failed';
        error_message?: string;
    };
    logs: string[];
}

export const RunView: React.FC<RunViewProps> = ({ run, logs }) => {
    const logsEndRef = useRef<HTMLDivElement>(null);
    const logsContainerRef = useRef<HTMLDivElement>(null);
    const [autoScroll, setAutoScroll] = useState(true);
    const [showScrollButtons, setShowScrollButtons] = useState(false);

    // Auto-scroll to bottom when new logs arrive
    useEffect(() => {
        if (autoScroll && logsEndRef.current) {
            logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [logs, autoScroll]);

    // Check if scroll buttons should be shown
    useEffect(() => {
        const container = logsContainerRef.current;
        if (container) {
            const hasScroll = container.scrollHeight > container.clientHeight;
            setShowScrollButtons(hasScroll);
        }
    }, [logs]);

    const statusIcon = run.status === 'completed'
        ? <CheckCircle2 size={24} className="text-success" />
        : run.status === 'failed'
            ? <XCircle size={24} className="text-error" />
            : <Clock size={24} className="text-warning animate-pulse" />;

    const getRunStatusVariant = (status: string): 'default' | 'success' | 'warning' | 'error' => {
        switch (status) {
            case 'completed': return 'success';
            case 'running': return 'warning';
            case 'failed': return 'error';
            default: return 'default';
        }
    };

    const handleDownloadLogs = () => {
        const logsText = logs.join('');
        const blob = new Blob([logsText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `butterfly-run-${run.id.substring(0, 8)}-logs.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleCopyLogs = async () => {
        const logsText = logs.join('');
        try {
            await navigator.clipboard.writeText(logsText);
            alert('Logs copied to clipboard!');
        } catch (error) {
            console.error('Failed to copy logs:', error);
        }
    };

    const scrollToTop = () => {
        logsContainerRef.current?.scrollTo({ top: 0, behavior: 'smooth' });
        setAutoScroll(false);
    };

    const scrollToBottom = () => {
        logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        setAutoScroll(true);
    };

    const handleDownloadModel = () => {
        // Download model file
        const a = document.createElement('a');
        a.href = `/api/runs/${run.id}/artifacts/model.pkl`;
        a.download = `butterfly-model-${run.id.substring(0, 8)}.pkl`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    const handleDownloadMetrics = () => {
        // Download metrics as JSON
        fetch(`/api/runs/${run.id}/artifacts/metrics.json`)
            .then(res => res.json())
            .then(metrics => {
                const blob = new Blob([JSON.stringify(metrics, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `butterfly-metrics-${run.id.substring(0, 8)}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            })
            .catch(err => console.error('Failed to download metrics:', err));
    };

    return (
        <div className="run-view">
            <div className="run-view__header">
                <div className="run-view__title">
                    {statusIcon}
                    <div>
                        <h2>Run {run.id.substring(0, 8)}</h2>
                        <Badge variant={getRunStatusVariant(run.status)}>
                            {run.status}
                        </Badge>
                    </div>
                </div>

                {run.status === 'completed' && (
                    <div className="run-view__actions">
                        <Button
                            variant="secondary"
                            size="sm"
                            icon={<Download size={16} />}
                            onClick={handleDownloadModel}
                        >
                            Download Model
                        </Button>
                        <Button
                            variant="secondary"
                            size="sm"
                            icon={<Download size={16} />}
                            onClick={handleDownloadMetrics}
                        >
                            Download Metrics
                        </Button>
                    </div>
                )}
            </div>

            <Card className="logs-card">
                <div className="logs-card__header">
                    <h3>Execution Logs</h3>
                    <div className="logs-card__actions">
                        <Button
                            variant="ghost"
                            size="sm"
                            icon={<Copy size={14} />}
                            onClick={handleCopyLogs}
                        >
                            Copy
                        </Button>
                        <Button
                            variant="ghost"
                            size="sm"
                            icon={<Download size={14} />}
                            onClick={handleDownloadLogs}
                        >
                            Download
                        </Button>
                    </div>
                </div>

                <div className="logs-container" ref={logsContainerRef}>
                    <pre className="logs-content">
                        {logs.length === 0 ? (
                            <span className="logs-loading">
                                <Clock size={16} className="animate-pulse" />
                                Waiting for execution to start...
                            </span>
                        ) : (
                            logs.join('')
                        )}
                        <div ref={logsEndRef} />
                    </pre>

                    {showScrollButtons && (
                        <div className="logs-scroll-buttons">
                            <button
                                className="logs-scroll-btn"
                                onClick={scrollToTop}
                                title="Scroll to top"
                            >
                                <ChevronsUp size={16} />
                            </button>
                            <button
                                className={`logs-scroll-btn ${autoScroll ? 'active' : ''}`}
                                onClick={scrollToBottom}
                                title="Scroll to bottom (auto-scroll)"
                            >
                                <ChevronsDown size={16} />
                            </button>
                        </div>
                    )}
                </div>
            </Card>

            {run.status === 'completed' && (
                <Card variant="elevated" className="status-card status-card--success">
                    <CheckCircle2 size={20} />
                    <div>
                        <h4>Run Completed Successfully</h4>
                        <p className="text-secondary">
                            The experiment has completed. Download the model and metrics above, or check the logs for details.
                        </p>
                    </div>
                </Card>
            )}

            {run.status === 'failed' && (
                <Card variant="elevated" className="status-card status-card--error">
                    <XCircle size={20} />
                    <div>
                        <h4>Run Failed</h4>
                        <p className="text-secondary">
                            {run.error_message || 'An error occurred during execution. Check the logs above for details.'}
                        </p>
                    </div>
                </Card>
            )}

            {run.status === 'running' && (
                <Card variant="elevated" className="status-card status-card--running">
                    <Clock size={20} className="animate-pulse" />
                    <div>
                        <h4>Execution in Progress</h4>
                        <p className="text-secondary">
                            Your pipeline is currently executing. Logs will stream in real-time above.
                        </p>
                    </div>
                </Card>
            )}
        </div>
    );
};
