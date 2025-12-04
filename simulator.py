import os
import json
import csv
from engine import run_game
from serializer import gamestate_to_book_object
import random


def run_simulation(rounds=100000, bet=1.0, seed=None):
    books = []               # stores unique book objects
    lookup = {}              # path → lookup info
    total_bet = 0
    total_win = 0

    next_book_id = 1

    for i in range(rounds):

        # run one game
        gs = run_game(bet_amount=bet, rng_seed=None if seed is None else seed + i)
        total_bet += gs.bet_amount
        total_win += gs.running_total_win

        # Convert to book object (temporary id)
        temp_book = gamestate_to_book_object(gs, id=None)
        path = temp_book["path"]

        # Check if path already exists
        if path in lookup:
            lookup[path]["count"] += 1
            continue

        # new unique outcome
        book_id = next_book_id
        next_book_id += 1

        # store new lookup row
        lookup[path] = {
            "id": book_id,
            "path": path,
            "count": 1,
            "payout": gs.running_total_win
        }

        # insert final book object with correct ID
        final_book = gamestate_to_book_object(gs, id=book_id)
        books.append(final_book)

    # Ensure output folder exists
    os.makedirs("library/books", exist_ok=True)

    # === Write books.json ===
    with open("library/books/books103.json", "w") as f:
        json.dump(books, f, indent=2)

    with open("library/books/lookup103.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "weight", "payout"])

        for info in lookup.values():
            writer.writerow([
                info["id"],        # book ID
                info["count"],     # weight
                info["payout"]     # payout in cents
            ])


    # print(list(lookup.keys()))
    print(f"Simulation complete.")
    print(f"Unique outcomes: {len(books)}")
    print(f"books.json and lookup.csv written to /library/books/")
    total_win = total_win/100
    print(f"RTP for {rounds} rounds: {round((total_win/total_bet)*100, 2)}%")



# Run the simulation
if __name__ == "__main__":
    run_simulation(rounds=100000)
