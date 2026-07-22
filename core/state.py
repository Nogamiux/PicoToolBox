from __future__ import annotations

import json
import os

STATE_FILENAME = ".dspico_updater_state.json"


def _state_path(pico_folder: str) -> str:
    return os.path.join(pico_folder, STATE_FILENAME)


def load_state(pico_folder: str) -> dict:
    path = _state_path(pico_folder)
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(pico_folder: str, state: dict) -> None:
    os.makedirs(pico_folder, exist_ok=True)
    path = _state_path(pico_folder)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def set_component_version(pico_folder: str, component_key: str, tag_name: str) -> None:
    state = load_state(pico_folder)
    state[component_key] = {"tag_name": tag_name}
    save_state(pico_folder, state)


def get_component_version(pico_folder: str, component_key: str) -> str | None:
    state = load_state(pico_folder)
    entry = state.get(component_key)
    if entry:
        return entry.get("tag_name")
    return None