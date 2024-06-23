from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BackupPeriods:
    period: int
    price: float
