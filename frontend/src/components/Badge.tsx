import React from 'react';
import './Badge.css';

interface BadgeProps {
    children: React.ReactNode;
    variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
    size?: 'sm' | 'md';
    icon?: React.ReactNode;
    className?: string;
    style?: React.CSSProperties;
}

export const Badge: React.FC<BadgeProps> = ({
    children,
    variant = 'default',
    size = 'md',
    icon,
    className = '',
    style
}) => {
    const classes = [
        'butterfly-badge',
        `butterfly-badge--${variant}`,
        `butterfly-badge--${size}`,
        className
    ].filter(Boolean).join(' ');

    return (
        <span className={classes} style={style}>
            {icon && <span className="butterfly-badge__icon">{icon}</span>}
            <span className="butterfly-badge__text">{children}</span>
        </span>
    );
};
