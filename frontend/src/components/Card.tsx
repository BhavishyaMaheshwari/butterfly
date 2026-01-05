import React from 'react';
import './Card.css';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    variant?: 'default' | 'glass' | 'elevated';
    hoverable?: boolean;
    onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
    children,
    className = '',
    variant = 'default',
    hoverable = false,
    onClick
}) => {
    const classes = [
        'butterfly-card',
        `butterfly-card--${variant}`,
        hoverable && 'butterfly-card--hoverable',
        onClick && 'butterfly-card--clickable',
        className
    ].filter(Boolean).join(' ');

    return (
        <div className={classes} onClick={onClick}>
            {children}
        </div>
    );
};
