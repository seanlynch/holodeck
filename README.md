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
   state. You may not need everything in there.
3. You may also need to install some dependencies for
   [Guidance](https://github.com/guidance-ai/guidance), in particular
   llama-cpp-python with cuBLAS support if you want to use local GGUF
   models. If you don't, you will need to change `app.py` to use
   whatever model type you like (or make it configurable and send me a
   PR).
4. `venv/bin/python -m holodeck.main --model <model>`

## Commands

We now use the LLM to recognize commands. The different command
descriptions given to the LLM are:

1. Create, remove, or change something in the holodeck
2. Retry the last command
3. Print command history
4. Undo the last command
5. Describe the holodeck, look around, print the holodeck description
6. Quit, exit

We print the command the LLM thinks you gave for debugging
purposes. If it always gives 1, something is messed up. I haven't
yet figured out what causes this, but I suspect the model would
otherwise have given a blank response. Try a different model, or try
playing around with the prompt in `app.py` and let me know if you have
any success from changing it.

## Example session

Note that the responses depend a lot on the model and prompt, so you
will probably have to play with those to get reasonable results.

```
$ venv/bin/python -m holodeck --model \
Doctor-Shotgun/airoboros-2.2.1-limarpv3-y34b --transformers
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
