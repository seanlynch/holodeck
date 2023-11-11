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
        self.world = "An empty holodeck."
        self.prompter = None

    async def connect(self):
        llm_client = KoboldClient("http://localhost:5001/api")
        await llm_client.connect()
        self.prompter = Prompter(
            llm_client, template=template.LIMARP3_SHORT, autoextend=True
        )

    async def run(self):
        await self.connect()

        session = prompt_toolkit.PromptSession()
        response = ""
        prev_command = None

        while True:
            with patch_stdout():
                command = await session.prompt_async("> ")

            command = command.strip()
            if not command:
                print(f"World: {self.world}")
                if response:
                    print(f"Response: {response}")
                continue

            if command.startswith("/"):
                match command:
                    case "":
                        continue
                    case "/regen":
                        command = prev_command
                        response = ""
                    case "/undo":
                        response = ""
                        print(self.world)
                        continue
                    case _:
                        print(f"Unrecognized command {command}")
                        continue
            elif response:
                self.world = response
                response = ""

            response = await self.update_world(command)
            prev_command = command
            print(response)

    async def update_world(self, command):
        system_prompt = f"""\
You are the Enterprise computer from Star Trek: The Next Generation. You are controlling the holodeck. Update the holodeck world description according to the following request. Do not make any changes to the scene not requested by the user. Write only the new description of the world and all objects in it. Make sure to keep any existing objects.

Current world description:
{self.world}
"""
        return await self.prompter.prompt(
            system_prompt=system_prompt,
            prompt=command,
            prefix="New world description:\n",
        )

        return response
