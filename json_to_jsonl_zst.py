import json
import zstandard as zstd

def json_to_jsonl_zst(input_path: str, output_path: str, zstd_level: int = 3):
    """Convert a JSON file with a top-level array into a .jsonl.zst compressed file."""
    
    # Load complete JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must contain a top-level list (array).")

    cctx = zstd.ZstdCompressor(level=zstd_level)
    
    with open(output_path, "wb") as out_f:
        with cctx.stream_writer(out_f) as compressor:
            for obj in data:
                line = json.dumps(obj, ensure_ascii=False)
                compressor.write((line + "\n").encode("utf-8"))

    print(f"Created compressed file: {output_path}")


json_to_jsonl_zst("./library/books/books101.json", "./library/publish_files_custom/books.jsonl.zst")
