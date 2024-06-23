from dataclasses import dataclass
from typing import Optional

from FourVps.types.DataCenters import DataCenter


@dataclass(frozen=True, slots=True)
class ClusterInfo(DataCenter):
    pass


@dataclass(frozen=True, slots=True)
class AvailableUpgradePreset:
    cpu_number: int
    id: int
    name: str
    name_full: Optional[str]
    price: float
    ram: int
    ram_mib: int
    rom: int
    rom_mib: int


@dataclass(frozen=True, slots=True)
class OsInfo:
    id: int
    name: str


@dataclass(frozen=True, slots=True)
class Preset:
    id: int
    name: str
    name_full: str
    cpu_name: str # commentParsed[cpu_name]
    eth: str # commentParsed[eth]
    frequency: str # commentParsed[frequency]
    price: float # commentParsed[price]
    cpu_number: int
    dc_id: int
    available_upgrade_presets: Optional[list[AvailableUpgradePreset]]
    os_list: list[OsInfo]
    ram_mib: int
    rom: int


@dataclass(frozen=True, slots=True)
class TariffPreset(Preset):
    pass


@dataclass(frozen=True, slots=True)
class Tariff:
    cluster_info: ClusterInfo
    presets: list[Preset]


@dataclass(frozen=True, slots=True)
class GetAvailableUpgradePresets:
    id: int
    name: str
    name_full: str
    price: float
    cpu_number: int
    ram_mib: int
    rom_mib: int
    ram: int
    rom: int
