import os
import yaml
from .yaml_loader import load_and_merge_yaml
from .context import get_app_root


def _load_backends_from_env():
    backends = {}
    prefix = "COMFYUI_BACKEND_"
    for key, value in os.environ.items():
        if key.startswith(prefix):
            backend_name = key[len(prefix):].lower()
            if value:
                backends[backend_name] = value
    return backends


def load_config():
    config_data = load_and_merge_yaml("config.yaml")
    if not config_data:
        # Fallback minimal default configuration
        return {
            "comfyui_path": os.getenv("COMFYUI_PATH", ""),
            "comfyui_backends": {"default": "http://127.0.0.1:8188"},
            "wait_for_all_backends": False,
            "save_workflow_to_json": False,
            "auto_download_models": True,
            "enable_login": False,
        }
    return config_data


config = load_config()

WAIT_FOR_ALL_BACKENDS = config.get("wait_for_all_backends", False)

env_backends = _load_backends_from_env()
if env_backends:
    COMFYUI_BACKENDS = env_backends
    print("[Config] Loaded ComfyUI backends from environment variables.")
else:
    COMFYUI_BACKENDS = config.get("comfyui_backends", {})
    if not isinstance(COMFYUI_BACKENDS, dict) or "default" not in COMFYUI_BACKENDS:
        # Graceful fallback instead of crashing at import time
        print("[Config] Warning: 'comfyui_backends' missing or has no 'default' backend in config. Using fallback http://127.0.0.1:8188.")
        COMFYUI_BACKENDS = {"default": "http://127.0.0.1:8188"}
    else:
        print("[Config] Loaded ComfyUI backends from configuration.")

COMFYUI_PATH = os.getenv("COMFYUI_PATH", config.get("comfyui_path") or "")
if not COMFYUI_PATH or not os.path.isdir(COMFYUI_PATH):
    # Do not raise hard exception during import to allow pure headless tools / testing
    if COMFYUI_PATH:
        print(f"[Config] Warning: ComfyUI path '{COMFYUI_PATH}' is not an existing directory.")
    else:
        COMFYUI_PATH = os.path.join(get_app_root(), "comfyui_workspace")

SAVE_WORKFLOW_TO_JSON = config.get("save_workflow_to_json", False)

CIVITAI_API_KEY = os.getenv("CIVITAI_API_KEY", config.get("civitai_api_key", ""))
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", config.get("huggingface_token", ""))

ENABLE_LOGIN = config.get("enable_login", False)
LOGIN_CREDENTIALS = config.get("login_credentials", [])

if ENABLE_LOGIN:
    if not LOGIN_CREDENTIALS or not isinstance(LOGIN_CREDENTIALS, list):
        print("[Config] Warning: 'enable_login' is true, but 'login_credentials' is not set correctly.")
    else:
        for cred in LOGIN_CREDENTIALS:
            if not isinstance(cred, dict) or not cred.get('username') or not cred.get('password'):
                print("[Config] Warning: Login credential entry format is invalid.")

AUTO_DOWNLOAD_MODELS = config.get("auto_download_models", True)

COMFYUI_INPUT_PATH = os.path.join(COMFYUI_PATH, "input")
COMFYUI_OUTPUT_PATH = os.path.join(COMFYUI_PATH, "output")
LORA_DIR = os.path.join(COMFYUI_PATH, "models", "loras")
EMBEDDING_DIR = os.path.join(COMFYUI_PATH, "models", "embeddings")
JSON_SAVE_PATH = os.path.join(COMFYUI_PATH, "JSON")

try:
    if COMFYUI_PATH and os.path.isdir(COMFYUI_PATH):
        os.makedirs(COMFYUI_INPUT_PATH, exist_ok=True)
        os.makedirs(LORA_DIR, exist_ok=True)
        os.makedirs(EMBEDDING_DIR, exist_ok=True)
        os.makedirs(JSON_SAVE_PATH, exist_ok=True)
except Exception as e:
    print(f"[Config] Notice: Could not create directories under COMFYUI_PATH: {e}")
