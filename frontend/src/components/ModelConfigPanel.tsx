import React, { useState } from 'react';
import { Card } from './Card';
import { Button } from './Button';
import { Badge } from './Badge';
import { ChevronDown, ChevronUp, Sparkles, Code, Settings } from 'lucide-react';
import './ModelConfigPanel.css';

interface ModelConfig {
    mode: 'auto' | 'manual';
    model_type: string;
    test_size: number;
    random_state: number;
    max_iter: number;
    learning_rate: number;
    n_estimators: number;
    max_depth: number;
    feature_selection: boolean;
    scaling: boolean;
    pca: boolean;
    pca_components: number;
}

interface ModelConfigPanelProps {
    onConfigChange?: (config: ModelConfig) => void;
}

export const ModelConfigPanel: React.FC<ModelConfigPanelProps> = ({ onConfigChange }) => {
    const [expanded, setExpanded] = useState(true);
    const [showCode, setShowCode] = useState(false);

    const [config, setConfig] = useState<ModelConfig>({
        mode: 'auto',
        model_type: 'classification',
        test_size: 0.2,
        random_state: 42,
        max_iter: 1000,
        learning_rate: 0.01,
        n_estimators: 100,
        max_depth: 5,
        feature_selection: true,
        scaling: true,
        pca: false,
        pca_components: 10
    });

    const updateConfig = (key: keyof ModelConfig, value: any) => {
        const newConfig = { ...config, [key]: value };
        setConfig(newConfig);
        onConfigChange?.(newConfig);
    };

    const generatePythonCode = () => {
        return `# Butterfly ML Configuration
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
${config.mode === 'auto' ? 'from autosklearn.classification import AutoSklearnClassifier' : 'from sklearn.ensemble import RandomForestClassifier'}

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=${config.test_size}, 
    random_state=${config.random_state}
)

${config.scaling ? `# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
` : ''}
${config.pca ? `# PCA Dimensionality Reduction
pca = PCA(n_components=${config.pca_components})
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
` : ''}
# Model Training
${config.mode === 'auto'
                ? `model = AutoSklearnClassifier(
    time_left_for_this_task=300,
    per_run_time_limit=30
)`
                : `model = RandomForestClassifier(
    n_estimators=${config.n_estimators},
    max_depth=${config.max_depth},
    random_state=${config.random_state}
)`}

model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(f"Model Accuracy: {score:.4f}")`;
    };

    return (
        <Card className="model-config-panel">
            <div className="model-config-panel__header" onClick={() => setExpanded(!expanded)}>
                <div className="model-config-panel__title">
                    <Settings size={20} />
                    <h3>Model Configuration</h3>
                    <Badge variant="info" size="sm">
                        {config.mode === 'auto' ? 'AutoML' : 'Manual'}
                    </Badge>
                </div>
                <button className="model-config-panel__toggle">
                    {expanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </button>
            </div>

            {expanded && (
                <div className="model-config-panel__content">
                    {/* Mode Toggle */}
                    <div className="config-section">
                        <label className="config-label">Training Mode</label>
                        <div className="toggle-group">
                            <button
                                className={`toggle-btn ${config.mode === 'auto' ? 'active' : ''}`}
                                onClick={() => updateConfig('mode', 'auto')}
                            >
                                <Sparkles size={16} />
                                AutoML
                            </button>
                            <button
                                className={`toggle-btn ${config.mode === 'manual' ? 'active' : ''}`}
                                onClick={() => updateConfig('mode', 'manual')}
                            >
                                <Settings size={16} />
                                Manual
                            </button>
                        </div>
                    </div>

                    {/* Test Size Slider */}
                    <div className="config-section">
                        <label className="config-label">
                            Test Size: <span className="config-value">{(config.test_size * 100).toFixed(0)}%</span>
                        </label>
                        <input
                            type="range"
                            min="0.1"
                            max="0.4"
                            step="0.05"
                            value={config.test_size}
                            onChange={(e) => updateConfig('test_size', parseFloat(e.target.value))}
                            className="slider"
                        />
                        <div className="slider-labels">
                            <span>10%</span>
                            <span>40%</span>
                        </div>
                    </div>

                    {/* Random State */}
                    <div className="config-section">
                        <label className="config-label">
                            Random Seed: <span className="config-value">{config.random_state}</span>
                        </label>
                        <input
                            type="range"
                            min="0"
                            max="100"
                            step="1"
                            value={config.random_state}
                            onChange={(e) => updateConfig('random_state', parseInt(e.target.value))}
                            className="slider"
                        />
                    </div>

                    {/* Manual Mode Settings */}
                    {config.mode === 'manual' && (
                        <>
                            <div className="config-section">
                                <label className="config-label">
                                    Number of Trees: <span className="config-value">{config.n_estimators}</span>
                                </label>
                                <input
                                    type="range"
                                    min="10"
                                    max="500"
                                    step="10"
                                    value={config.n_estimators}
                                    onChange={(e) => updateConfig('n_estimators', parseInt(e.target.value))}
                                    className="slider"
                                />
                                <div className="slider-labels">
                                    <span>10</span>
                                    <span>500</span>
                                </div>
                            </div>

                            <div className="config-section">
                                <label className="config-label">
                                    Max Depth: <span className="config-value">{config.max_depth}</span>
                                </label>
                                <input
                                    type="range"
                                    min="1"
                                    max="20"
                                    step="1"
                                    value={config.max_depth}
                                    onChange={(e) => updateConfig('max_depth', parseInt(e.target.value))}
                                    className="slider"
                                />
                                <div className="slider-labels">
                                    <span>1</span>
                                    <span>20</span>
                                </div>
                            </div>
                        </>
                    )}

                    {/* Feature Engineering Toggles */}
                    <div className="config-section">
                        <label className="config-label">Feature Engineering</label>
                        <div className="checkbox-group">
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    checked={config.scaling}
                                    onChange={(e) => updateConfig('scaling', e.target.checked)}
                                />
                                <span>Standard Scaling</span>
                            </label>
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    checked={config.feature_selection}
                                    onChange={(e) => updateConfig('feature_selection', e.target.checked)}
                                />
                                <span>Feature Selection</span>
                            </label>
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    checked={config.pca}
                                    onChange={(e) => updateConfig('pca', e.target.checked)}
                                />
                                <span>PCA Reduction</span>
                            </label>
                        </div>
                    </div>

                    {/* PCA Components (if enabled) */}
                    {config.pca && (
                        <div className="config-section">
                            <label className="config-label">
                                PCA Components: <span className="config-value">{config.pca_components}</span>
                            </label>
                            <input
                                type="range"
                                min="2"
                                max="50"
                                step="1"
                                value={config.pca_components}
                                onChange={(e) => updateConfig('pca_components', parseInt(e.target.value))}
                                className="slider"
                            />
                        </div>
                    )}

                    {/* Show Python Code */}
                    <div className="config-actions">
                        <Button
                            variant="secondary"
                            size="sm"
                            icon={<Code size={14} />}
                            onClick={() => setShowCode(!showCode)}
                        >
                            {showCode ? 'Hide' : 'Show'} Python Code
                        </Button>
                    </div>

                    {showCode && (
                        <div className="python-code-preview">
                            <pre><code>{generatePythonCode()}</code></pre>
                        </div>
                    )}
                </div>
            )}
        </Card>
    );
};
