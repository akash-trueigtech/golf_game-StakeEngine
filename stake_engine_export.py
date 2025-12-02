# stake_engine_export.py
# Tools to generate Stake Engine publish bundle:
# - lookup CSV
# - JSONL logic file
# - index.json
# (Works with your golf game engine and serializer)

import json
import csv
import zstandard as zstd
from datetime import datetime

# ----------------------
# 1. WRITE LOGIC JSONL
# ----------------------

def write_logic_jsonl(results, output_path):
    """
    results = list of book objects:
       { id, payoutMultiplier, events, win }
    Writes JSONL file compressed as .jsonl.zst for Stake Engine.
    """

    jsonl_path = output_path + ".jsonl"
    zst_path = output_path + ".jsonl.zst"

    # Write raw jsonl
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    # Compress using Zstandard
    with open(jsonl_path, "rb") as f_in, open(zst_path, "wb") as f_out:
        compressor = zstd.ZstdCompressor(level=10)
        f_out.write(compressor.compress(f_in.read()))

    return zst_path


# ----------------------
# 2. BUILD LOOKUP TABLE
# ----------------------

def build_lookup_table(results):
    """
    Builds a lookup table list of rows:
    [simulation_id, probability_integer, payout_multiplier]

    Probability is computed from count / total, scaled to 64-bit integer space.
    """
    total = len(results)
    counts = {}

    for r in results:
        pm = r["payoutMultiplier"]
        counts[pm] = counts.get(pm, 0) + 1

    # Probability scaling constant from Stake Engine examples
    SCALE = 10**12

    lookup_rows = []
    sim_id = 1

    for r in results:
        pm = r["payoutMultiplier"]
        prob_float = counts[pm] / total
        prob_int = int(prob_float * SCALE)
        lookup_rows.append([sim_id, prob_int, pm])
        sim_id += 1

    return lookup_rows


# ----------------------
# 3. WRITE LOOKUP CSV
# ----------------------

def write_lookup_csv(rows, path):
    """Writes lookup table rows into a CSV (no header)."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


# ----------------------
# 4. WRITE INDEX.JSON
# ----------------------

def write_index_json(mode_name, logic_file, lookup_file, cost_multiplier, output_path):
    index = {
        "mode": mode_name,
        "costMultiplier": cost_multiplier,
        "logicFile": logic_file,
        "lookupFile": lookup_file,
        "created": datetime.utcnow().isoformat() + "Z",
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


# ----------------------
# 5. MAIN EXPORT PIPELINE
# ----------------------

import os

# Ensure library/publish_files exists
PUBLISH_ROOT = os.path.join("library", "publish_files")
os.makedirs(PUBLISH_ROOT, exist_ok=True)

def export_stake_bundle(results, output_prefix, mode_name="normal", cost_multiplier=1):
    """
    results: list of book objects from run_game
    output_prefix: e.g. "exports/golf_normal"
    """

    # 1. Write logic JSONL.ZST
    logic_path = write_logic_jsonl(results, output_prefix + "_logic")

    # 2. Build and write lookup table
    lookup_rows = build_lookup_table(results)
    lookup_csv_path = output_prefix + "_lookup.csv"
    write_lookup_csv(lookup_rows, lookup_csv_path)

    # 3. Write index.json
    index_json_path = output_prefix + "_index.json"
    write_index_json(
        mode_name=mode_name,
        logic_file=logic_path.split("/")[-1],
        lookup_file=lookup_csv_path.split("/")[-1],
        costMultiplier=cost_multiplier,
        output_path=index_json_path,
    )

    return {
        "logic": logic_path,
        "lookup": lookup_csv_path,
        "index": index_json_path,
    }


# ----------------------
# EXAMPLE USAGE
# ----------------------
if __name__ == "__main__":
    from engine import run_game
    from serializer import gamestate_to_book_object

    results = []
    N = 10000
    for i in range(N):
        gs = run_game(bet_amount=1.0)
        results.append(gamestate_to_book_object(gs, id=i+1))

    export_stake_bundle(results, output_prefix="exports/golf_normal")
