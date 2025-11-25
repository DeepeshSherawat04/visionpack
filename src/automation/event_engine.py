# src/automation/event_engine.py

from __future__ import annotations
from enum import Enum, auto
from typing import Any, Callable, Dict, List


class EventType(Enum):
    IMAGE_UPLOADED = auto()
    FEEDBACK_RECEIVED = auto()
    QUALITY_ISSUE = auto()
    MODEL_UPDATED = auto()


Listener = Callable[[Dict[str, Any]], None]

_listeners: Dict[EventType, List[Listener]] = {e: [] for e in EventType}


def register_listener(event_type: EventType, listener: Listener) -> None:
    _listeners[event_type].append(listener)


def emit_event(event_type: EventType, **payload: Any) -> None:
    for listener in _listeners[event_type]:
        try:
            listener(payload)
        except Exception as exc:
            # don't crash the main flow
            print(f"[event_engine] Listener error for {event_type}: {exc}")
