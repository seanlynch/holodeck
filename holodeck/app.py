# built in
import re

# third party
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout

# mine
from .llm_prompter import Prompter
from .llm_apis.kobold import KoboldClient
from . import template


class App:
    def __init__(self):
        self.prompter = None
        self.world = "An empty holodeck."
        self.history = [
            template.HistoryEntry(
                "Create a table.",
                "The holodeck is empty save for a simple square wooden table in the center of the floor.",
            ),
            template.HistoryEntry(
                "Create a blue sky overhead.",
                "There is a simple square wooden table in the center of the holodeck floor. A blue sky stretches overhead, merging with the holodeck walls and floor in the distance.",
            ),
            template.HistoryEntry(
                "Clear the holodeck.",
                self.world,
            ),
        ]
        self.min_history = len(self.history)
        self.trim = 0

    async def connect(self):
        llm_client = KoboldClient(
            "http://localhost:5001/api", settings={"min_p": 0.07, "temperature": 0.9}
        )
        await llm_client.connect()
        self.prompter = Prompter(
            llm_client, template=template.LIMARP3_SHORT, autoextend=True
        )

    def pop_history(self):
        if len(self.history) < self.min_history:
            return None

        if self.trim > 0:
            # Trim 1 fewer history items off. Not precise, but close
            # enough.
            self.trim -= 1

        return self.history.pop()

    async def run(self):
        await self.connect()

        session = prompt_toolkit.PromptSession()
        while True:
            with patch_stdout():
                command = await session.prompt_async("> ")

            command = command.strip()
            if not command:
                print(f"World: {self.world}")
                continue

            if command.startswith("/"):
                match command:
                    case "/regen":
                        h = self.pop_history()
                        if h is None:
                            print("Nothing to regenerate.")
                        else:
                            command = h.prompt
                            self.world = self.history[-1].response
                            await self.update_world(command)
                    case "/undo":
                        h = self.pop_history()
                        if h is None:
                            print("Nothing left to undo.")
                        else:
                            self.world = h.response
                    case "/history":
                        for history_item in self.history:
                            print(history_item)
                    case _:
                        print(f"Unrecognized command {command}")
            else:
                await self.update_world(command)

    async def update_world(self, command):
        system_prompt = f"""\
You are the Enterprise computer from Star Trek: The Next Generation. You are controlling the holodeck. Update the holodeck world description according to the following request. Do not make any changes to the scene not requested by the user. Write only the new description of the world and all objects in it. Make sure to keep any existing objects.

Current world description:
{self.world}
"""
        r = await self.prompter.prompt(
            system_prompt=system_prompt,
            prompt=command,
            prefix="New world description:\n",
            history=self.history,
            history_start=self.trim,
        )

        self.history.append(template.HistoryEntry(command, r.response))
        self.world = r.response
        self.trim = r.trim_history
        print(r.response)
