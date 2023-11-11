# built in
import re

# third party
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout

# mine
from .llm_apis.kobold import KoboldClient
from . import template


class App:
    stop_pattern = re.compile(r"```|###|</")

    def __init__(self):
        self.llm_client = KoboldClient("http://localhost:5001/api")
        self.world = "An empty holodeck."

    async def run(self):
        await self.llm_client.connect()

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
                    case "/extend":
                        command = prev_command
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

            response = await self.update_world(command, response)
            prev_command = command
            print(response)

    async def update_world(self, command, prev):
        system_prompt = f"""\
Current world description:
{self.world}

***

Please update the world description according to the following request. Give a complete description of the world as it exists after the request, keeping any objects which already existed in the world and their complete descriptions. Do not describe any actions or events, only the world and the objects in it."""
        prompt = template.LIMARP3_SHORT(
            system_prompt, [], command, "New world description:\n", prev
        )
        response = prev + await self.llm_client.generate(prompt)
        m = self.stop_pattern.search(response)
        if m is not None:
            response = response[: m.start(0)]

        return response
