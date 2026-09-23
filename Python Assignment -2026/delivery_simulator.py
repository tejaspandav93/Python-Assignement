"""FastBox Delivery System Simulator (Standalone / Backward-Compatible Adapter).

This module provides the DeliverySimulator class and CLI interface, fully powered
by the modular `src` architecture.
"""

from typing import Any, Dict, List, Optional, Tuple
from src.dispatcher import Dispatcher
from src.distance import euclidean_distance
from src.engine import SimulationEngine
from src.exporter import ReportExporter
from src.models import Agent, Package, Point, SimulationReport, Warehouse
from src.parser import ScenarioParser
from src.visualization import AsciiVisualizer


def calculate_euclidean_distance(
    p1: Tuple[float, float], p2: Tuple[float, float]
) -> float:
    """Calculate 2D Euclidean distance between two coordinate tuples."""
    pt1 = Point(float(p1[0]), float(p1[1]))
    pt2 = Point(float(p2[0]), float(p2[1]))
    return euclidean_distance(pt1, pt2)


class DeliverySimulator:
    """Core logistics simulation engine for FastBox."""

    def __init__(self, data_source: Any):
        if isinstance(data_source, str):
            raw_data = ScenarioParser.load_from_file(data_source)
        elif isinstance(data_source, dict):
            raw_data = data_source
        else:
            raise TypeError("data_source must be a file path string or a dictionary.")

        self._raw_data = raw_data
        self._warehouses, self._agents, self._packages = ScenarioParser.parse(raw_data)

    @property
    def warehouses(self) -> Dict[str, Tuple[float, float]]:
        return {k: v.location.to_tuple() for k, v in self._warehouses.items()}

    @property
    def agents(self) -> Dict[str, Tuple[float, float]]:
        return {k: v.initial_location.to_tuple() for k, v in self._agents.items()}

    @property
    def packages(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": p.id,
                "warehouse": p.warehouse_id,
                "destination": p.destination.to_tuple(),
            }
            for p in self._packages
        ]

    def assign_packages(
        self, agent_pool: Optional[Dict[str, Tuple[float, float]]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Assign each package to nearest agent based on distance from agent start to warehouse."""
        if agent_pool is not None:
            agents_obj = {
                a_id: Agent(id=a_id, initial_location=Point.from_raw(coords))
                for a_id, coords in agent_pool.items()
            }
        else:
            agents_obj = self._agents

        raw_assignments = Dispatcher.assign_packages(
            self._warehouses, agents_obj, self._packages
        )

        return {
            a_id: [
                {
                    "id": p.id,
                    "warehouse": p.warehouse_id,
                    "destination": p.destination.to_tuple(),
                }
                for p in pkgs
            ]
            for a_id, pkgs in raw_assignments.items()
        }

    def run_simulation(
        self,
        enable_delays: bool = False,
        midday_agent: Optional[Tuple[str, Tuple[float, float]]] = None,
    ) -> Dict[str, Any]:
        """Simulate delivery routes for all agents and calculate metrics."""
        midday_obj = None
        if midday_agent:
            midday_obj = (midday_agent[0], Point.from_raw(midday_agent[1]))

        engine = SimulationEngine(self._warehouses, self._agents, self._packages)
        report: SimulationReport = engine.run(
            enable_delays=enable_delays, midday_agent=midday_obj
        )
        return report.to_dict()

    def render_ascii_map(self, width: int = 50, height: int = 20) -> str:
        """Render an ASCII grid representation of warehouses, agents, and package destinations."""
        return AsciiVisualizer.render(
            self._warehouses, self._agents, self._packages, width=width, height=height
        )

    def export_to_csv(
        self, report: Dict[str, Any], filepath: str = "report.csv"
    ) -> None:
        """Export report and top performer metrics to CSV."""
        from src.models import AgentReport, SimulationReport

        agent_reports = {}
        best_agent = report.get("best_agent")
        for k, v in report.items():
            if k == "best_agent":
                continue
            agent_reports[k] = AgentReport(
                packages_delivered=v["packages_delivered"],
                total_distance=v["total_distance"],
                efficiency=v["efficiency"],
                total_delay_minutes=v.get("total_delay_minutes"),
            )
        sim_report = SimulationReport(
            agent_reports=agent_reports, best_agent=best_agent
        )
        ReportExporter.save_csv(sim_report, filepath)


def run_single_simulation(
    input_path: str,
    output_path: str = "report.json",
    csv_output_path: Optional[str] = "report.csv",
    visualize: bool = False,
    enable_delays: bool = False,
    midday_agent: Optional[Tuple[str, Tuple[float, float]]] = None,
) -> Dict[str, Any]:
    from main import run_pipeline

    report = run_pipeline(
        input_path=input_path,
        output_path=output_path,
        csv_output_path=csv_output_path,
        visualize=visualize,
        enable_delays=enable_delays,
        midday_agent=midday_agent,
    )
    return report.to_dict()


def main() -> None:
    from main import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
