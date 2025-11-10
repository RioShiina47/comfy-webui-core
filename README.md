# Comfy web UI Core

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is the core framework of the [comfy-webui](https://github.com/RioShiina47/comfy-webui) project.

We have removed all specific application-layer feature modules, retaining only the most essential components: the dynamic workflow engine, UI/API/MCP generator, and backend management system.

Its goal is to provide developers with a clean, lightweight starting point for rapidly building custom, complex-workflow-oriented Gradio WebUI applications on top of the powerful ComfyUI platform. It is an ideal choice for rapid prototyping.

---

## Core Features

While it doesn't include any specific generation features, `comfy-webui-core` provides a powerful set of underlying mechanisms:

-   **Recipe-Driven Dynamic Workflows**
    Define ComfyUI node blueprints using simple and intuitive YAML `recipe` files. The system dynamically and programmatically assembles these into a final, executable, and complex workflow JSON based on user input from the frontend.

-   **Pluggable Chain Injectors**
    The core framework includes chain injectors for common dynamic functionalities like LoRA, ControlNet, IP-Adapter, and Regional Conditioning. You can easily add these dynamic, stackable capabilities to your new workflows without manually handling complex node connection logic.

-   **API & MCP Ready (Workflow as a Service)**
    The framework is not just for building graphical interfaces; its architecture natively supports Gradio's API and MCP mechanisms. Developers can create an `_mcp.py` file within a module to encapsulate complex, recipe-driven workflows into simple, high-level API and MCP functions that can be called externally, allowing for easy integration with LLMs and AI Agents.

-   **Multi-Backend Management**
    It features a built-in intelligent system for managing connections to multiple backends. You can configure and connect to several different ComfyUI instances (e.g., on different devices or with different dependency environments) and allow various UI modules to schedule tasks to their designated backends.

-   **Asynchronous Job Engine**
    All generation tasks are executed asynchronously in the background. Tasks continue to run on the server even if the browser is closed or the network connection is lost.

-   **Layered Configuration System**
    Through a directory structure of `yaml/` (base configuration) and `custom/yaml/` (user-defined overrides), you can easily separate and merge global and personal settings. This makes project upgrades and customizations simple and conflict-free.

-   **Modular UI Builder**
    The core UI builder can automatically discover the modules you create (`_ui.py`) and generate the corresponding Gradio tabs and interface layouts based on the layout configuration file (`ui_layout.yaml`).

## Target Audience

-   Developers who want to build highly customized web interfaces for ComfyUI.
-   Researchers or tech enthusiasts who need to quickly validate specific complex workflows and provide them with a simple UI.
-   Developers looking to encapsulate complex ComfyUI workflows into standard MCP tools for easy integration with LLMs and AI Agents.
-   Teams seeking a standardized foundational framework for developing in-house AI generation tools.

## Learn About the Full Version

To see a full-featured implementation, more comprehensive module examples, and advanced usage, please refer to the main project: [comfy-webui](https://github.com/RioShiina47/comfy-webui).