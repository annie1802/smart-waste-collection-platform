"""Scheduling algorithms used by the prototype."""


def fcfs_schedule(tasks):
    """First-Come, First-Served: preserve task creation order."""
    return sorted(tasks, key=lambda task: task.task_number)


def priority_schedule(tasks):
    """
    Non-preemptive priority scheduling.
    Lower numeric priority means higher priority.
    Task number breaks ties.
    """
    return sorted(tasks, key=lambda task: (task.priority, -task.fill_level, task.task_number))


def average_waiting_position(tasks):
    """Simple scheduling metric based on position in the queue."""
    if not tasks:
        return 0.0
    return sum(index for index, _ in enumerate(tasks)) / len(tasks)
