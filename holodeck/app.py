# built in
from functools import wraps
import re

# third party
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout
import guidance
from guidance import models, gen, system, user, assistant, select
import transformers
import torch


def retry(f):
    @wraps(f)
    def retry_wrapper(*args, **kwargs):
        i = 0
        while True:
            try:
                return f(*args, **kwargs)
            except RecursionError:
                i += 1
                if i == 10:
                    raise

    return retry_wrapper


class App:
    def __init__(self, llm):
        self.llm = llm
        self.world = "An empty holodeck."
        self.history = [
            (
                "Create a table.",
                "The holodeck is empty save for a simple square wooden table in the center of the floor.",
            ),
            (
                "Create a blue sky overhead.",
                "There is a simple square wooden table in the center of the holodeck floor. A blue sky stretches overhead, merging with the holodeck walls and floor in the distance.",
            ),
            (
                "Put some chairs around the table.",
                "There is a simple square wooden table in the center of the holodeck floor. There are four matching chairs placed around it. A blue sky stretches overhead, merging with the holodeck walls and floor in the distance.",
            ),
            (
                "Clear the holodeck.",
                self.world,
            ),
        ]
        self.min_history = len(self.history)
        self.trim = 0

    def pop_history(self):
        if len(self.history) < self.min_history:
            return None

        if self.trim > 0:
            # Trim 1 fewer history items off. Not precise, but close
            # enough.
            self.trim -= 1

        return self.history.pop()

    async def run(self):
        session = prompt_toolkit.PromptSession()
        while True:
            with patch_stdout():
                command = await session.prompt_async("> ")

            command = command.strip()
            if not command:
                continue

            c = self.get_command(command)

            print(f"Command number: {c}")

            match c:
                case "2":
                    h = self.pop_history()
                    if h is None:
                        print("Nothing to regenerate.")
                    else:
                        command = h[0]
                        self.world = self.history[-1][1]
                        self.update_world(command)
                case "4":
                    h = self.pop_history()
                    if h is None:
                        print("Nothing left to undo.")
                    else:
                        self.world = self.history[-1][1]
                        print(self.world)
                case "3":
                    for history_item in self.history:
                        print(history_item)
                case "1":
                    self.update_world(command)
                case "5":
                    print(self.world)
                case "6":
                    return

    @retry
    def update_world(self, command):
        with system():
            lm = (
                self.llm
                + "You are the Enterprise computer controlling the holodeck. Update this holodeck description based on the instructions given, being sure to preserve any existing objects and details that are not explicitly changed or removed."
            )

        with user():
            lm += f"Original description:\n{self.world}\n\nInstructions: {command}"

        with assistant():
            lm += "New description (one paragraph):\n" + gen(
                name="new_world", temperature=0.8, stop="\n"
            )

        new_world = lm["new_world"]
        self.history.append((command, new_world))
        self.world = new_world
        print(new_world)

    @retry
    def get_command(self, command):
        with system():
            lm = (
                self.llm
                + """You are the Enterprise computer controlling the holodeck. Please determine what the user is asking you to do from the following list:

1. Create, remove, or change something in the holodeck
2. Retry the last command
3. Print command history
4. Undo the last command
5. Describe the holodeck, look around, print the holodeck description
6. Quit, exit
"""
            )

        with user():
            lm += f"Command: {command}\n"

        with assistant():
            lm += "Answer [1-6]: " "" + select(
                ["1", "2", "3", "4", "5", "6"], name="option"
            )

        return lm["option"]
