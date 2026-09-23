"""Package dispatch and agent assignment module."""

from typing import Dict, List
from src.distance import euclidean_distance
from src.models import Agent, Package, Warehouse


class Dispatcher:
    """Assigns packages to delivery agents based on initial proximity to pickup warehouses."""

    @staticmethod
    def assign_packages(
        warehouses: Dict[str, Warehouse],
        agents: Dict[str, Agent],
        packages: List[Package],
    ) -> Dict[str, List[Package]]:
        """Map every package to the agent closest to the origin warehouse."""
        if not agents:
            raise ValueError("Cannot assign packages with zero agents available.")

        assignments: Dict[str, List[Package]] = {a_id: [] for a_id in agents}

        for pkg in packages:
            if pkg.warehouse_id not in warehouses:
                raise KeyError(
                    f"Warehouse '{pkg.warehouse_id}' referenced by package '{pkg.id}' not found."
                )

            wh_loc = warehouses[pkg.warehouse_id].location

            # Determine nearest agent by initial starting location
            nearest_agent_id = min(
                agents.keys(),
                key=lambda a_id: euclidean_distance(agents[a_id].initial_location, wh_loc),
            )
            assignments[nearest_agent_id].append(pkg)

        return assignments
