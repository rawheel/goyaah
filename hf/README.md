---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
base_model: nvidia/personaplex-7b-v1
base_model_relation: quantized
library_name: mlx
pipeline_tag: audio-to-audio
language:
- en
tags:
- mlx
- apple-silicon
- full-duplex
- speech-to-speech
- personaplex
- moshi
- 4-bit
- goyaah
---

<p align="center"><img src="https://goyaah.xyz/img/logo.svg" width="96" alt=""></p>
<h1 align="center">Goyaah 7B, MLX 4-bit</h1>
<p align="center">NVIDIA's PersonaPlex 7B, converted and quantized for Apple Silicon.<br>
The model <a href="https://goyaah.xyz">Goyaah</a> runs on a MacBook.</p>

This is **not a new model**. It is [nvidia/personaplex-7b-v1](https://huggingface.co/nvidia/personaplex-7b-v1),
a full-duplex speech-to-speech model NVIDIA fine-tuned from Kyutai's
[Moshi](https://github.com/kyutai-labs/moshi), converted once so that a Mac can run it
without PyTorch, a GPU server, or the 16.7 GB original checkpoint.

What was done to it:

- Weights converted from NVIDIA's PyTorch checkpoint to MLX and quantized to 4 bits
  (group size 64). 16.7 GB became 5.2 GB.
- Only the 8 depformer slices that generate the agent's audio are kept. The checkpoint's
  other 8 predict the user's audio, which is always given during a conversation, so dropping
  them changes nothing in the output.
- The 18 voice prompts converted from PyTorch pickles to safetensors.
- The conversion is checked against NVIDIA's frame-by-frame path (`goyaah-bench verify-prefill`).

## Use it

The files are what [Goyaah](https://github.com/rawheel/goyaah) loads. On an Apple Silicon Mac
with 16 GB of memory or more:

```bash
git clone https://github.com/rawheel/goyaah
cd goyaah
uv venv --python 3.12 && uv pip install -e .
.venv/bin/goyaah-download     # fetches this repo, about 5.6 GB
.venv/bin/goyaah-serve        # then open http://localhost:8998
```

No Hugging Face account is needed for the download. Goyaah talks to the model at one step per
80 ms frame; on an M4 Pro a step takes 26 ms and the model uses about 7 GB of memory.

## Files

| File | What | Size |
|---|---|---|
| `model.q4.safetensors` | PersonaPlex 7B, 4-bit MLX weights | 5.2 GB |
| `tokenizer-e351c8d8-checkpoint125.safetensors` | Mimi codec (Kyutai), 24 kHz, 12.5 Hz, 8 codebooks | 385 MB |
| `tokenizer_spm_32k_3.model` | text tokenizer (Kyutai) | 0.5 MB |
| `voices/*.safetensors` | NVIDIA's 18 voice prompts, embeddings and token cache | 7.5 MB |

Weights are loaded by `goyaah.engine.Engine`; the layout follows Kyutai's `moshi_mlx`, so a
`moshi_mlx` user will find the parameter names familiar. Not loadable by `transformers`.

## Limits

Same as PersonaPlex: English only, no tool use, knows only what is in its prompt, and 4-bit
quantization costs a little quality next to the bf16 original (an 8-bit conversion is a
`goyaah-convert --bits 8` away if your Mac has the memory).

## License and credit

Licensed by NVIDIA Corporation under the NVIDIA Open Model License. The license text is in
`LICENSE`; the attribution is in `NOTICE.md`. PersonaPlex is NVIDIA's work. Moshi, the Mimi
codec and the text tokenizer are Kyutai's (CC-BY 4.0). Goyaah is an independent project,
not affiliated with or endorsed by NVIDIA or Kyutai.

If you use the model in research, cite PersonaPlex and Moshi:

```bibtex
@article{personaplex2026,
  title={PersonaPlex: Voice and Role Control for Full Duplex Conversational Speech Models},
  author={NVIDIA},
  year={2026},
  url={https://github.com/NVIDIA/personaplex}
}
@article{defossez2024moshi,
  title={Moshi: a speech-text foundation model for real-time dialogue},
  author={D{\'e}fossez, Alexandre and Mazar{\'e}, Laurent and Orsini, Manu and Royer, Am{\'e}lie and P{\'e}rez, Patrick and J{\'e}gou, Herv{\'e} and Grave, Edouard and Zeghidour, Neil},
  journal={arXiv preprint arXiv:2410.00037},
  year={2024}
}
```
