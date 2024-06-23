from dataclasses import dataclass
from typing import Union, Optional


@dataclass(frozen=True, slots=True)
class Period:
    discount: int
    period: int


@dataclass(frozen=True, slots=True)
class DataCenter:
    id: int
    city: str
    core_price: float
    country: str
    cpu_name: str
    dc_name: str
    description: str
    disk_price: float
    eth: str
    flag: str
    frequency: str
    info_name: str
    ip_price: Union[int, float]
    ipv6: bool # ipv6id
    max_core: int
    max_disk: int
    max_ram: int
    name: str
    periods: Optional[list[Period]]
    ping_domain: str # pingdomain
    presets: list[int]
    ram_price: Union[int, float]
    title: str
    type_ram: Optional[str]
    need_verification: bool # verif



