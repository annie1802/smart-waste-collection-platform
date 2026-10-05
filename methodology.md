# Methodology

## 1. Input
Sample waste-bin information is stored in `data/sample_bins.csv`. Each record contains a bin ID, location, fill level, and priority.

## 2. Monitoring and Task Creation
A bin with a fill level of 70% or more is considered ready for collection. A `CollectionTask` is created for each such bin.

## 3. Scheduling
Two scheduling approaches are demonstrated:
- FCFS: tasks are processed in task-creation order.
- Priority Scheduling: lower priority numbers are processed first. Fill level is used as a tie-breaker.

## 4. Resource Management
The system has a limited pool of two collection vehicles. A task must acquire a vehicle before collection can begin.

## 5. Synchronization
Multiple worker threads simulate concurrent collection processes. A `threading.Lock` protects the shared vehicle list and result lists from unsafe simultaneous updates.

## 6. Output
The program displays bin status, schedules, resource allocation, collection completion, and basic interim performance results.

## OS Concept Mapping

| Operating System Concept | Project Implementation |
|---|---|
| Process/task management | `CollectionTask` objects and worker threads |
| CPU scheduling | FCFS and priority scheduling simulation |
| Resource management | `VehicleManager` and limited vehicles |
| Synchronization | `threading.Lock` |
| System coordination | Main program integrates monitoring, scheduling and collection |
