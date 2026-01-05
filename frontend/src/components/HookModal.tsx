import React, { useState } from 'react';
import { CodeEditor } from './CodeEditor';
import { Button } from './Button';
import { X } from 'lucide-react';
import './HookModal.css';

interface HookModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: (hookData: { type: string; code: string }) => void;
    blockId: string;
    blockName: string;
    initialCode?: string;
    initialType?: string;
}

const HOOK_TEMPLATES = {
    before: `def before_{block_id}(context):
    """
    Runs BEFORE the {block_name} block.
    
    Available in context:
    - context.raw_data: pandas DataFrame
    - context.target_column: str
    - context.feature_names: list
    - context.log(message): Log to execution
    
    Return context to continue execution.
    """
    import numpy as np
    import pandas as pd
    
    # Your code here
    context.log("Before hook executed")
    
    return context
`,
    after: `def after_{block_id}(context):
    """
    Runs AFTER the {block_name} block.
    
    Available in context:
    - context.train_data: pandas DataFrame
    - context.test_data: pandas DataFrame
    - context.metrics: dict
    - context.log(message): Log to execution
    
    Return context to continue execution.
    """
    import numpy as np
    import pandas as pd
    
    # Your code here
    context.log("After hook executed")
    
    return context
`,
    override: `def override_{block_id}(context):
    """
    REPLACES the {block_name} block entirely.
    System logic will be SKIPPED.
    
    Available in context:
    - All context variables
    - context.log(message): Log to execution
    
    You MUST implement the block's functionality yourself.
    Return context to continue execution.
    """
    import numpy as np
    import pandas as pd
    
    # Your complete implementation here
    context.log("Override hook executed - system logic skipped")
    
    return context
`
};

export const HookModal: React.FC<HookModalProps> = ({
    isOpen,
    onClose,
    onSave,
    blockId,
    blockName,
    initialCode,
    initialType = 'before'
}) => {
    const [hookType, setHookType] = useState(initialType);
    const [code, setCode] = useState(initialCode || '');

    React.useEffect(() => {
        if (isOpen && !initialCode) {
            // Load template when modal opens
            const template = HOOK_TEMPLATES[hookType as keyof typeof HOOK_TEMPLATES]
                .replace(/{block_id}/g, blockId.toLowerCase().replace(/_/g, '_'))
                .replace(/{block_name}/g, blockName);
            setCode(template);
        }
    }, [isOpen, hookType, blockId, blockName, initialCode]);

    const handleSave = () => {
        onSave({ type: hookType, code });
        onClose();
    };

    const handleTypeChange = (type: string) => {
        setHookType(type);
        // Load new template
        const template = HOOK_TEMPLATES[type as keyof typeof HOOK_TEMPLATES]
            .replace(/{block_id}/g, blockId.toLowerCase().replace(/_/g, '_'))
            .replace(/{block_name}/g, blockName);
        setCode(template);
    };

    if (!isOpen) return null;

    return (
        <div className="hook-modal-overlay" onClick={onClose}>
            <div className="hook-modal" onClick={(e) => e.stopPropagation()}>
                <div className="hook-modal__header">
                    <div>
                        <h3>Add Hook to {blockName}</h3>
                        <p className="text-secondary">Inject custom Python code into the pipeline</p>
                    </div>
                    <button className="hook-modal__close" onClick={onClose}>
                        <X size={20} />
                    </button>
                </div>

                <div className="hook-modal__content">
                    <div className="hook-modal__type-selector">
                        <label>Hook Type:</label>
                        <div className="hook-type-buttons">
                            <button
                                className={`hook-type-btn ${hookType === 'before' ? 'active' : ''}`}
                                onClick={() => handleTypeChange('before')}
                            >
                                Before
                                <span className="hook-type-desc">Runs before system logic</span>
                            </button>
                            <button
                                className={`hook-type-btn ${hookType === 'after' ? 'active' : ''}`}
                                onClick={() => handleTypeChange('after')}
                            >
                                After
                                <span className="hook-type-desc">Runs after system logic</span>
                            </button>
                            <button
                                className={`hook-type-btn ${hookType === 'override' ? 'active' : ''}`}
                                onClick={() => handleTypeChange('override')}
                            >
                                Override
                                <span className="hook-type-desc">Replaces system logic</span>
                            </button>
                        </div>
                    </div>

                    <div className="hook-modal__editor">
                        <label>Python Code:</label>
                        <CodeEditor
                            value={code}
                            onChange={setCode}
                            height="400px"
                        />
                    </div>

                    <div className="hook-modal__info">
                        <p className="text-tertiary">
                            <strong>Hook Execution Order:</strong> override → before → system → after
                        </p>
                        <p className="text-tertiary">
                            Hooks have access to the execution context and can modify data, add features, or replace entire blocks.
                        </p>
                    </div>
                </div>

                <div className="hook-modal__footer">
                    <Button variant="ghost" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button variant="primary" onClick={handleSave}>
                        Save Hook
                    </Button>
                </div>
            </div>
        </div>
    );
};
