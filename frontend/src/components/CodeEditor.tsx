import React, { useRef } from 'react';
import Editor, { Monaco } from '@monaco-editor/react';
import './CodeEditor.css';

interface CodeEditorProps {
    value: string;
    onChange: (value: string) => void;
    language?: string;
    height?: string;
    readOnly?: boolean;
    theme?: 'vs-dark' | 'light';
}

export const CodeEditor: React.FC<CodeEditorProps> = ({
    value,
    onChange,
    language = 'python',
    height = '400px',
    readOnly = false,
    theme = 'vs-dark'
}) => {
    const editorRef = useRef<any>(null);

    const handleEditorDidMount = (editor: any, monaco: Monaco) => {
        editorRef.current = editor;

        // Configure Python language features
        monaco.languages.typescript.javascriptDefaults.setDiagnosticsOptions({
            noSemanticValidation: true,
            noSyntaxValidation: true
        });
    };

    const handleEditorChange = (value: string | undefined) => {
        if (value !== undefined && !readOnly) {
            onChange(value);
        }
    };

    return (
        <div className="code-editor">
            <Editor
                height={height}
                language={language}
                value={value}
                onChange={handleEditorChange}
                onMount={handleEditorDidMount}
                theme={theme}
                options={{
                    readOnly,
                    minimap: { enabled: false },
                    fontSize: 14,
                    lineNumbers: 'on',
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    tabSize: 4,
                    insertSpaces: true,
                    wordWrap: 'on',
                    folding: true,
                    lineDecorationsWidth: 10,
                    lineNumbersMinChars: 3,
                }}
            />
        </div>
    );
};
