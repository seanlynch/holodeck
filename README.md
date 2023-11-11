# Holodeck

An experimental attempt at using an LLM to create a "holodeck"
interface like in Star Trek, so you can say things like, "Computer,
create an opponent who can defeat Data" and get a sentient Professor
Moriarty.

## How it works

We present the LLM with a prompt telling it to update a description of
the world based on the user's command, then replace the world
description with its output. We keep a history seeded with examples so
that it knows how to respond, and feed it as many history entries as
we can without overflowing the context.

How well this works depends heavily on the model, the prompt
(including any necessary instruct template), your generation settings,
time of day, wind speed, humidity, and barometer reading. It may be
possible to make it work nearly flawlessly with a commercial hosted
model, but so far the most sophisticated model I've tried with is a Yi
finetune with 34 billion parameters running locally.

## How to use

1. Read the code; you'll probably have to modify it to make it do
   anything useful.
2. Create a virtual environment and install the packages from
   `requirements.txt` into it. If you don't know how to do that,
   it's probably best to wait until this software is in a more usable
   state.
3. Start a Kobold Lite API server on port 5001, or change the
   hardcoded address in `app.py`, or even better turn it into a
   command line or config line option and send me a PR, or implement
   some other API in `llm_apis` and send me a PR. Or wait and I'll
   probably do it myself.
4. `venv/bin/python -m holodeck.main`

## Commands

* `/regen` - regenerate the last response
* `/undo` - discard the last response
* `/history` - print current history

Anything else will set the world description to the last response and
attempt to generate a new response based on the world description and
your command. Hitting enter by itself will print the current world
description, and the last response if there is one.

## Example session

Note that the responses depend a lot on the model and prompt, so you
will probably have to play with those to get reasonable results,
though the results seem more stable now that I've implemented history
and added examples to the beginning of the history.

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
