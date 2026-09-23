"""Report exporter module for JSON and CSV formats."""

import csv
import json
from src.models import SimulationReport


class ReportExporter:
    """Handles serializing simulation reports to JSON and CSV formats."""

    @staticmethod
    def save_json(report: SimulationReport, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)

    @staticmethod
    def save_csv(report: SimulationReport, filepath: str) -> None:
        best_agent = report.best_agent
        fieldnames = [
            "agent_id",
            "packages_delivered",
            "total_distance",
            "efficiency",
            "is_best_agent",
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for agent_id, data in report.agent_reports.items():
                writer.writerow(
                    {
                        "agent_id": agent_id,
                        "packages_delivered": data.packages_delivered,
                        "total_distance": data.total_distance,
                        "efficiency": data.efficiency,
                        "is_best_agent": "YES" if agent_id == best_agent else "NO",
                    }
                )
