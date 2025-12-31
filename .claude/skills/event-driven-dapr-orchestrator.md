name: "event-driven-dapr-orchestrator"
description: "Decouples services using Dapr Pub/Sub and Kafka. Implements recurring tasks and background notifications without blocking the main API."
version: "1.0.0"
---
# How This Skill Works
1. Sets up Dapr sidecars for the Frontend and Backend pods.
2. Configures a Kafka component in Dapr for the `task-events` topic.
3. Implements a "Notification Service" that consumes events when a task is created or due.
4. Uses Dapr Cron Bindings to trigger the "Recurring Task" logic every midnight.
5. Abstract direct DB calls into Dapr State Store calls where appropriate.

# Deliverables
- Dapr component YAMLs (pubsub.yaml, statestore.yaml).
- Kafka Producer logic in the Backend.
- Background 'worker' service for processing reminders.