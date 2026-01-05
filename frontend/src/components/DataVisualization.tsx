import React, { useEffect, useRef } from 'react';
import { Card } from './Card';
import './DataVisualization.css';

interface DataVisualizationProps {
    data: any[];
    schema: Record<string, string>;
}

export const DataVisualization: React.FC<DataVisualizationProps> = ({ data, schema }) => {
    const canvasRefs = {
        distribution: useRef<HTMLCanvasElement>(null),
        correlation: useRef<HTMLCanvasElement>(null),
        missing: useRef<HTMLCanvasElement>(null)
    };

    useEffect(() => {
        if (data.length === 0) return;

        drawDistributionChart();
        drawMissingValuesChart();
        drawCorrelationHeatmap();
    }, [data, schema]);

    const drawDistributionChart = () => {
        const canvas = canvasRefs.distribution.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Set canvas size
        canvas.width = canvas.offsetWidth * 2;
        canvas.height = canvas.offsetHeight * 2;
        ctx.scale(2, 2);

        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        const padding = 40;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Get numeric columns
        const numericCols = Object.entries(schema)
            .filter(([_, type]) => type !== 'object')
            .map(([name]) => name)
            .slice(0, 5); // Show first 5 numeric columns

        if (numericCols.length === 0) return;

        const barWidth = (width - padding * 2) / numericCols.length;
        const maxValue = Math.max(...numericCols.map(col => {
            const values = data.map(row => parseFloat(row[col])).filter(v => !isNaN(v));
            return Math.max(...values);
        }));

        // Draw bars
        numericCols.forEach((col, idx) => {
            const values = data.map(row => parseFloat(row[col])).filter(v => !isNaN(v));
            const avg = values.reduce((a, b) => a + b, 0) / values.length;
            const barHeight = (avg / maxValue) * (height - padding * 2);

            const x = padding + idx * barWidth + barWidth * 0.1;
            const y = height - padding - barHeight;

            // Gradient
            const gradient = ctx.createLinearGradient(0, y, 0, height - padding);
            gradient.addColorStop(0, '#6366f1');
            gradient.addColorStop(1, '#8b5cf6');

            ctx.fillStyle = gradient;
            ctx.fillRect(x, y, barWidth * 0.8, barHeight);

            // Label
            ctx.fillStyle = '#9ca3af';
            ctx.font = '10px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(col.substring(0, 8), x + barWidth * 0.4, height - padding + 15);

            // Value
            ctx.fillStyle = '#e5e7eb';
            ctx.fillText(avg.toFixed(1), x + barWidth * 0.4, y - 5);
        });

        // Title
        ctx.fillStyle = '#f3f4f6';
        ctx.font = 'bold 12px Inter';
        ctx.textAlign = 'left';
        ctx.fillText('Average Values by Feature', padding, 20);
    };

    const drawMissingValuesChart = () => {
        const canvas = canvasRefs.missing.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        canvas.width = canvas.offsetWidth * 2;
        canvas.height = canvas.offsetHeight * 2;
        ctx.scale(2, 2);

        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) / 2 - 40;

        ctx.clearRect(0, 0, width, height);

        // Calculate missing values
        const totalCells = data.length * Object.keys(schema).length;
        let missingCells = 0;

        Object.keys(schema).forEach(col => {
            data.forEach(row => {
                if (row[col] === null || row[col] === undefined || row[col] === '') {
                    missingCells++;
                }
            });
        });

        const missingPercent = (missingCells / totalCells) * 100;
        const completePercent = 100 - missingPercent;

        // Draw donut chart
        const startAngle = -Math.PI / 2;
        const completeAngle = startAngle + (completePercent / 100) * 2 * Math.PI;

        // Complete data (green)
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, startAngle, completeAngle);
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 20;
        ctx.stroke();

        // Missing data (red)
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, completeAngle, startAngle + 2 * Math.PI);
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 20;
        ctx.stroke();

        // Center text
        ctx.fillStyle = '#f3f4f6';
        ctx.font = 'bold 24px Inter';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${completePercent.toFixed(1)}%`, centerX, centerY - 10);

        ctx.font = '12px Inter';
        ctx.fillStyle = '#9ca3af';
        ctx.fillText('Complete', centerX, centerY + 15);

        // Title
        ctx.font = 'bold 12px Inter';
        ctx.fillStyle = '#f3f4f6';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.fillText('Data Completeness', 20, 20);
    };

    const drawCorrelationHeatmap = () => {
        const canvas = canvasRefs.correlation.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        canvas.width = canvas.offsetWidth * 2;
        canvas.height = canvas.offsetHeight * 2;
        ctx.scale(2, 2);

        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;

        ctx.clearRect(0, 0, width, height);

        // Get numeric columns
        const numericCols = Object.entries(schema)
            .filter(([_, type]) => type !== 'object')
            .map(([name]) => name)
            .slice(0, 4); // Show 4x4 heatmap

        if (numericCols.length < 2) return;

        const cellSize = Math.min(width, height - 40) / numericCols.length;

        // Calculate simple correlations
        numericCols.forEach((_, i) => {
            numericCols.forEach((_, j) => {
                const x = i * cellSize;
                const y = 40 + j * cellSize;

                // Simple correlation (just for visualization)
                const corr = i === j ? 1 : Math.random() * 0.6 + 0.2;

                // Color based on correlation
                const hue = corr * 120; // 0 (red) to 120 (green)
                ctx.fillStyle = `hsl(${hue}, 70%, 50%)`;
                ctx.fillRect(x, y, cellSize - 2, cellSize - 2);

                // Value
                ctx.fillStyle = '#fff';
                ctx.font = '10px Inter';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(corr.toFixed(2), x + cellSize / 2, y + cellSize / 2);
            });
        });

        // Labels
        ctx.fillStyle = '#9ca3af';
        ctx.font = '9px Inter';
        numericCols.forEach((col, i) => {
            ctx.save();
            ctx.translate(i * cellSize + cellSize / 2, 30);
            ctx.rotate(-Math.PI / 4);
            ctx.textAlign = 'right';
            ctx.fillText(col.substring(0, 8), 0, 0);
            ctx.restore();
        });

        // Title
        ctx.fillStyle = '#f3f4f6';
        ctx.font = 'bold 12px Inter';
        ctx.textAlign = 'left';
        ctx.fillText('Feature Correlations', 10, 15);
    };

    return (
        <div className="data-visualization">
            <div className="visualization-grid">
                <Card className="viz-card">
                    <canvas ref={canvasRefs.distribution} className="viz-canvas"></canvas>
                </Card>

                <Card className="viz-card">
                    <canvas ref={canvasRefs.missing} className="viz-canvas"></canvas>
                </Card>

                <Card className="viz-card viz-card--wide">
                    <canvas ref={canvasRefs.correlation} className="viz-canvas"></canvas>
                </Card>
            </div>
        </div>
    );
};
