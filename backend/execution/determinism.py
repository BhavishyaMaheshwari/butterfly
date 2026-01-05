"""
Butterfly Execution Engine - Determinism

Manages seed control and deterministic execution guarantees.
Follows 09_execution_rules.md section 7.
"""
import random
import numpy as np
import os


class DeterminismManager:
    """
    Ensures deterministic execution across all randomness sources.
    
    From 09_execution_rules.md:
    - A single global seed is applied per run
    - All randomness must derive from this seed
    - Any non-deterministic operation must be declared explicitly
    
    Guarantees:
    - Same seed + same input = same output
    """
    
    @staticmethod
    def set_global_seed(seed: int):
        """
        Set global seed for all randomness sources.
        
        Sets seeds for:
        - Python random module
        - NumPy
        - Environment variables (for ML libraries)
        """
        # Python random
        random.seed(seed)
        
        # NumPy
        np.random.seed(seed)
        
        # Environment variables for ML libraries
        os.environ['PYTHONHASHSEED'] = str(seed)
        
        # Try to set seeds for common ML libraries if available
        try:
            import torch
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        except ImportError:
            pass
        
        try:
            import tensorflow as tf
            tf.random.set_seed(seed)
        except ImportError:
            pass
    
    @staticmethod
    def get_seeded_rng(seed: int) -> np.random.Generator:
        """
        Get a seeded random number generator.
        
        Returns a NumPy Generator for deterministic random operations.
        """
        return np.random.default_rng(seed)
