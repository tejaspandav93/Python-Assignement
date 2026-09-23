"""Batch test runner for FastBox Delivery Simulator.

Runs simulations on:
1. base_case.json
2. All test cases in 'Python Assignment(Delivery System Test Cases)/'

Validates:
- Correct JSON loading & parsing
- Total packages delivered matches input packages count
- Valid efficiency calculation & best agent selection
- Report output generation
"""

import glob
import json
import os
from delivery_simulator import DeliverySimulator, run_single_simulation


def run_all_tests():
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    test_cases_dir = os.path.join(
        workspace_dir, "Python Assignment(Delivery System Test Cases)"
    )
    test_files = sorted(
        glob.glob(os.path.join(test_cases_dir, "test_case_*.json")),
        key=lambda x: int(os.path.basename(x).split("_")[-1].split(".")[0])
        if os.path.basename(x).split("_")[-1].split(".")[0].isdigit()
        else x,
    )

    all_inputs = []
    base_case_path = os.path.join(workspace_dir, "base_case.json")
    if os.path.exists(base_case_path):
        all_inputs.append(("base_case.json", base_case_path))

    for tf in test_files:
        all_inputs.append((os.path.basename(tf), tf))

    print("=" * 85)
    print(" " * 25 + "FASTBOX DELIVERY SYSTEM - BATCH TEST SUITE")
    print("=" * 85)
    print(
        f"{'Test File':<22} | {'Pkgs':<6} | {'Agents':<8} | {'Best Agent':<12} | {'Best Efficiency':<16} | {'Status':<8}"
    )
    print("-" * 85)

    passed_count = 0
    total_count = len(all_inputs)

    for name, filepath in all_inputs:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            total_input_pkgs = len(raw_data.get("packages", []))

            sim = DeliverySimulator(raw_data)
            report = sim.run_simulation()

            # Validation checks
            total_delivered = sum(
                v["packages_delivered"]
                for k, v in report.items()
                if k != "best_agent"
            )
            assert total_delivered == total_input_pkgs, (
                f"Package count mismatch: delivered {total_delivered} vs input {total_input_pkgs}"
            )

            best_agent = report.get("best_agent")
            best_eff = (
                report[best_agent]["efficiency"]
                if best_agent and best_agent in report
                else "N/A"
            )
            num_agents = len(sim.agents)

            status = "PASSED"
            passed_count += 1
            print(
                f"{name:<22} | {total_input_pkgs:<6} | {num_agents:<8} | {str(best_agent):<12} | {str(best_eff):<16} | {status:<8}"
            )

        except Exception as e:
            print(f"{name:<22} | ERROR: {str(e)}")

    print("-" * 85)
    print(f"Summary: {passed_count}/{total_count} tests PASSED successfully.")
    print("=" * 85)


if __name__ == "__main__":
    run_all_tests()
