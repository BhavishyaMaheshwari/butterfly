import React, { useState, useEffect } from 'react';
import { Card } from './Card';
import { Badge } from './Badge';
import { HookModal } from './HookModal';
import { apiClient, Hook } from '../api/client';
import {
    Database, Target, Sliders, Sparkles, Brain,
    Settings, Play, BarChart3, Eye, Package,
    ChevronDown, ChevronUp, Code, Trash2
} from 'lucide-react';
import './PipelineCanvas.css';

interface PipelineBlock {
    id: string;
    name: string;
    status: 'idle' | 'running' | 'completed' | 'failed';
    icon: React.ReactNode;
    description?: string;
}

const PIPELINE_BLOCKS: PipelineBlock[] = [
    { id: 'data_ingestion', name: 'Data Ingestion', status: 'idle', icon: <Database size={20} />, description: 'Load and validate dataset' },
    { id: 'task_resolution', name: 'Task Resolution', status: 'idle', icon: <Target size={20} />, description: 'Detect classification vs regression' },
    { id: 'preprocessing', name: 'Preprocessing', status: 'idle', icon: <Sliders size={20} />, description: 'Clean, encode, and scale data' },
    { id: 'feature_engineering', name: 'Feature Engineering', status: 'idle', icon: <Sparkles size={20} />, description: 'Create and select features' },
    { id: 'model_selection', name: 'Model Selection', status: 'idle', icon: <Brain size={20} />, description: 'Choose candidate models' },
    { id: 'hyperparameter_tuning', name: 'Hyperparameter Tuning', status: 'idle', icon: <Settings size={20} />, description: 'Optimize model parameters' },
    { id: 'training', name: 'Training', status: 'idle', icon: <Play size={20} />, description: 'Train selected models' },
    { id: 'evaluation', name: 'Evaluation', status: 'idle', icon: <BarChart3 size={20} />, description: 'Measure model performance' },
    { id: 'explainability', name: 'Explainability', status: 'idle', icon: <Eye size={20} />, description: 'Generate SHAP values' },
    { id: 'output_packaging', name: 'Output Packaging', status: 'idle', icon: <Package size={20} />, description: 'Export model and artifacts' }
];

interface PipelineCanvasProps {
    blocks?: PipelineBlock[];
    experimentId?: string;
    currentRun?: {
        id: string;
        status: 'created' | 'running' | 'completed' | 'failed';
    } | null;
}

