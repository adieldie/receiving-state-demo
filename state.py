from __future__ import annotations

from enum import Enum
from typing import Any


class LaunchState(str, Enum):
    IDLE = "idle"
    READING_SOURCE = "reading_source"
    MAPPING = "mapping"
    WAITING_MAPPING = "waiting_mapping"
    PLAN_READY = "plan_ready"
    WAITING_CONFIRMATION = "waiting_confirmation"
    SENDING = "sending"
    VALIDATING = "validating"
    RECOVERY = "recovery"
    CONFIRMED = "confirmed"
    INCONCLUSIVE = "inconclusive"
    CANCELLED = "cancelled"
    FAILED = "failed"


_ALLOWED = {
    LaunchState.IDLE: {LaunchState.READING_SOURCE, LaunchState.CANCELLED, LaunchState.FAILED},
    LaunchState.READING_SOURCE: {
        LaunchState.MAPPING,
        LaunchState.PLAN_READY,
        LaunchState.WAITING_MAPPING,
        LaunchState.FAILED,
        LaunchState.CANCELLED,
    },
    LaunchState.MAPPING: {
        LaunchState.READING_SOURCE,
        LaunchState.WAITING_MAPPING,
        LaunchState.PLAN_READY,
        LaunchState.FAILED,
        LaunchState.CANCELLED,
    },
    LaunchState.WAITING_MAPPING: {
        LaunchState.MAPPING,
        LaunchState.READING_SOURCE,
        LaunchState.CANCELLED,
        LaunchState.FAILED,
    },
    LaunchState.PLAN_READY: {
        LaunchState.WAITING_CONFIRMATION,
        LaunchState.SENDING,
        LaunchState.CANCELLED,
        LaunchState.FAILED,
    },
    LaunchState.WAITING_CONFIRMATION: {
        LaunchState.SENDING,
        LaunchState.CANCELLED,
        LaunchState.FAILED,
    },
    LaunchState.SENDING: {
        LaunchState.VALIDATING,
        LaunchState.RECOVERY,
        LaunchState.CANCELLED,
        LaunchState.FAILED,
    },
    LaunchState.VALIDATING: {
        LaunchState.CONFIRMED,
        LaunchState.RECOVERY,
        LaunchState.INCONCLUSIVE,
        LaunchState.FAILED,
    },
    LaunchState.RECOVERY: {
        LaunchState.SENDING,
        LaunchState.VALIDATING,
        LaunchState.INCONCLUSIVE,
        LaunchState.FAILED,
        LaunchState.CANCELLED,
    },
    LaunchState.CONFIRMED: {LaunchState.IDLE},
    LaunchState.INCONCLUSIVE: {LaunchState.IDLE, LaunchState.RECOVERY},
    LaunchState.CANCELLED: {LaunchState.IDLE},
    LaunchState.FAILED: {LaunchState.IDLE, LaunchState.RECOVERY},
}


class LaunchStateMachine:
    def __init__(self) -> None:
        self.state = LaunchState.IDLE
        self.message = ""
        self.history: list[dict[str, Any]] = []

    def transition(self, state: LaunchState, message: str = "") -> LaunchState:
        if state == self.state:
            self.message = message
            return self.state
        allowed = _ALLOWED.get(self.state, set())
        if state not in allowed:
            raise ValueError(
                f"Transição inválida: {self.state.value} -> {state.value}"
            )
        previous = self.state
        self.state = state
        self.message = message
        self.history.append(
            {
                "from": previous.value,
                "to": state.value,
                "message": message,
            }
        )
        return self.state

    def force(self, state: LaunchState, message: str = "") -> LaunchState:
        previous = self.state
        self.state = state
        self.message = message
        self.history.append(
            {
                "from": previous.value,
                "to": state.value,
                "message": message,
                "forced": True,
            }
        )
        return self.state

    def snapshot(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "message": self.message,
            "history": list(self.history[-50:]),
        }

