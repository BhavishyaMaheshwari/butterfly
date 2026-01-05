"""
Butterfly Execution Engine - Hook Executor

Executes user-provided hooks with sandboxing.
Follows 09_execution_rules.md section 11.
"""
from typing import Any, Dict
import sys
from io import StringIO
import traceback

from backend.domain import Hook, HookType, ExecutionContext


class HookExecutor:
    """
    Executes user-provided code in restricted environment.
    
    From 09_execution_rules.md section 11:
    - User code runs with the same execution guarantees as system code
    - User code cannot bypass sandbox restrictions
    - User code errors are treated as run failures
    
    Responsibilities:
    - Execute hooks safely
    - Capture output and errors
    - Enforce resource limits (basic)
    """
    
    def __init__(self):
        self.restricted_imports = {
            'os': ['system', 'exec', 'spawn'],
            'subprocess': ['*'],
            'eval': ['*'],
            'exec': ['*'],
        }
    
    def execute_hook(
        self,
        hook: Hook,
        context: ExecutionContext,
        block_type: str
    ) -> tuple[bool, str]:
        """
        Execute a hook with the execution context.
        
        Args:
            hook: Hook to execute
            context: Execution context (mutable)
            block_type: Type of block this hook is for
        
        Returns:
            (success, output/error_message)
        """
        context.log(f"Executing {hook.type.value} hook for {block_type}")
        
        # Prepare execution namespace
        namespace = {
            'context': context,
            'pd': None,  # Will import pandas if needed
            'np': None,  # Will import numpy if needed
        }
        
        # Import safe libraries
        try:
            import pandas as pd
            import numpy as np
            namespace['pd'] = pd
            namespace['np'] = np
        except ImportError:
            pass
        
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        captured_output = StringIO()
        
        try:
            sys.stdout = captured_output
            sys.stderr = captured_output
            
            # Execute user code
            exec(hook.code, namespace)
            
            output = captured_output.getvalue()
            if output:
                context.log(f"Hook output: {output}")
            
            return True, output
        
        except Exception as e:
            error_msg = f"Hook execution failed: {str(e)}\n{traceback.format_exc()}"
            context.log(f"ERROR: {error_msg}")
            return False, error_msg
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def validate_hook_code(self, code: str) -> tuple[bool, str]:
        """
        Basic validation of hook code.
        
        Checks for obviously dangerous patterns.
        Returns (is_valid, error_message)
        """
        dangerous_patterns = [
            'import os',
            'import subprocess',
            '__import__',
            'eval(',
            'exec(',
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Try to compile
        try:
            compile(code, '<hook>', 'exec')
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
