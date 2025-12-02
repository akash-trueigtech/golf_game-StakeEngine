# === FILE: engine.py ===
from symbols.golf_symbols import ZONE1_SYMBOLS, ZONE2_SYMBOLS, ZONE3_SYMBOLS
from gamestate import GameState
import random
from events.events import (
    tee_off_event,
    enter_zone_event,
    hit_result_event,
    final_win_event,
    game_end_event,
)


def run_game(bet_amount: float = 1.0, rng_seed: int = None) -> GameState:
    """Run a single round of the Golf betting game.

    - Player hits once per zone (zones 1 → 3) unless a finalizing symbol occurs earlier.
    - Payouts add bet * multiplier to running_total_win.
    - hard_end sets running_total_win to 0 and ends the game.
    - soft_end ends the game but keeps running_total_win.
    - hole awards its multiplier then ends the game.

    Returns the GameState containing the event book and final running_total_win.
    """

    if rng_seed is not None:
        random.seed(rng_seed)

    gamestate = GameState(bet_amount=bet_amount)

    # Zone 1
    tee_off_event(gamestate)

    # pick zone 1
    z1_index = random.randint(0, len(ZONE1_SYMBOLS) - 1)
    z1_result = ZONE1_SYMBOLS[z1_index]
    hit_result_event(
        gamestate,
        zone=1,
        hit_name=z1_result.code,
        hit_type=z1_result.type,
        multiplier=getattr(z1_result, "multiplier", None) or None,
    )

    # If game ended at zone 1 (hard_end / soft_end / hole) -> finalize
    last = gamestate.book.events[-1]
    if last.get("final"):
        final_win_event(gamestate)
        game_end_event(gamestate, reason=f"Ended at zone 1 with {last.get('hitType')}")
        return gamestate

    # Enter zone 2
    enter_zone_event(gamestate, 2)

    z2_index = random.randint(0, len(ZONE2_SYMBOLS) - 1)
    z2_result = ZONE2_SYMBOLS[z2_index]
    hit_result_event(
        gamestate,
        zone=2,
        hit_name=z2_result.code,
        hit_type=z2_result.type,
        multiplier=getattr(z2_result, "multiplier", None) or None,
    )

    last = gamestate.book.events[-1]
    if last.get("final"):
        final_win_event(gamestate)
        game_end_event(gamestate, reason=f"Ended at zone 2 with {last.get('hitType')}")
        return gamestate

    # Enter zone 3
    enter_zone_event(gamestate, 3)

    z3_index = random.randint(0, len(ZONE3_SYMBOLS) - 1)
    z3_result = ZONE3_SYMBOLS[z3_index]
    hit_result_event(
        gamestate,
        zone=3,
        hit_name=z3_result.code,
        hit_type=z3_result.type,
        multiplier=getattr(z3_result, "multiplier", None) or None,
    )

    last = gamestate.book.events[-1]
    # whether or not final, the game ends after zone 3
    final_win_event(gamestate)
    game_end_event(gamestate, reason=f"Completed zones - last: {last.get('hitType')}")

    return gamestate


if __name__ == "__main__":
    # quick demo runner
    gs = run_game(bet_amount=1.0, rng_seed=42)
    print("Final running_total_win:", gs.running_total_win)
    print("Events:")
    for e in gs.book.events:
        print(e)


# === USAGE NOTES ===
# Save each section above into separate files in a single folder:
# - event_constants.py
# - events.py
# - symbols/golf_symbols.py (create folder `symbols` and save inside)
# - gamestate.py
# - engine.py
# Then run `python engine.py` to run the demo. The engine.run_game function can be
# imported into simulation scripts to run many rounds for RTP calculations.
