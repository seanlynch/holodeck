# Holodeck

An LLM experiment.

## How to use

1. Read the code; you'll probably have to modify it to make it do
   anything useful.
2. Create a virtual environment and install the packages from
   `requirements.txt` into it. If you don't know how to do that,
   it's probably best to wait until this software is in a more usable
   state.
3. `venv/bin/python -m holodeck.main`

## Commands

* `/extend` - extend the current response
* `/undo` - clear the current response

Anything else will set the world description to the last response and
attempt to generate a new response based on the world description and
your command. Hitting enter by itself will print the current world
description, and the last response if there is one.

## Example session

Note that the responses depend a lot on the model and prompt, so you
will probably have to play with those to get reasonable results. The
model I'm running right now probably embellishes too much.

```
$ venv/bin/python -m holodeck
>
World: An empty holodeck.
> Create a table.
A circular, wooden table with four chairs sits near the center of the room. A bowl of grapes and apples rests on the table.
> Delete the fruit, the bowl, and the chairs.
The circular, wooden table remains in the center of the room, its surface now empty. The four chairs have also been removed from the space.
> Create a blue sky overhead.
A deep, rich shade of azure fills the sky above. Its expanse stretches infinitely into the distance, unbroken by clouds or other disturbances. It reflects off the floor below, creating a mirror image of itself on the polished wood.
>
```

# TODO

* Factor out generation (WIP in `llm_prompter.py`)
* Make instruct templates config-based instead of hardcoded
* Lots of other stuff
