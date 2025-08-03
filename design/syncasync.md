## Sync vs Async in Temporal

When designing with Temporal, it's important to understand the relationship between synchronous and asynchronous operations.

Internally, Temporal is a highly asynchronous system. Almost everything is designed to be non-blocking and provides all the benefits of pub/sub, queuing, and async processing. At the same time, it offers high-level abstractions—like activity calls—that appear synchronous and blocking, giving the impression that an RPC can take days to complete. However, understanding what is truly synchronous and what is asynchronous is critical to building and reasoning about workflows correctly. This document is an attempt to clarify that.

### Synchronous Execution: Within a Single Workflow

Most synchronous behavior in Temporal occurs within the context of a single workflow. For example, invoking an activity from within a workflow is usually a synchronous operation. Although activities can be invoked asynchronously—or multiple activities can be invoked concurrently and then waited on—it’s common to call an activity and block until it completes. The same applies to child workflows.

### Asynchronous System Behavior

Across the entire system, most operations are asynchronous. Consider the process of activity invocation:

1. A workflow invokes an activity.
2. This creates a task in an activity task queue.
3. A worker picks up the task and executes the activity function synchronously.
4. Once the function completes, it reports the result to the server.
5. The workflow then becomes unblocked and continues execution.

This creates the effect of synchronous remote invocation. However, the presence of the task queue is essential. If 10 million workflows simultaneously invoke that activity, the activity task queue will receive 10 million tasks. Suppose the combined workers can process 10,000 tasks per second—it will take time to drain the backlog.

Activities from multiple workflows are executed in parallel. Even activities scheduled from the same workflow—if scheduled concurrently—can execute in parallel. If the goal is to increase throughput, you increase the number of concurrently executing activities. If workflows block on activities, increasing the number of parallel workflows improves throughput.

### Example: Starbucks as an Asynchronous System

The classic "Starbucks as an asynchronous system" analogy can be modeled naturally in Temporal. Each customer order is represented by a separate workflow. Each workflow defines a clear sequence of steps for that customer:

1. Place order
2. Make payment
3. Receive drink

If something goes wrong (e.g., payment failure), the drink can be retried or canceled. The entire order lifecycle, including retries and error handling, can be written as a simple synchronous workflow.

However, as the Starbucks analogy highlights, the overall system is asynchronous. When a customer places an order, the workflow may invoke an activity to process the payment. With multiple customers, multiple payment activities are scheduled in parallel and can be executed concurrently.

If there is only one barista making drinks, then all drink preparation tasks are queued in a dedicated task queue with a single worker slot. This means drinks are prepared one at a time. The queue and worker model enforce this sequential execution.

Recent versions of Temporal added support for **fairness** and **priorities**. A high-priority customer can jump the queue, and fairness ensures that a customer ordering 1,000 drinks won’t block another customer ordering just two. This helps maintain responsiveness and throughput across the system.