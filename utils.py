import sys


def err(*args, **kwargs):
    """Print to standard error output."""
    print(*args, file=sys.stderr, **kwargs)
