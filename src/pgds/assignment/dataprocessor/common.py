"""
Common Utilities
Shared helper functions used across dataprocessor modules.
"""
import os


def ensure_dirs(*paths):
    """Create directories if they do not already exist."""
    for path in paths:
        os.makedirs(path, exist_ok=True)
