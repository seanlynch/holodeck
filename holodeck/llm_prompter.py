# built in
import re

# mine
from .llm_apis.kobold import KoboldClient
from . import template


class Prompter:
    stop_pattern = re.compile(r"```|###|</")

    def __init__(
        self,
        llm_client: KoboldClient,
        template: template.Template,
        autoextend: bool = False,
    ):
        self.llm_client = llm_client
        self.template = template
        self.autoextend = autoextend

    async def prompt(
        self,
        system_prompt: str,
        prompt: str,
        prefix: str = "",
        previous: str = "",
        history=[],
    ):
        response = previous
        while True:
            prompt = self.template(system_prompt, history, prompt, prefix, response)
            new = await self.llm_client.generate(prompt)

            if not new:
                return response

            response += new
            m = self.stop_pattern.search(response)
            if m is not None:
                response = response[: m.start(0)]
                break

            if not self.autoextend:
                break

        return response.strip()
