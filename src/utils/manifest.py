import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def ensure_data_dir():
    """Ensures the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def get_manifest_path():
    return os.path.join(DATA_DIR, "schema_manifest.json")

def get_router_map_path():
    return os.path.join(DATA_DIR, "router_map.json")

def get_fk_graph_path():
    return os.path.join(DATA_DIR, "fk_graph.json")

def load_json_file(file_path, default=None):
    """Loads a JSON file if it exists, otherwise returns a default value."""
    if default is None:
        default = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json_file(file_path, data):
    """Saves data to a JSON file."""
    ensure_data_dir()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_manifest():
    return load_json_file(get_manifest_path())

def save_manifest(manifest):
    save_json_file(get_manifest_path(), manifest)

def load_router_map():
    return load_json_file(get_router_map_path())

def save_router_map(router_map):
    save_json_file(get_router_map_path(), router_map)

def load_fk_graph():
    return load_json_file(get_fk_graph_path())

def save_fk_graph(fk_graph):
    save_json_file(get_fk_graph_path(), fk_graph)
