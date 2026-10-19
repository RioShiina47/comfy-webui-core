"""
Comfy Web UI Core Framework.

Provides dynamic ComfyUI workflow engine, Gradio WebUI dynamic assembly,
MCP server endpoints, multi-backend routing, and chain injector topology.
"""

from .context import set_app_root, get_app_root
from .workflow_assembler import WorkflowAssembler
from .ui_builder import build_gradio_ui
from .ui_loader import discover_ui_modules, load_ui_layout
from .backend_manager import backend_manager
from .node_info_manager import (
    fetch_and_cache_object_info,
    get_node_info,
    get_all_node_info,
)
from .job_manager import (
    create_job,
    get_job,
    update_job,
    get_latest_running_job_for_module,
)
from .yaml_loader import load_and_merge_yaml, load_and_merge_yaml_from_module

from . import config
from . import workflow_assembler
from . import ui_builder
from . import ui_loader
from . import backend_manager as backend_manager_mod
from . import node_info_manager as node_info_manager_mod
from . import job_manager as job_manager_mod
from . import comfy_api
from . import shared_ui
from . import utils
from . import input_processors
from . import yaml_loader
from . import download_utils
from . import model_downloader
from . import chain_injectors

__version__ = "0.1.1"

__all__ = [
    "set_app_root",
    "get_app_root",
    "WorkflowAssembler",
    "build_gradio_ui",
    "discover_ui_modules",
    "load_ui_layout",
    "backend_manager",
    "fetch_and_cache_object_info",
    "get_node_info",
    "get_all_node_info",
    "create_job",
    "get_job",
    "update_job",
    "get_latest_running_job_for_module",
    "load_and_merge_yaml",
    "load_and_merge_yaml_from_module",
    "config",
    "workflow_assembler",
    "ui_builder",
    "ui_loader",
    "comfy_api",
    "shared_ui",
    "utils",
    "input_processors",
    "yaml_loader",
    "download_utils",
    "model_downloader",
    "chain_injectors",
]
