"""Input parsing and schema normalization module.

Handles both JSON schema formats seamlessly:
- Dictionary format (test cases 1-10)
- Array-of-objects format (base_case.json)
"""

import json
from typing import Any, Dict, List, Tuple
from src.models import Agent, Package, Point, Warehouse


class ScenarioParser:
    """Parses and standardizes raw input data into domain models."""

    @staticmethod
    def load_from_file(filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def parse(
        cls, raw_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Warehouse], Dict[str, Agent], List[Package]]:
        warehouses: Dict[str, Warehouse] = {}
        agents: Dict[str, Agent] = {}
        packages: List[Package] = []

        # 1. Parse Warehouses
        raw_warehouses = raw_data.get("warehouses", {})
        if isinstance(raw_warehouses, list):
            for item in raw_warehouses:
                w_id = item["id"]
                warehouses[w_id] = Warehouse(
                    id=w_id, location=Point.from_raw(item["location"])
                )
        elif isinstance(raw_warehouses, dict):
            for w_id, coords in raw_warehouses.items():
                warehouses[w_id] = Warehouse(
                    id=w_id, location=Point.from_raw(coords)
                )

        # 2. Parse Agents
        raw_agents = raw_data.get("agents", {})
        if isinstance(raw_agents, list):
            for item in raw_agents:
                a_id = item["id"]
                agents[a_id] = Agent(
                    id=a_id, initial_location=Point.from_raw(item["location"])
                )
        elif isinstance(raw_agents, dict):
            for a_id, coords in raw_agents.items():
                agents[a_id] = Agent(
                    id=a_id, initial_location=Point.from_raw(coords)
                )

        # 3. Parse Packages
        raw_packages = raw_data.get("packages", [])
        for item in raw_packages:
            p_id = item["id"]
            w_id = item.get("warehouse") or item.get("warehouse_id")
            if not w_id:
                raise ValueError(f"Package '{p_id}' is missing a warehouse ID.")
            packages.append(
                Package(
                    id=p_id,
                    warehouse_id=w_id,
                    destination=Point.from_raw(item["destination"]),
                )
            )

        return warehouses, agents, packages
