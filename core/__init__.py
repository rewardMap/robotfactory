from .task import get_task

try:
    from .configs import get_configs
except ImportError as e:
    print(f"[WARN] Could not register get_configs : {e}")

from .instructions import get_instructions
from .render import get_render_info

__all__ = [
    "get_configs",
    "get_instructions",
    "get_render_info",
    "get_task",
]
