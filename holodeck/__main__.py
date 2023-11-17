# built in
import asyncio

# third party
from guidance import models

# mine
from .app import App


def main():
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument("--model", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--lcpp", action="store_true")
    g.add_argument("--transformers", action="store_true")
    args = p.parse_args()

    if args.lcpp:
        llm = models.LlamaCppChat(args.model, n_gpu_layers=-1, n_ctx=2048)
    else:  # args.transformers
        import torch
        from transformers import BitsAndBytesConfig

        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        llm = models.TransformersChat(args.model, quantization_config=nf4_config)

    app = App(llm=llm)
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
