"""CLI Entry Point for FastBox Logistics Simulator."""

import argparse
import json
import os
from typing import Optional, Tuple
from src.engine import SimulationEngine
from src.exporter import ReportExporter
from src.models import Point
from src.parser import ScenarioParser
from src.visualization import AsciiVisualizer


def run_pipeline(
    input_path: str,
    output_path: str = "report.json",
    csv_output_path: Optional[str] = "report.csv",
    visualize: bool = False,
    enable_delays: bool = False,
    midday_agent: Optional[Tuple[str, Point]] = None,
):
    """Executes the end-to-end simulation pipeline."""
    # 1. Load and parse data
    raw_data = ScenarioParser.load_from_file(input_path)
    warehouses, agents, packages = ScenarioParser.parse(raw_data)

    # 2. Initialize and run simulation
    engine = SimulationEngine(warehouses, agents, packages)
    report = engine.run(enable_delays=enable_delays, midday_agent=midday_agent)

    # 3. Export reports
    ReportExporter.save_json(report, output_path)
    if csv_output_path:
        ReportExporter.save_csv(report, csv_output_path)

    # 4. Optional visualization
    if visualize:
        print("\n" + "=" * 54)
        print(" FASTBOX DISPATCH & ROUTE MAP (ASCII)")
        print("=" * 54)
        print(AsciiVisualizer.render(warehouses, agents, packages))
        print("=" * 54 + "\n")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="FastBox Delivery System - Advanced Logistics Simulator"
    )
    parser.add_argument(
        "--input",
        "-i",
        default="base_case.json",
        help="Path to input scenario JSON (default: base_case.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="report.json",
        help="Path to output JSON report (default: report.json)",
    )
    parser.add_argument(
        "--csv",
        "-c",
        default="report.csv",
        help="Path to output CSV report (default: report.csv)",
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Display ASCII map of warehouses, agents, and package destinations",
    )
    parser.add_argument(
        "--delays",
        "-d",
        action="store_true",
        help="Enable random operational delivery delays",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        return

    report = run_pipeline(
        input_path=args.input,
        output_path=args.output,
        csv_output_path=args.csv,
        visualize=args.visualize,
        enable_delays=args.delays,
    )

    print(f"Simulation completed successfully for: {args.input}")
    print(f"Report saved to: {args.output}")
    if args.csv:
        print(f"CSV report saved to: {args.csv}")
    print("\nSummary Report:")
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    main()
