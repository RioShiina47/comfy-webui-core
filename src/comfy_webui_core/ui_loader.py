import os
import importlib
import sys
import yaml
from collections import defaultdict
from .context import get_app_root


def discover_ui_modules():
    ui_tree = defaultdict(list)
    ui_modules = {}

    app_root = get_app_root()
    if app_root not in sys.path:
        sys.path.insert(0, app_root)

    module_dir = os.path.join(app_root, "module")
    print(f"Discovering all UI modules in {module_dir}...")
    if not os.path.isdir(module_dir):
        # Also check relative fallback
        if os.path.isdir("module"):
            module_dir = os.path.abspath("module")

    if os.path.isdir(module_dir):
        for root, _, files in os.walk(module_dir):
            for filename in files:
                if filename.endswith("_ui.py") and filename != "__init__.py":
                    rel_to_app = os.path.relpath(os.path.join(root, filename[:-3]), app_root)
                    module_path_parts = os.path.normpath(rel_to_app).split(os.sep)
                    module_name = ".".join(module_path_parts)
                    _load_and_register_module(module_name, ui_tree, ui_modules)

    return ui_tree, ui_modules


def _load_and_register_module(module_name, ui_tree, ui_modules):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, "UI_INFO"):
            info = module.UI_INFO
            if "main_tab" not in info or "sub_tab" not in info:
                print(f"Skipping module {module_name}: UI_INFO missing 'main_tab' or 'sub_tab'.")
                return

            main_tab_name = info["main_tab"]
            sub_tab_name = info["sub_tab"]

            ui_tree[main_tab_name].append(info)
            ui_modules[sub_tab_name] = module
            print(f"Successfully loaded UI module: {module_name}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error loading UI module {module_name}: {e}")


def load_ui_layout():
    app_root = get_app_root()
    layout_path = os.path.join(app_root, "yaml", "ui_layout.yaml")
    layout_config = {"main_tabs_order": [], "sub_tabs_order": {}}

    if not os.path.exists(layout_path):
        print("Notice: No 'ui_layout.yaml' found in host application. Using alphabetical module sorting.")
        return layout_config

    try:
        with open(layout_path, "r", encoding="utf-8") as f:
            layout = yaml.safe_load(f)

        if isinstance(layout, dict) and "main_tabs_order" in layout:
            for item in layout["main_tabs_order"]:
                if isinstance(item, dict):
                    main_tab_name = next(iter(item))
                    layout_config["main_tabs_order"].append(main_tab_name)
                    layout_config["sub_tabs_order"][main_tab_name] = item[main_tab_name]
                else:
                    layout_config["main_tabs_order"].append(item)

        print("Successfully loaded UI layout configuration.")
    except Exception as e:
        print(f"Error loading UI layout configuration from {layout_path}: {e}")

    return layout_config
