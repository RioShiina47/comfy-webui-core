import os
import yaml
from collections.abc import Mapping
from .context import get_app_root

_config_cache = {}


def get_base_yaml_dir() -> str:
    app_root = get_app_root()
    return os.path.join(app_root, "yaml")


def deep_merge_dicts(base, custom):
    if not isinstance(base, Mapping) or not isinstance(custom, Mapping):
        return custom

    merged = base.copy()
    for key, custom_value in custom.items():
        base_value = merged.get(key)
        if isinstance(base_value, Mapping) and isinstance(custom_value, Mapping):
            merged[key] = deep_merge_dicts(base_value, custom_value)
        else:
            merged[key] = custom_value
    return merged


def load_and_merge_yaml(filename: str):
    if filename in _config_cache:
        return _config_cache[filename]

    base_yaml_dir = get_base_yaml_dir()
    base_config_path = os.path.join(base_yaml_dir, filename)
    base_config = {}

    if os.path.exists(base_config_path):
        with open(base_config_path, "r", encoding="utf-8") as f:
            try:
                base_config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing configuration file {filename}: {e}")
                base_config = {}

    # Check for user-defined overrides in custom/yaml/
    custom_yaml_dir = os.path.join(get_app_root(), "custom", "yaml")
    custom_config_path = os.path.join(custom_yaml_dir, filename)
    if os.path.exists(custom_config_path):
        with open(custom_config_path, "r", encoding="utf-8") as f:
            try:
                custom_config = yaml.safe_load(f) or {}
                if isinstance(custom_config, dict):
                    base_config = deep_merge_dicts(base_config, custom_config)
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing custom configuration file {filename}: {e}")

    _config_cache[filename] = base_config
    return base_config


def load_and_merge_yaml_from_module(module_path: str, filename: str):
    module_yaml_dir = os.path.join(module_path, "yaml")
    base_config_path = os.path.join(module_yaml_dir, filename)
    base_config = {}
    if os.path.exists(base_config_path):
        with open(base_config_path, "r", encoding="utf-8") as f:
            try:
                base_config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing module configuration file {filename}: {e}")
                base_config = {}

    return base_config


def __getattr__(name: str):
    if name == "ROOT_DIR":
        return get_app_root()
    if name == "BASE_YAML_DIR":
        return get_base_yaml_dir()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
