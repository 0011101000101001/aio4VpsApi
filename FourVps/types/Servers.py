from dataclasses import dataclass
from typing import Optional

from FourVps.types.DataCenters import DataCenter


@dataclass(frozen=True, slots=True)
class ServerCreated:
    server_id: int
    password: str


@dataclass(frozen=True, slots=True)
class ServerInfo:
    server_id: int
    tid: int
    name: str
    price: float
    dc_id: int
    image: str
    mem: int
    cpu: int
    disk: int
    ipv4: Optional[str]
    status: str
    tariff_name: str
    time: int
    expired: int
    autoprolong: bool
    period: int
    api_order: bool


@dataclass(frozen=True, slots=True)
class AdditionalServerInfo:
    server_info: ServerInfo
    data_center: DataCenter

