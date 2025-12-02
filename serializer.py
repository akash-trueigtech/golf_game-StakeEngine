import uuid

def gamestate_to_book_object(gamestate, id):
    """
    Converts a GameState into a Stake-engine-format book object.
    """
    hits = [e["hit"] for e in gamestate.book.events if e["type"] == "hitResult"]
    return {
        # "id": int(uuid.uuid4().int >> 96),   # 32-bit style number
        "id": id,
        "payoutMultiplier": gamestate.running_total_win,
        "events": gamestate.book.events,
        "win": gamestate.bet_amount * (gamestate.running_total_win/100),
        "path": "-".join(hits)
    }

