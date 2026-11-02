# Notice

Licensed by NVIDIA Corporation under the NVIDIA Open Model License.

These files are a conversion of [nvidia/personaplex-7b-v1](https://huggingface.co/nvidia/personaplex-7b-v1)
(NVIDIA Open Model License, see LICENSE) to 4-bit MLX weights for Apple Silicon, made by
Raheel Siddiqui for [Goyaah](https://goyaah.xyz). The model weights were not retrained; they
were quantized. The voice prompts are NVIDIA's, converted from PyTorch archives to safetensors.

PersonaPlex was fine-tuned by NVIDIA from Kyutai's
[Moshi](https://github.com/kyutai-labs/moshi) weights (moshiko, CC-BY 4.0). The Mimi codec
weights (`tokenizer-e351c8d8-checkpoint125.safetensors`) and the text tokenizer are Kyutai's,
released under CC-BY 4.0. Copyright (c) Kyutai.

Goyaah is an independent project, not affiliated with or endorsed by NVIDIA or Kyutai.
