from engine import run_game
from serializer import gamestate_to_book_object
from stake_engine_export import export_stake_bundle

def generate_publish_files(rounds=500000):
    results = []
    
    for i in range(rounds):
        gs = run_game(bet_amount=1.0, rng_seed=i)  # deterministic
        book = gamestate_to_book_object(gs, id=i+1)
        results.append(book)
    
    export_stake_bundle(
        results,
        output_prefix="library/publish_files/golf_normal",
        mode_name="normal",
        cost_multiplier=100
    )

if __name__ == "__main__":
    generate_publish_files(rounds=10)
