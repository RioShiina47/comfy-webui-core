"""
Application Context for comfy_webui_core.
Manages the application root directory for locating downstream host assets
(such as module/, yaml/, chain_injectors/, custom/).
"""

import os
import sys

_app_root: str | None = None


def set_app_root(path: str) -> None:
    """Explicitly set the root directory of the host application."""
    global _app_root
    _app_root = os.path.abspath(path)


def get_app_root() -> str:
    """
    Get the host application root directory.
    Resolution priority:
    1. Explicitly set via `set_app_root()`
    2. Environment variable `COMFY_WEBUI_APP_ROOT`
    3. Fallback to current working directory `os.getcwd()`
    """
    global _app_root
    if _app_root:
        return _app_root
    env_root = os.getenv("COMFY_WEBUI_APP_ROOT")
    if env_root and os.path.isdir(env_root):
        return os.path.abspath(env_root)
    return os.getcwd()
