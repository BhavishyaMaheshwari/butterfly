"""
Butterfly Execution Engine - Block Executor

Executes pipeline blocks with hook precedence.
Follows 09_execution_rules.md section 5.
"""
from typing import Callable, List, Optional
import traceback

from backend.domain import Block, BlockStatus, BlockType, Hook, HookType, ExecutionContext
from backend.storage import ExperimentStore
from .hook_executor import HookExecutor


class BlockExecutor:
    """
    Executes pipeline blocks with proper hook precedence.
    
    From 09_execution_rules.md section 5.2:
    Hook execution precedence is STRICT and DETERMINISTIC:
    1. override hooks (skip system logic if present)
    2. before hooks
    3. system block logic
    4. after hooks
    
    Rules:
    - If an override hook exists, system logic is skipped
    - Before/after hooks wrap system logic
    - Multiple hooks of the same type execute in registration order
    """
    
    def __init__(self, experiment_store: ExperimentStore):
        self.experiment_store = experiment_store
        self.hook_executor = HookExecutor()
    
    def execute_block(
        self,
        block: Block,
        context: ExecutionContext,
        system_logic: Callable[[ExecutionContext], None],
        experiment_id: str
    ) -> tuple[bool, Optional[str]]:
        """
        Execute a block with full hook precedence.
        
        Args:
            block: Block to execute
            context: Execution context (mutable)
            system_logic: System implementation function
            experiment_id: Experiment ID (to load hooks)
        
        Returns:
            (success, error_message)
        """
        context.set_current_block(block.id)
        context.log(f"=== Executing block: {block.type.value} ===")
        
        # Check if block is enabled
        if not block.enabled:
            context.log(f"Block {block.type.value} is disabled, skipping")
            block.status = BlockStatus.SKIPPED
            context.mark_block_complete(block.id)
            return True, None
        
        block.status = BlockStatus.RUNNING
        
        try:
            # Load hooks for this block
            all_hooks = self.experiment_store.list_hooks(experiment_id)
            block_hooks = [h for h in all_hooks if h.block_id == block.id]
            
            # Separate hooks by type
            override_hooks = [h for h in block_hooks if h.type == HookType.OVERRIDE]
            before_hooks = [h for h in block_hooks if h.type == HookType.BEFORE]
            after_hooks = [h for h in block_hooks if h.type == HookType.AFTER]
            
            # PRECEDENCE STEP 1: Execute override hooks
            # If override hooks exist, system logic is SKIPPED
            if override_hooks:
                context.log(f"Found {len(override_hooks)} override hook(s), system logic will be skipped")
                
                for hook in override_hooks:
                    success, output = self.hook_executor.execute_hook(
                        hook, context, block.type.value
                    )
                    if not success:
                        block.status = BlockStatus.FAILED
                        return False, f"Override hook failed: {output}"
            
            else:
                # PRECEDENCE STEP 2: Execute before hooks
                for hook in before_hooks:
                    context.log(f"Executing before hook")
                    success, output = self.hook_executor.execute_hook(
                        hook, context, block.type.value
                    )
                    if not success:
                        block.status = BlockStatus.FAILED
                        return False, f"Before hook failed: {output}"
                
                # PRECEDENCE STEP 3: Execute system logic
                context.log(f"Executing system logic for {block.type.value}")
                try:
                    system_logic(context)
                except Exception as e:
                    error_msg = f"System logic failed: {str(e)}\n{traceback.format_exc()}"
                    context.log(f"ERROR: {error_msg}")
                    block.status = BlockStatus.FAILED
                    return False, error_msg
                
                # PRECEDENCE STEP 4: Execute after hooks
                for hook in after_hooks:
                    context.log(f"Executing after hook")
                    success, output = self.hook_executor.execute_hook(
                        hook, context, block.type.value
                    )
                    if not success:
                        block.status = BlockStatus.FAILED
                        return False, f"After hook failed: {output}"
            
            # Block completed successfully
            block.status = BlockStatus.COMPLETED
            context.mark_block_complete(block.id)
            context.log(f"Block {block.type.value} completed successfully")
            
            return True, None
        
        except Exception as e:
            error_msg = f"Block execution failed: {str(e)}\n{traceback.format_exc()}"
            context.log(f"ERROR: {error_msg}")
            block.status = BlockStatus.FAILED
            return False, error_msg
