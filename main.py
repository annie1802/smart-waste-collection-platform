"""Entry point for the Smart Waste Collection Platform."""

import csv
from pathlib import Path

from waste_collection import WasteBin, CollectionTask
from scheduling import fcfs_schedule, priority_schedule, average_waiting_position
from resource_management import VehicleManager


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sample_bins.csv"


def load_bins(filename):
    """Load waste-bin records from a CSV file."""
    bins = []

    with open(filename, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            bins.append(
                WasteBin(
                    row["bin_id"],
                    row["location"],
                    row["fill_level"],
                    row["priority"],
                )
            )

    return bins


def create_tasks(bins, threshold=70):
    """Create collection tasks only for bins above the fill threshold."""
    tasks = []
    task_number = 1

    for waste_bin in bins:
        if waste_bin.needs_collection(threshold):
            tasks.append(CollectionTask(waste_bin, task_number))
            task_number += 1

    return tasks


def print_schedule(title, tasks):
    print(f"\n{title}")
    print("-" * len(title))

    for position, task in enumerate(tasks, start=1):
        print(
            f"{position}. {task.bin_id} | "
            f"{task.location} | Fill {task.fill_level:.0f}% | "
            f"Priority {task.priority}"
        )


def main():
    print("SMART WASTE COLLECTION PLATFORM")
    print("-" * 34)

    bins = load_bins(DATA_FILE)
    print(f"Loaded {len(bins)} waste bins.")

    print("\nWASTE BIN STATUS")
    print("-----------------")
    for waste_bin in bins:
        status = "COLLECT" if waste_bin.needs_collection() else "MONITOR"
        print(f"{waste_bin} | Action: {status}")

    tasks = create_tasks(bins)

    print(f"\nCreated {len(tasks)} collection tasks.")

    fcfs = fcfs_schedule(tasks)
    priority = priority_schedule(tasks)

    print_schedule("FCFS SCHEDULING", fcfs)
    print(f"Average waiting position: {average_waiting_position(fcfs):.2f}")

    print_schedule("PRIORITY SCHEDULING", priority)
    print(f"Average waiting position: {average_waiting_position(priority):.2f}")

    print("\nRESOURCE ALLOCATION")
    print("-------------------")
    print("Available resources: 2 collection vehicles")
    print("Synchronization: Lock protects the shared vehicle pool.")

    manager = VehicleManager(vehicle_count=2)
    manager.run_concurrent_collection(priority)

    print("\nCOLLECTION SUMMARY")
    print("------------------")
    print(f"Completed tasks: {len(manager.completed)}")
    print(f"Waiting/skipped tasks: {len(manager.skipped)}")

    if manager.completed:
        average_fill = (
            sum(task.fill_level for task in manager.completed)
            / len(manager.completed)
        )
        print(f"Average fill level collected: {average_fill:.1f}%")

    print("\nProject simulation completed successfully.")


if __name__ == "__main__":
    main()
