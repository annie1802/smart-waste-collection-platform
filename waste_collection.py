"""Waste-bin and collection-task models."""


class WasteBin:
    """Represents a monitored waste bin."""

    def __init__(self, bin_id, location, fill_level, priority):
        self.bin_id = bin_id
        self.location = location
        self.fill_level = float(fill_level)
        self.priority = int(priority)

    def needs_collection(self, threshold=70):
        return self.fill_level >= threshold

    def __str__(self):
        return (
            f"{self.bin_id} | {self.location} | "
            f"Fill: {self.fill_level:.0f}% | Priority: {self.priority}"
        )


class CollectionTask:
    """Represents a collection process/task created for a waste bin."""

    def __init__(self, waste_bin, task_number):
        self.task_number = task_number
        self.bin_id = waste_bin.bin_id
        self.location = waste_bin.location
        self.fill_level = waste_bin.fill_level
        self.priority = waste_bin.priority
        self.status = "Waiting"
        self.vehicle = None

    def __str__(self):
        return (
            f"Task-{self.task_number} | {self.bin_id} | "
            f"{self.location} | {self.fill_level:.0f}% | "
            f"Priority {self.priority} | {self.status}"
        )
