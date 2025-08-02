# Temporal Python Hello Activity Sample

This sample demonstrates Temporal workflow patterns using Python with activities. It shows how to:

- Define activities that perform business logic
- Create workflows that orchestrate activity calls
- Configure activity timeouts and retry policies
- Handle activity failures and retries

## Components

### 1. Activities (`activities.py`)
- **say_hello**: Generates a personalized greeting message with simulated processing time
- **format_message**: Formats the greeting with a timestamp
- Demonstrates activity heartbeat for long-running operations
- Shows proper logging and error handling patterns

### 2. Workflow (`workflow.py`)
- **HelloActivityWorkflow**: Orchestrates calls to activities in sequence
- Demonstrates activity configuration (timeouts, retry policies)
- Shows how to pass data between activities
- Uses `workflow.now()` for deterministic time handling

### 3. Worker (`worker.py`)
- Connects to the Temporal service
- Registers both the workflow and activities
- Polls the `hello-activity-task-queue` for both workflow and activity tasks
- Can execute workflow orchestration and activity business logic

### 4. Starter (`starter.py`)
- Creates a Temporal client connection
- Starts a new workflow execution with ID `hello-activity-workflow-001`
- Waits for workflow completion and prints the result

## Sequence Diagram

The following diagram shows the interaction flow between components:

```mermaid
sequenceDiagram
    participant S as Starter
    participant TS as Temporal Service
    participant W as Worker
    
    Note over S,W: Prerequisites: Temporal service running, Worker started
    
    S->>+TS: StartWorkflowExecution<br/>(HelloActivityWorkflow, TaskQueue: hello-activity-task-queue, ID: hello-activity-workflow-001, Input:"Temporal")
    TS-->>-S: Ack
        
    W->>TS: long-poll PollWorkflowTaskQueue (hello-activity-task-queue)
    
    TS->>+W: WorkflowTask<br/>(HelloActivityWorkflow, ID: hello-activity-workflow-001, Input:"Temporal")
    W->>W: Execute HelloActivityWorkflow.run("Temporal")
    W->>W: Schedule say_hello activity
    W-->>-TS: CompleteWorkflowTask(Commands:[<br/>ScheduleActivityTask(say_hello, "Temporal")<br/>])
    
    W->>TS: long-poll PollActivityTaskQueue (hello-activity-task-queue)
    
    TS->>+W: ActivityTask<br/>(say_hello, Input:"Temporal")
    W->>W: Execute say_hello("Temporal")
    W->>W: Heartbeat: "Processing greeting..."
    W->>W: return "Hello Temporal!"
    W-->>-TS: CompleteActivityTask(Result:"Hello Temporal!")
    
    TS->>+W: WorkflowTask<br/>(Continue workflow with activity result)
    W->>W: Process activity result
    W->>W: Schedule format_message activity  
    W-->>-TS: CompleteWorkflowTask(Commands:[<br/>ScheduleActivityTask(format_message, "Hello Temporal!", timestamp)<br/>])
    
    TS->>+W: ActivityTask<br/>(format_message, Inputs: greeting, timestamp)
    W->>W: Execute format_message(greeting, timestamp)
    W->>W: return formatted message
    W-->>-TS: CompleteActivityTask(Result: formatted message)
    
    TS->>+W: WorkflowTask<br/>(Continue workflow with final result)
    W->>W: Complete workflow execution
    W-->>-TS: CompleteWorkflowTask(Commands:[<br/>CompleteWorkflowExecution(Result: formatted message)<br/>])
    
    Note over S,W: Workflow execution complete
    
    S->>+TS: long-poll GetResult
    TS-->>-S: Return result: formatted message
```

## Documentation Index

This sample includes several documentation files explaining different aspects of Temporal activity execution:

### 📚 Core Documentation
- **[Setup and Running Guide](setup-and-running.md)** - Step-by-step instructions for running this sample
- **[Activity Failure Scenarios](activity-failure-scenarios.md)** - Analysis of activity-specific failure scenarios and how Temporal handles them

### 🚀 Quick Start
To run this sample immediately, see the **[Setup and Running Guide](setup-and-running.md)**.

## Key Concepts Demonstrated

### Activity Definition
- **Activity Decorator**: `@activity.defn` marks functions as Temporal activities
- **Heartbeat**: `activity.heartbeat()` for long-running operations
- **Input/Output**: Activities receive parameters and return results

### Workflow Orchestration
- **Activity Execution**: `workflow.execute_activity()` to call activities
- **Single Arguments**: Pass single argument directly: `workflow.execute_activity(activity_fn, arg)`
- **Multiple Arguments**: Pass multiple arguments as list: `workflow.execute_activity(activity_fn, args=[arg1, arg2])`
- **Timeout Configuration**: `start_to_close_timeout` for activity execution limits
- **Retry Policies**: Configure retry behavior for failed activities
- **Deterministic Time**: Use `workflow.now()` instead of `datetime.now()`

### Worker Registration
- **Multiple Registration**: Workers can register both workflows and activities
- **Task Queue Polling**: Single worker polls for both workflow and activity tasks
- **Concurrent Execution**: Worker can handle multiple workflow and activity instances

### Activity Benefits
- **Fault Tolerance**: Activities can fail and retry without affecting workflow state
- **External Interactions**: Activities can call external APIs, databases, etc.
- **Resource Management**: Activities can be distributed across different workers
- **Timeout Protection**: Activities have built-in timeout protection