"""Limited vehicle resource management with synchronization."""

import threading
import time


class VehicleManager:
    """Manages a fixed pool of collection vehicles."""

    def __init__(self, vehicle_count=2):
        self.available_vehicles = [
            f"Vehicle-{number}" for number in range(1, vehicle_count + 1)
        ]
        self.lock = threading.Lock()
        self.completed = []
        self.skipped = []

    def acquire_vehicle(self):
        """Safely acquire one shared vehicle resource."""
        with self.lock:
            if self.available_vehicles:
                return self.available_vehicles.pop(0)
            return None

    def release_vehicle(self, vehicle):
        """Safely return a vehicle to the shared resource pool."""
        with self.lock:
            self.available_vehicles.append(vehicle)

    def process_task(self, task):
        """
        Simulate a collection operation.
        The lock protects the shared vehicle pool.
        """
        vehicle = self.acquire_vehicle()

        if vehicle is None:
            task.status = "Waiting for vehicle"
            with self.lock:
                self.skipped.append(task)
            return

        task.vehicle = vehicle
        task.status = "Collecting"

        print(
            f"[START] {vehicle} -> {task.bin_id} "
            f"({task.location}, {task.fill_level:.0f}%)"
        )

        # Simulation delay; real systems would perform actual work here.
        time.sleep(0.5)

        task.status = "Completed"
        with self.lock:
            self.completed.append(task)

        print(f"[DONE ] {vehicle} -> {task.bin_id}")

        self.release_vehicle(vehicle)

    def run_concurrent_collection(self, tasks):
        """Process scheduled tasks concurrently using worker threads."""
        threads = []

        for task in tasks:
            thread = threading.Thread(
                target=self.process_task,
                args=(task,),
                name=f"Process-{task.bin_id}",
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
