from .task import get_task

try:
    from .configs import get_configs
except ImportError as e:
    print(f"[WARN] Could not register get_configs : {e}")

from .backend_psychopy import get_psychopy_info

from .instructions_psychopy import instructions_psychopy

try:
    from .backend_pygame import get_pygame_info
except (ImportError, NameError):
    get_pygame_info = None


__all__ = [
    "get_configs",
    "get_pygame_info",
    "get_psychopy_info",
    "get_task",
    "instructions_psychopy",
]
