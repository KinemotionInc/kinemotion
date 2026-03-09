"""Determinism utilities for reproducible analysis.

Provides functions to set random seeds for NumPy and Python's random module
to ensure deterministic behavior.
"""

import hashlib
import os
import random
from pathlib import Path

import numpy as np


def get_video_hash_seed(video_path: str) -> int:
    """Generate deterministic seed from video file path.

    Uses video filename (not contents) to generate a consistent seed
    for the same video across multiple runs.

    Args:
        video_path: Path to video file

    Returns:
        Integer seed value derived from filename
    """
    # Use filename only (not full path) for consistency
    filename = Path(video_path).name
    # Hash filename to get deterministic seed
    hash_value = hashlib.md5(filename.encode()).hexdigest()
    # Convert first 8 hex chars to integer
    return int(hash_value[:8], 16)


def set_deterministic_mode(seed: int | None = None, video_path: str | None = None) -> None:
    """Set random seeds for reproducible analysis.

    Sets seeds for:
    - Python's random module
    - NumPy random number generator

    Args:
        seed: Random seed value. If None and video_path provided,
              generates seed from video filename.
        video_path: Optional video path to generate deterministic seed

    Note:
        This should be called before any MediaPipe or analysis operations
        to ensure deterministic pose detection and metric calculation.
    """
    # Generate seed from video if not provided
    if seed is None and video_path is not None:
        seed = get_video_hash_seed(video_path)
    elif seed is None:
        seed = 42  # Default

    # Python random
    random.seed(seed)

    # NumPy random
    np.random.seed(seed)

    # Set hash seed for deterministic hashing
    os.environ["PYTHONHASHSEED"] = str(seed)
