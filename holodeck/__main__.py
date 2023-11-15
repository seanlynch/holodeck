# built in
import asyncio

# mine
from .app import App


def main():
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument("--model", required=True)
    args = p.parse_args()

    app = App(model=args.model)
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
