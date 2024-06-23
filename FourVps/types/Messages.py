from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Message:
    id: int
    title: str
    content: str
    time: int
