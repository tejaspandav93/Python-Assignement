"""Domain models for FastBox Delivery System."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Point:
    """Represents a 2D Cartesian coordinate (x, y)."""
    x: float
    y: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @classmethod
    def from_raw(cls, coords: List[float] | Tuple[float, float]) -> "Point":
        return cls(x=float(coords[0]), y=float(coords[1]))


@dataclass
class Warehouse:
    """Represents a physical warehouse where packages originate."""
    id: str
    location: Point


@dataclass
class Agent:
    """Represents a delivery driver."""
    id: str
    initial_location: Point
    current_location: Point = field(init=False)

    def __post_init__(self):
        self.current_location = self.initial_location


@dataclass
class Package:
    """Represents a parcel to be picked up from a warehouse and delivered to a destination."""
    id: str
    warehouse_id: str
    destination: Point


@dataclass
class AgentReport:
    """Performance metrics for an individual agent."""
    packages_delivered: int
    total_distance: float
    efficiency: float
    total_delay_minutes: Optional[float] = None

    def to_dict(self) -> Dict[str, float | int]:
        data = {
            "packages_delivered": self.packages_delivered,
            "total_distance": self.total_distance,
            "efficiency": self.efficiency,
        }
        if self.total_delay_minutes is not None:
            data["total_delay_minutes"] = self.total_delay_minutes
        return data


@dataclass
class SimulationReport:
    """Consolidated summary report of the entire simulation."""
    agent_reports: Dict[str, AgentReport]
    best_agent: Optional[str]

    def to_dict(self) -> Dict[str, Dict[str, float | int] | Optional[str]]:
        res: Dict[str, Dict[str, float | int] | Optional[str]] = {
            k: v.to_dict() for k, v in self.agent_reports.items()
        }
        res["best_agent"] = self.best_agent
        return res
