from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServerIP:
    id: int
    name: str
    ip: str
    ptr: str