export const PipelineCanvas: React.FC<PipelineCanvasProps> = ({
    blocks = PIPELINE_BLOCKS,
    experimentId,
    currentRun
}) => {
    const [expandedBlocks, setExpandedBlocks] = useState<Set<string>>(new Set());
    const [hookModalOpen, setHookModalOpen] = useState(false);
    const [selectedBlock, setSelectedBlock] = useState<PipelineBlock | null>(null);
    const [hooks, setHooks] = useState<Hook[]>([]);
    const [blockStatuses, setBlockStatuses] = useState<Record<string, 'idle' | 'running' | 'completed' | 'failed'>>({});

    // Update block statuses based on current run
    useEffect(() => {
        if (currentRun) {
            if (currentRun.status === 'running') {
                // Mark all blocks as idle initially, then update based on progress
                // In a real implementation, you'd parse logs or get status from backend
                // For now, we'll simulate by marking first few as completed
                const newStatuses: Record<string, 'idle' | 'running' | 'completed' | 'failed'> = {};
                blocks.forEach((block, idx) => {
                    if (idx < 3) newStatuses[block.id] = 'completed';
                    else if (idx === 3) newStatuses[block.id] = 'running';
                    else newStatuses[block.id] = 'idle';
                });
                setBlockStatuses(newStatuses);
            } else if (currentRun.status === 'completed') {
                // Mark all blocks as completed
                const newStatuses: Record<string, 'idle' | 'running' | 'completed' | 'failed'> = {};
                blocks.forEach(block => {
                    newStatuses[block.id] = 'completed';
                });
                setBlockStatuses(newStatuses);
            } else if (currentRun.status === 'failed') {
                // Mark some as completed, last one as failed
                const newStatuses: Record<string, 'idle' | 'running' | 'completed' | 'failed'> = {};
                blocks.forEach((block, idx) => {
                    if (idx < blocks.length - 1) newStatuses[block.id] = 'completed';
                    else newStatuses[block.id] = 'failed';
                });
                setBlockStatuses(newStatuses);
            }
        } else {
            // No run, all idle
            setBlockStatuses({});
        }
    }, [currentRun, blocks]);

    // Load hooks when experiment changes
    useEffect(() => {
        if (experimentId) {
            loadHooks();
        }
    }, [experimentId]);

    const loadHooks = async () => {
        if (!experimentId) return;
        try {
            const loadedHooks = await apiClient.listHooks(experimentId);
            setHooks(loadedHooks);
        } catch (error) {
            console.error('Failed to load hooks:', error);
        }
    };

    const toggleBlock = (blockId: string) => {
        const newExpanded = new Set(expandedBlocks);
        if (newExpanded.has(blockId)) {
            newExpanded.delete(blockId);
        } else {
            newExpanded.add(blockId);
        }
        setExpandedBlocks(newExpanded);
    };

    const handleAddHook = (block: PipelineBlock) => {
        setSelectedBlock(block);
        setHookModalOpen(true);
    };

    const handleSaveHook = async (hookData: { type: string; code: string }) => {
        if (!experimentId || !selectedBlock) return;

        try {
            await apiClient.createHook(experimentId, {
                block_id: selectedBlock.id,
                hook_type: hookData.type,
                code: hookData.code
            });

            // Reload hooks
            await loadHooks();

            // Expand the block to show the new hook
            setExpandedBlocks(prev => new Set(prev).add(selectedBlock.id));
        } catch (error) {
            console.error('Failed to create hook:', error);
            alert('Failed to create hook. Please try again.');
        }
    };

    const handleDeleteHook = async (hookId: string) => {
        if (!experimentId) return;

        if (!confirm('Are you sure you want to delete this hook?')) return;

        try {
            await apiClient.deleteHook(experimentId, hookId);
            await loadHooks();
        } catch (error) {
            console.error('Failed to delete hook:', error);
            alert('Failed to delete hook. Please try again.');
        }
    };

    const getBlockHooks = (blockId: string): Hook[] => {
        return hooks.filter(h => h.block_id === blockId);
    };

    const getStatusVariant = (status: string): 'default' | 'success' | 'warning' | 'error' => {
        switch (status) {
            case 'completed': return 'success';
            case 'running': return 'warning';
            case 'failed': return 'error';
            default: return 'default';
        }
    };

    const getHookTypeColor = (type: string): string => {
        switch (type) {
            case 'before': return 'var(--accent-info)';
            case 'after': return 'var(--accent-success)';
            case 'override': return 'var(--accent-warning)';
            default: return 'var(--text-secondary)';
        }
    };

    return (
        <>
            <div className="pipeline-canvas">
                <div className="pipeline-canvas__header">
                    <h2>ML Pipeline</h2>
                    <p className="text-secondary">Visual representation of your machine learning workflow</p>
                </div>

                <div className="pipeline-canvas__blocks">
                    {blocks.map((block, index) => {
                        const isExpanded = expandedBlocks.has(block.id);
                        const blockHooks = getBlockHooks(block.id);
                        const currentStatus = blockStatuses[block.id] || block.status;

                        return (
                            <React.Fragment key={block.id}>
                                <div className="pipeline-block-wrapper">
                                    <Card
                                        className={`pipeline-block pipeline-block--${currentStatus}`}
                                        hoverable
                                    >
                                        <div className="pipeline-block__header">
                                            <div className="pipeline-block__info">
                                                <div className="pipeline-block__icon">
                                                    {block.icon}
                                                </div>
                                                <div className="pipeline-block__title">
                                                    <h4>{block.name}</h4>
                                                    {block.description && (
                                                        <p className="text-tertiary">{block.description}</p>
                                                    )}
                                                </div>
                                            </div>

                                            <div className="pipeline-block__actions">
                                                <Badge variant={getStatusVariant(currentStatus)} size="sm">
                                                    {currentStatus}
                                                </Badge>

                                                {blockHooks.length > 0 && (
                                                    <Badge variant="info" size="sm">
                                                        {blockHooks.length} hook{blockHooks.length > 1 ? 's' : ''}
                                                    </Badge>
                                                )}

                                                <button
                                                    className="pipeline-block__expand-btn"
                                                    onClick={() => toggleBlock(block.id)}
                                                    aria-label={isExpanded ? 'Collapse' : 'Expand'}
                                                >
                                                    {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                                                </button>
                                            </div>
                                        </div>

                                        {isExpanded && (
                                            <div className="pipeline-block__details animate-fadeIn">
                                                <div className="pipeline-block__code-section">
                                                    <div className="pipeline-block__code-header">
                                                        <Code size={14} />
                                                        <span>Custom Hooks</span>
                                                    </div>

                                                    {blockHooks.length === 0 ? (
                                                        <div className="pipeline-block__code-placeholder">
                                                            <p className="text-tertiary">No custom hooks added</p>
                                                            <button
                                                                className="pipeline-block__add-code-btn"
                                                                onClick={() => handleAddHook(block)}
                                                            >
                                                                + Add Hook
                                                            </button>
                                                        </div>
                                                    ) : (
                                                        <div className="pipeline-block__hooks-list">
                                                            {blockHooks.map(hook => (
                                                                <div key={hook.id} className="hook-item">
                                                                    <div className="hook-item__header">
                                                                        <Badge
                                                                            variant="default"
                                                                            size="sm"
                                                                            style={{ borderColor: getHookTypeColor(hook.type) }}
                                                                        >
                                                                            {hook.type}
                                                                        </Badge>
                                                                        <button
                                                                            className="hook-item__delete"
                                                                            onClick={() => handleDeleteHook(hook.id)}
                                                                            title="Delete hook"
                                                                        >
                                                                            <Trash2 size={14} />
                                                                        </button>
                                                                    </div>
                                                                    <pre className="hook-item__code">
                                                                        {hook.code.substring(0, 100)}...
                                                                    </pre>
                                                                </div>
                                                            ))}
                                                            <button
                                                                className="pipeline-block__add-code-btn"
                                                                onClick={() => handleAddHook(block)}
                                                            >
                                                                + Add Another Hook
                                                            </button>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        )}
                                    </Card>
                                </div>

                                {index < blocks.length - 1 && (
                                    <div className="pipeline-connector">
                                        <div className="pipeline-connector__line"></div>
                                        <div className="pipeline-connector__arrow"></div>
                                    </div>
                                )}
                            </React.Fragment>
                        );
                    })}
                </div>
            </div>

            {selectedBlock && (
                <HookModal
                    isOpen={hookModalOpen}
                    onClose={() => setHookModalOpen(false)}
                    onSave={handleSaveHook}
                    blockId={selectedBlock.id}
                    blockName={selectedBlock.name}
                />
            )}
        </>
    );
};
