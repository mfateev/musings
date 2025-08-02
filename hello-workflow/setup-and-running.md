# Setup and Running the Hello World Sample

This guide provides step-by-step instructions for setting up and running the Temporal Python Hello World sample.

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
   cd hello-workflow
   python worker.py
   ```
   
   You should see output indicating the worker is polling for tasks:
   ```
   INFO:__main__:Starting worker for HelloWorldWorkflow...
   INFO:__main__:Task queue: hello-world-task-queue
   INFO:__main__:Press Ctrl+C to stop the worker
   ```

3. **Run the Starter** (in another terminal):
   ```bash
   cd hello-workflow
   python starter.py
   ```
   
   You should see output showing the workflow execution:
   ```
   INFO:__main__:Starting workflow with ID: hello-world-workflow-001
   INFO:__main__:Input parameter: Temporal
   INFO:__main__:Workflow started. WorkflowId: hello-world-workflow-001, RunId: ...
   INFO:__main__:Workflow completed successfully!
   INFO:__main__:Result: Hello Temporal!
   ```

## Temporal Web UI

With Temporal server running, you can view workflow executions at:
http://localhost:8233

This provides visibility into workflow history, execution details, and debugging information.