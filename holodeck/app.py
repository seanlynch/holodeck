# built in
import re

# third party
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout

# mine
import guidance
from guidance import models, gen, system, user, assistant


class App:
    def __init__(self, model: str):
        self.llm = models.LlamaCppChat(model, n_gpu_layers=128, device_map="auto")
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
                print(self.world)
                continue

            if command.startswith("/"):
                match command:
                    case "/regen":
                        h = self.pop_history()
                        if h is None:
                            print("Nothing to regenerate.")
                        else:
                            command = h[0]
                            self.world = self.history[-1][1]
                            await self.update_world(command)
                    case "/undo":
                        h = self.pop_history()
                        if h is None:
                            print("Nothing left to undo.")
                        else:
                            self.world = self.history[-1][1]
                            print(self.world)
                    case "/history":
                        for history_item in self.history:
                            print(history_item)
                    case _:
                        print(f"Unrecognized command {command}")
            else:
                await self.update_world(command)

    async def update_world(self, command):
        lm = self.llm
        with system():
            lm += f"Update this holodeck description based on the instructions given, being sure to preserve any existing objects and details that are not explicitly changed or removed."

        with user():
            lm += f"Original description:\n{self.world}\n\nInstructions: {command}"

        with assistant():
            lm += "New description (one paragraph): " + gen(name="new_world", stop="\n")

        new_world = lm["new_world"]
        self.history.append((command, new_world))
        self.world = new_world
        print(new_world)
