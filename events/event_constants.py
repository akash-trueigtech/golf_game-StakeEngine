"""
Contains all reusable event `type` constants for the Golf betting game.
"""

from enum import Enum


class EventConstants(Enum):
    """Define all standard event 'type' keys used in the golf game."""

    # Game flow events
    TEE_OFF = "teeOff"                 # Start of the round entering Zone 1
    ENTER_ZONE = "enterZone"           # Optional: emitted when moving to next zone
    HIT_RESULT = "hitResult"           # Each ball result (payout / empty / hard-end / soft-end / hole)
    FINAL_WIN = "finalWin"             # Final payout multiplier output
    GAME_END = "gameEnd"               # (optional) explicit end marker for soft/hard-end outcomes

    # Debug / math events (optional)
    STATE_SNAPSHOT = "stateSnapshot"   # Internal testing / debugging snapshot
