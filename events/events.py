"""
Event builder functions for the Golf betting game.
Creates JSON-ready event objects and appends them to the game state's book.
"""

from .event_constants import EventConstants


def tee_off_event(gamestate):
    """Initial event fired when ball is placed and first hit begins (Zone 1)."""
    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.TEE_OFF.value,
        "zone": 1,
        "description": "Player tees off into Zone 1"
    }
    gamestate.book.add_event(event)


def enter_zone_event(gamestate, zone):
    """Optional event to show transitioning into next zone."""
    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.ENTER_ZONE.value,
        "zone": zone,
        "description": f"Ball enters Zone {zone}"
    }
    gamestate.book.add_event(event)


def hit_result_event(
    gamestate,
    zone: int,
    hit_name: str,
    hit_type: str,  # payout | empty | hard_end | soft_end | hole
    multiplier: float = None,
):
    """Primary event: ball lands somewhere in a zone and produces a result.


    This function will also update the gamestate.running_total_win according to
    the hit_type (payout adds to running total, hard-end wipes it out, soft-end leaves it).
    """


    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.HIT_RESULT.value,
        "zone": zone,
        "hit": hit_name,
        "hitType": hit_type,
        "runningTotalWin": gamestate.running_total_win,
    }

    # include multiplier only if relevant
    if multiplier is not None:
        event["multiplier"] = multiplier


     # --- payout event ---
    if hit_type == "payout":
        win_amount = int(multiplier * 100)
        gamestate.running_total_win += win_amount
        event["runningTotalWin"] = gamestate.running_total_win

    # --- hard-end ---
    elif hit_type == "hard_end":
        gamestate.running_total_win = 0
        event["runningTotalWin"] = 0
        event["final"] = True

    # --- soft-end ---
    elif hit_type == "soft_end":
        event["runningTotalWin"] = gamestate.running_total_win
        event["final"] = True

    # --- hole ---
    elif hit_type == "hole":
        win_amount = int(multiplier * 100)
        gamestate.running_total_win += win_amount
        event["runningTotalWin"] = gamestate.running_total_win
        event["final"] = True

    gamestate.book.add_event(event)


def final_win_event(gamestate):
    """Last event → assigns final payout amount X100 for RGS.


    The stake engine expects amount in integer cents (or percent-of-stake *100 depending on engine).
    We follow the pattern: amount = int(running_total_win * 100)
    """
    event = {
    "index": len(gamestate.book.events),
    "type": EventConstants.FINAL_WIN.value,
    "amount": int(gamestate.running_total_win),
    }

    gamestate.book.add_event(event)


def game_end_event(gamestate, reason: str):
    """Optional explicit termination event."""
    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.GAME_END.value,
        "reason": reason,
        "runningTotalWin": gamestate.running_total_win
    }
    gamestate.book.add_event(event)
