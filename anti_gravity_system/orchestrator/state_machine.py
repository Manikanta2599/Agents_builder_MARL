from enum import Enum, auto
from typing import Dict, Any

class AgentState(Enum):
    IDLE = auto()
    OBSERVING = auto()
    THINKING = auto()
    PLANNING = auto()
    DELEGATING = auto()
    CRITIQUING = auto()
    COMPLETED = auto()
    ERROR = auto()

class OrchestratorStateMachine:
    def __init__(self):
        self.current_state = AgentState.IDLE
        self.history = []

    def transition(self, new_state: AgentState, metadata: Dict[str, Any] = None):
        """
        Transitions to a new state and logs the change.
        """
        self.history.append({
            "from": self.current_state.name,
            "to": new_state.name,
            "metadata": metadata or {}
        })
        self.current_state = new_state

    def get_history(self):
        return self.history
