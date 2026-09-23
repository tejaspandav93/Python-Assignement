"""ASCII Route & Grid Visualizer module."""

from typing import Dict, List, Tuple
from src.models import Agent, Package, Point, Warehouse


class AsciiVisualizer:
    """Renders 2D terminal map displaying warehouses, agents, and package destinations."""

    @staticmethod
    def render(
        warehouses: Dict[str, Warehouse],
        agents: Dict[str, Agent],
        packages: List[Package],
        width: int = 50,
        height: int = 20,
    ) -> str:
        all_points: List[Point] = []
        all_points.extend(w.location for w in warehouses.values())
        all_points.extend(a.initial_location for a in agents.values())
        all_points.extend(p.destination for p in packages)

        if not all_points:
            return "No coordinates available to map."

        xs = [pt.x for pt in all_points]
        ys = [pt.y for pt in all_points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        span_x = max(max_x - min_x, 1.0)
        span_y = max(max_y - min_y, 1.0)

        grid = [["." for _ in range(width)] for _ in range(height)]

        def map_coords(pt: Point) -> Tuple[int, int]:
            gx = int(((pt.x - min_x) / span_x) * (width - 1))
            gy = int(((max_y - pt.y) / span_y) * (height - 1))
            return max(0, min(width - 1, gx)), max(0, min(height - 1, gy))

        # Plot Destinations (D)
        for p in packages:
            gx, gy = map_coords(p.destination)
            grid[gy][gx] = "D"

        # Plot Warehouses (W)
        for w in warehouses.values():
            gx, gy = map_coords(w.location)
            grid[gy][gx] = "W"

        # Plot Agents (A)
        for a in agents.values():
            gx, gy = map_coords(a.initial_location)
            grid[gy][gx] = "A"

        lines = ["+" + "-" * width + "+"]
        for row in grid:
            lines.append("|" + "".join(row) + "|")
        lines.append("+" + "-" * width + "+")
        lines.append(
            f"Legend: [W] Warehouse ({len(warehouses)}) | [A] Agent ({len(agents)}) | [D] Package Destination ({len(packages)})"
        )
        lines.append(f"Bounds: X: [{min_x}, {max_x}], Y: [{min_y}, {max_y}]")
        return "\n".join(lines)
