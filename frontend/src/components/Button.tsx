import React from 'react';
import './Button.css';

interface ButtonProps {
    children: React.ReactNode;
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    loading?: boolean;
    icon?: React.ReactNode;
    onClick?: (e?: React.MouseEvent<HTMLButtonElement>) => void;
    type?: 'button' | 'submit' | 'reset';
    className?: string;
}

export const Button: React.FC<ButtonProps> = ({
    children,
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    icon,
    onClick,
    type = 'button',
    className = ''
}) => {
    const classes = [
        'butterfly-btn',
        `butterfly-btn--${variant}`,
        `butterfly-btn--${size}`,
        loading && 'butterfly-btn--loading',
        className
    ].filter(Boolean).join(' ');

    return (
        <button
            type={type}
            className={classes}
            onClick={onClick}
            disabled={disabled || loading}
        >
            {loading && (
                <span className="butterfly-btn__spinner"></span>
            )}
            {icon && !loading && (
                <span className="butterfly-btn__icon">{icon}</span>
            )}
            <span className="butterfly-btn__text">{children}</span>
        </button>
    );
};
