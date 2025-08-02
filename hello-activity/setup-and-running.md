# Setup and Running the Hello Activity Sample

This guide provides step-by-step instructions for setting up and running the Temporal Python Hello Activity sample.

## Prerequisites

1. **Install Temporal Server**: Follow the [Temporal installation guide](https://docs.temporal.io/docs/server/quick-install/)
2. **Python 3.8+**: Ensure you have Python 3.8 or later installed

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Sample

1. **Start Temporal Server** (in a separate terminal):
   ```bash
   temporal server start-dev
   ```

2. **Start the Worker** (in a separate terminal):
   ```bash
   cd hello-activity
   python worker.py
   ```
   
   You should see output indicating the worker is polling for tasks:
   ```
   INFO:__main__:Starting worker for HelloActivityWorkflow and activity...
   INFO:__main__:Task queue: hello-activity-task-queue
   INFO:__main__:Registered workflows: HelloActivityWorkflow
   INFO:__main__:Registered activities: say_hello
   INFO:__main__:Press Ctrl+C to stop the worker
   ```

3. **Run the Starter** (in another terminal):
   ```bash
   cd hello-activity
   python starter.py
   ```
   
   You should see output showing the workflow execution:
   ```
   INFO:__main__:Starting workflow with ID: hello-activity-workflow-001
   INFO:__main__:Input parameter: Temporal
   INFO:__main__:Workflow started. WorkflowId: hello-activity-workflow-001, RunId: ...
   INFO:__main__:Workflow completed successfully!
   INFO:__main__:Result: Hello Temporal! (Generated at 2024-01-15 10:30:45)
   ```

## Expected Activity Execution

During execution, you'll see activity logs in the worker terminal:

```
INFO:activities:Activity started: generating greeting for 'Temporal'
INFO:activities:Activity completed: generated greeting 'Hello Temporal! (Generated at 2024-01-15 10:30:45)'
```

## Temporal Web UI

With Temporal server running, you can view workflow executions at:
http://localhost:8233

This provides visibility into:
- Workflow execution history
- Activity task details and timing
- Retry attempts and failures
- Activity heartbeat information