import enum


class StateEnum(enum.Enum):
    UNCONFIGURED = 0
    INACTIVE = 1
    ACTIVE = 2
    FINALIZED = 3
    ERROR = 4

    @classmethod
    def from_str(cls, state: str) -> "StateEnum":
        try:
            return cls[state.upper()]
        except KeyError:
            raise ValueError(f"Unknown state {state}")


class TransitionEnum(enum.Enum):
    CONFIGURE = 1
    CLEANUP = 2
    ACTIVATE = 3
    DEACTIVATE = 4
    SHUTDOWN_FROM_UNCONFIGURED = 5
    SHUTDOWN_FROM_INACTIVE = 6
    SHUTDOWN_FROM_ACTIVE = 7
