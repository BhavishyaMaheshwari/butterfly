import React, { useEffect, useState } from 'react';
import { Card } from './Card';
import { Badge } from './Badge';
import {
    BarChart3, PieChart, TrendingUp, AlertCircle,
    CheckCircle, Info, Sparkles
} from 'lucide-react';
import './DataInsights.css';

interface DataInsightsProps {
    dataset: {
        id: string;
        name: string;
        row_count: number;
        schema: Record<string, string>;
    };
    preview?: any[];
}

interface ColumnStats {
    name: string;
    type: string;
    missing: number;
    unique: number;
    insights: string[];
}

export const DataInsights: React.FC<DataInsightsProps> = ({ dataset, preview = [] }) => {
    const [columnStats, setColumnStats] = useState<ColumnStats[]>([]);
    const [insights, setInsights] = useState<string[]>([]);

    useEffect(() => {
        analyzeDataset();
    }, [dataset, preview]);

    const analyzeDataset = () => {
        const stats: ColumnStats[] = [];
        const dataInsights: string[] = [];

        // Analyze each column
        Object.entries(dataset.schema).forEach(([colName, colType]) => {
            const columnData = preview.map(row => row[colName]);
            const missing = columnData.filter(v => v === null || v === undefined || v === '').length;
            const unique = new Set(columnData.filter(v => v !== null && v !== undefined)).size;

            const colInsights: string[] = [];

            // Generate insights
            if (missing > preview.length * 0.3) {
                colInsights.push(`High missing values (${Math.round(missing / preview.length * 100)}%)`);
            }

            if (colType === 'object' && unique < 10) {
                colInsights.push(`Categorical with ${unique} categories`);
            }

            if (colType !== 'object' && unique === preview.length) {
                colInsights.push('Potential ID column');
            }

            stats.push({
                name: colName,
                type: colType,
                missing,
                unique,
                insights: colInsights
            });
        });

        // Dataset-level insights
        if (dataset.row_count < 100) {
            dataInsights.push('⚠️ Small dataset - consider collecting more data for better model performance');
        } else if (dataset.row_count > 100000) {
            dataInsights.push('✨ Large dataset - excellent for training robust models');
        }

        const numericCols = Object.values(dataset.schema).filter(t => t !== 'object').length;
        const categoricalCols = Object.values(dataset.schema).filter(t => t === 'object').length;

        if (categoricalCols > numericCols) {
            dataInsights.push('📊 Mostly categorical features - consider one-hot encoding');
        }

        if (numericCols > 10) {
            dataInsights.push('🎯 Many numeric features - feature selection may improve performance');
        }

        setColumnStats(stats);
        setInsights(dataInsights);
    };

    const getTypeColor = (type: string) => {
        return type === 'object' ? 'var(--accent-info)' : 'var(--accent-success)';
    };

    const getTypeIcon = (type: string) => {
        return type === 'object' ? '🔤' : '🔢';
    };

    return (
        <div className="data-insights">
            <div className="data-insights__header">
                <div className="data-insights__title">
                    <Sparkles size={20} className="text-accent" />
                    <h3>Data Insights</h3>
                </div>
                <Badge variant="info" size="sm">
                    {dataset.row_count.toLocaleString()} rows × {Object.keys(dataset.schema).length} columns
                </Badge>
            </div>

            {/* Smart Insights */}
            {insights.length > 0 && (
                <Card variant="glass" className="insights-card">
                    <div className="insights-card__header">
                        <Info size={16} />
                        <h4>Smart Recommendations</h4>
                    </div>
                    <ul className="insights-list">
                        {insights.map((insight, idx) => (
                            <li key={idx} className="insight-item">
                                {insight}
                            </li>
                        ))}
                    </ul>
                </Card>
            )}

            {/* Dataset Overview */}
            <div className="stats-grid">
                <Card className="stat-card">
                    <div className="stat-card__icon" style={{ backgroundColor: 'var(--accent-primary-bg)' }}>
                        <BarChart3 size={20} style={{ color: 'var(--accent-primary)' }} />
                    </div>
                    <div className="stat-card__content">
                        <span className="stat-card__label">Total Rows</span>
                        <span className="stat-card__value">{dataset.row_count.toLocaleString()}</span>
                    </div>
                </Card>

                <Card className="stat-card">
                    <div className="stat-card__icon" style={{ backgroundColor: 'var(--accent-success-bg)' }}>
                        <PieChart size={20} style={{ color: 'var(--accent-success)' }} />
                    </div>
                    <div className="stat-card__content">
                        <span className="stat-card__label">Features</span>
                        <span className="stat-card__value">{Object.keys(dataset.schema).length}</span>
                    </div>
                </Card>

                <Card className="stat-card">
                    <div className="stat-card__icon" style={{ backgroundColor: 'var(--accent-info-bg)' }}>
                        <TrendingUp size={20} style={{ color: 'var(--accent-info)' }} />
                    </div>
                    <div className="stat-card__content">
                        <span className="stat-card__label">Data Quality</span>
                        <span className="stat-card__value">
                            {Math.round((1 - columnStats.reduce((sum, col) => sum + col.missing, 0) / (preview.length * columnStats.length)) * 100)}%
                        </span>
                    </div>
                </Card>
            </div>

            {/* Column Details */}
            <Card className="columns-card">
                <h4>Column Analysis</h4>
                <div className="columns-table">
                    <div className="columns-table__header">
                        <span>Column</span>
                        <span>Type</span>
                        <span>Unique</span>
                        <span>Missing</span>
                        <span>Insights</span>
                    </div>
                    {columnStats.map((col, idx) => (
                        <div key={idx} className="columns-table__row">
                            <span className="column-name">
                                <span className="column-icon">{getTypeIcon(col.type)}</span>
                                {col.name}
                            </span>
                            <Badge
                                variant="default"
                                size="sm"
                                style={{ borderColor: getTypeColor(col.type) }}
                            >
                                {col.type}
                            </Badge>
                            <span className="text-secondary">{col.unique}</span>
                            <span className={col.missing > 0 ? 'text-warning' : 'text-success'}>
                                {col.missing > 0 ? (
                                    <>
                                        <AlertCircle size={12} className="inline-icon" />
                                        {col.missing}
                                    </>
                                ) : (
                                    <>
                                        <CheckCircle size={12} className="inline-icon" />
                                        0
                                    </>
                                )}
                            </span>
                            <span className="column-insights">
                                {col.insights.length > 0 ? (
                                    <span className="text-tertiary text-sm">{col.insights[0]}</span>
                                ) : (
                                    <span className="text-tertiary text-sm">—</span>
                                )}
                            </span>
                        </div>
                    ))}
                </div>
            </Card>
        </div>
    );
};
