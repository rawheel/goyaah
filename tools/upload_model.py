"""Uploads the converted model from ~/.cache/goyaah to Hugging Face.

    .venv/bin/python tools/upload_model.py            # create (private) and upload
    .venv/bin/python tools/upload_model.py --public   # ... and make the repo public

Needs a Hugging Face token with write access, saved by `hf auth login`. Uploads the weights,
the Mimi codec, the text tokenizer and the voices from the cache folder, plus the model card,
LICENSE and NOTICE.md from hf/. Previews and goyaah.json stay local. Re-running only uploads
what changed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import HfApi

from goyaah.convert import DEFAULT_OUT
from goyaah.download import FILES, MODEL_REPO

HERE = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=MODEL_REPO)
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--public", action="store_true", help="make the repo public after the upload")
    args = parser.parse_args()

    api = HfApi()
    me = api.whoami()
    role = (me.get("auth") or {}).get("accessToken", {}).get("role")
    print(f"logged in as {me['name']} (token role: {role})")

    api.create_repo(args.repo, repo_type="model", private=True, exist_ok=True)
    for name in ("README.md", "LICENSE", "NOTICE.md"):
        api.upload_file(path_or_fileobj=HERE / "hf" / name, path_in_repo=name, repo_id=args.repo)
    print("card, license and notice uploaded")

    api.upload_folder(
        folder_path=args.model_dir,
        repo_id=args.repo,
        allow_patterns=FILES,
        commit_message="PersonaPlex 7B converted to 4-bit MLX, Mimi, tokenizer and voices",
    )
    print(f"model uploaded to https://huggingface.co/{args.repo}")

    if args.public:
        api.update_repo_settings(args.repo, private=False)
        print("repo is public")


if __name__ == "__main__":
    main()
