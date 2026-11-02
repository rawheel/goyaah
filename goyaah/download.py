"""Downloads the ready-made 4-bit MLX model, so there is nothing to convert.

    goyaah-download                       # rawheel/goyaah-7b-mlx-4bit into ~/.cache/goyaah
    goyaah-download --repo someone/other  # another repo with the same layout

The repo holds what `goyaah-convert` produces: the 4-bit weights (5.2 GB), the Mimi codec,
the text tokenizer and the 18 voice prompts as safetensors. About 5.6 GB in all, no Hugging
Face account needed. `goyaah-convert` is the other route: it downloads NVIDIA's original
checkpoint (gated, 16.7 GB) and converts it on your Mac, which you need for 8-bit weights or
if you want to verify the conversion yourself.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from huggingface_hub import snapshot_download

from .convert import DEFAULT_OUT, MIMI, TEXT_TOKENIZER, model_file

MODEL_REPO = "rawheel/goyaah-7b-mlx-4bit"
FILES = ["model.q4.safetensors", MIMI, TEXT_TOKENIZER, "voices/*.safetensors"]


def download(repo: str, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo, allow_patterns=FILES, local_dir=out)
    weights = model_file(out, 4)
    if not weights.exists():
        raise FileNotFoundError(f"{repo} has no {weights.name}; is it a goyaah model repo?")
    (out / "goyaah.json").write_text(json.dumps({"source": repo, "bits": 4}))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=MODEL_REPO, help=f"Hugging Face repo (default: {MODEL_REPO})")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = download(args.repo, args.out)
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file() and ".cache" not in p.parts) / 1e9
    print(f"ready: {out} ({size:.1f} GB). Start the app with goyaah-serve")


if __name__ == "__main__":
    main()
