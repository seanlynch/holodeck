# built in
from dataclasses import dataclass
import re

# mine
from .llm_apis.kobold import KoboldClient
from . import template


@dataclass
class LlmResponse:
    trim_history: int
    response: str


class Prompter:
    stop_pattern = re.compile(r"```|###|</")

    def __init__(
        self,
        llm_client: KoboldClient,
        template: template.Template,
        autoextend: bool = False,
    ):
        self.llm_client = llm_client
        assert llm_client.max_length is not None
        self.max_length = llm_client.max_length
        assert llm_client.max_context_length is not None
        self.max_context_length = llm_client.max_context_length
        self.template = template
        self.autoextend = autoextend

    async def prompt(
        self,
        system_prompt: str,
        prompt: str,
        prefix: str = "",
        previous: str = "",
        history=[],
        history_start: int = 0,
    ) -> LlmResponse:
        response = previous
        trim = history_start
        while True:
            trimmed_history = history[trim:]
            p = self.template(
                system_prompt=system_prompt,
                history=trimmed_history,
                prompt=prompt,
                prefix=prefix,
                prev=response,
            )
            tokens = await self.llm_client.tokencount(p)
            if tokens + self.max_length > self.max_context_length:
                # Overflowed. Trim history.
                trim += 1
                continue

            new = await self.llm_client.generate(p)
            if not new:
                break

            response += new
            m = self.stop_pattern.search(response)
            if m is not None:
                response = response[: m.start(0)]
                break

            if not self.autoextend:
                break

        return LlmResponse(trim, response.strip())
