"""Core logistics simulation engine."""

import random
from typing import Dict, List, Optional, Tuple
from src.dispatcher import Dispatcher
from src.distance import euclidean_distance
from src.models import Agent, AgentReport, Package, Point, SimulationReport, Warehouse


class SimulationEngine:
    """Executes route simulation and calculates operational efficiency."""

    def __init__(
        self,
        warehouses: Dict[str, Warehouse],
        agents: Dict[str, Agent],
        packages: List[Package],
    ):
        self.warehouses = warehouses
        self.agents = agents
        self.packages = packages

    def run(
        self,
        enable_delays: bool = False,
        midday_agent: Optional[Tuple[str, Point]] = None,
    ) -> SimulationReport:
        """Simulate the full day of deliveries across all assigned routes."""
        # Deep copy agents dictionary for isolated simulation
        current_agents = {
            a_id: Agent(id=a.id, initial_location=a.initial_location)
            for a_id, a in self.agents.items()
        }

        # Handle dynamic mid-day agent joining (Bonus)
        if midday_agent:
            new_id, new_loc = midday_agent
            current_agents[new_id] = Agent(id=new_id, initial_location=new_loc)

        # Assign packages to agents
        assignments = Dispatcher.assign_packages(
            self.warehouses, current_agents, self.packages
        )

        agent_reports: Dict[str, AgentReport] = {}
        active_agents_eff: Dict[str, float] = {}

        for a_id, agent in current_agents.items():
            pkgs = assignments.get(a_id, [])
            total_dist = 0.0
            total_delay = 0.0

            for pkg in pkgs:
                wh_loc = self.warehouses[pkg.warehouse_id].location
                dest_loc = pkg.destination

                # Step 1: Agent moves from current location to warehouse (pickup)
                dist_to_wh = euclidean_distance(agent.current_location, wh_loc)
                # Step 2: Agent moves from warehouse to destination (delivery)
                dist_to_dest = euclidean_distance(wh_loc, dest_loc)

                total_dist += dist_to_wh + dist_to_dest
                # Step 3: Agent position updates to destination
                agent.current_location = dest_loc

                if enable_delays:
                    # Random operational delay between 2 and 15 minutes per package
                    total_delay += round(random.uniform(2.0, 15.0), 2)

            pkg_count = len(pkgs)
            efficiency = round(total_dist / pkg_count, 2) if pkg_count > 0 else 0.0

            report = AgentReport(
                packages_delivered=pkg_count,
                total_distance=round(total_dist, 2),
                efficiency=efficiency,
                total_delay_minutes=round(total_delay, 2) if enable_delays else None,
            )
            agent_reports[a_id] = report

            if pkg_count > 0:
                active_agents_eff[a_id] = efficiency

        # Identify best agent (lowest efficiency score)
        if active_agents_eff:
            best_agent = min(
                active_agents_eff.keys(),
                key=lambda k: (active_agents_eff[k], agent_reports[k].total_distance),
            )
        else:
            best_agent = None

        return SimulationReport(
            agent_reports=agent_reports,
            best_agent=best_agent,
        )
