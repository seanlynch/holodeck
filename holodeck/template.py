from dataclasses import dataclass


@dataclass
class HistoryEntry:
    prompt: str
    response: str


@dataclass
class Template:
    system_prompt_prefix: str
    input_sequence: str
    output_sequence: str
    last_output_sequence: str

    def __call__(
        self,
        system_prompt: str,
        history: list[HistoryEntry],
        prompt: str,
        prefix: str = "",
        prev: str = "",
    ) -> str:
        history_str = "\n".join(
            f"{self.input_sequence}\n{h.prompt}\n{self.output_sequence}\n{h.response}"
            for h in history
        )
        return f"{self.system_prompt_prefix}\n\n{system_prompt}\n{history_str}{self.input_sequence}\n{prompt}\n{self.last_output_sequence}\n{prefix}{prev}"


LIMARP3_SHORT = Template(
    system_prompt_prefix="Below is an instruction that describes a task. Write a response that appropriately completes the request.",
    input_sequence="\n### Input:",
    output_sequence="\n### Response:",
    last_output_sequence="\n### Response: (length = short)",
)
