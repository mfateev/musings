# Temporal Activity Design and Execution: Constraints, Patterns, and Recommendations

## Activity Fundamentals

An **Activity** in Temporal is ideally an atomic unit of work—practically, in most languages, it's just a function. This function can contain any logic, use any libraries, and run for as long as necessary. There are no restrictions on duration or capabilities. However, activities are not invoked directly by workflows.

When a workflow schedules an activity, it generates a **ScheduleActivityCommand**. This command is recorded on the Temporal service, and it atomically generates an **activity task** that is placed in a **task queue**. Activity workers long-poll this task queue, receive messages, and execute activities accordingly.

Each worker has a limited number of parallel execution slots. It won't poll for new tasks unless a slot is free. This provides automatic **flow control**. If activities are scheduled faster than workers can process them, the backlog accumulates in the task queue. This backlog can be measured and used as a signal to scale out the number of workers.

---

## Activity Timeouts and Retry Policies

An activity can run for as long as needed. If you want to limit execution time, you can specify timeouts. If an activity fails due to a timeout, it is retried by default.

Each activity has a **retry policy**, with default values:
- Initial retry interval: **1 second**
- Exponential backoff coefficient: **2**
- Maximum retry interval: **100 seconds** (100x the initial interval)

There is **no limit** on total retry duration unless configured.

You can override the retry policy per activity, including the initial interval, backoff coefficient, and maximum retry interval. Additionally, you can specify:
- `scheduleToCloseTimeout`: total time the activity is allowed from scheduling to completion, including retries and queue time.
- `startToCloseTimeout`: maximum duration of each individual activity attempt.

Temporal doesn’t detect worker crashes directly. Failures (including lost tasks) are only detected by **start-to-close timeouts**, so it’s important to set this timeout close to the actual expected execution time. If an activity usually takes 1 second, set the timeout to 1–2 seconds to detect issues quickly.

For long-running or unpredictable-duration activities, this can be problematic—e.g., an activity that runs from 1 minute to 5 hours needs a 5-hour timeout, which also becomes the retry delay. To address this, use **activity heartbeats** with a **heartbeat timeout**. The activity must call the heartbeat API at least once within the timeout window.

---

## Activity Heartbeats

Heartbeats can include **details**—usually progress information. For example, if an activity processes a dataset by paginating over records, it can store the last processed record ID in the heartbeat details. On retry, the activity can resume from that point.

Heartbeats are **buffered** locally and sent to the service at most once every 4/5 of the heartbeat timeout (by default), to reduce database writes. So while you can call `heartbeat()` frequently (even multiple times per millisecond), the data sent to the service will lag slightly. Your code should be **idempotent** to tolerate reprocessing.

---

## Activity Design Considerations

When structuring your application around activities, start with **fine-grained activities**. Each activity should represent a single, well-defined operation with a clear API: input and output. Think of activities like service methods—except that they can take a long time to complete.

### Input/Output Size Limitations

Inputs and outputs are limited to **2 megabytes**. You cannot return large payloads (e.g., PDF files, videos) directly from an activity. Instead:
- Store data externally and pass references.
- For locality-sensitive data, store it locally and route activities to specific hosts using **per-host task queues**.

---

## Task Queues and Routing

The **task queue** determines how activities are grouped and routed:

- **Single queue for multiple activities**: All share the same execution pool and queue. A backlog affects all activities in that queue.
- **Worker-level concurrency**: Each worker controls how many activities it can run in parallel.
- **Worker-level rate limit**: Each worker controls how many activities it can run per second.
- **Glotal task queue rate limiting**: Can be applied per task queue. If your downstream system allows only 100 requests/second, set a queue-wide limit.
- **Global concurrency limit**: Not currently supported; only per-worker concurrency limit exist. A common workaround is to maintain a fixed number of workers and specify per worker limit.


Task queues can also route activities to specific hosts or worker subsets. For example:
- Separate queues for different **GPU types**
- Per-worker queues to route tasks to specific hosts

When using host-specific task queues, specify a **schedule-to-start timeout**. If the host is down and no worker picks up the task, this timeout ensures the activity eventually fails and can be retried or handled differently by the workflow. This timeous is very rarely useful in other scenarios.

---

## Activity Status and Introspection

To check activity progress, use `DescribeWorkflowExecution`. It returns a list of **pending activities**—i.e., activities that have been started but not completed. Each entry includes:
- The **timestamp** of the last heartbeat
- The **heartbeat details**

You can extract this data to display status in a UI or CLI.

---

## Activity Cancellation

Activities can be cancelled if:
- The workflow is cancelled
- Business logic no longer needs the result
- A timeout occurred

Cancellation is a **request**, and the activity may ignore it. However:
- An **in-progress** activity will not be retried if a cancellation request is pending.
- A **retry-scheduled** activity is cancelled immediately if a cancellation is issued.

Cancellation delivery depends on **heartbeats**. A heartbeat call returns a result that includes cancellation status. So:
- If your activity supports cancellation, it **must** heartbeat.
- Cancellation is only known after a heartbeat returns.
- Due to heartbeat buffering, cancellation can be **delayed**.

---

## Language Interoperability

Activities and workflows can be implemented in different languages. As long as **input/output serialization formats** are compatible (e.g., JSON, Protobuf), the system works. There’s no requirement for workflows and activities to be in the same language.

---

## Failure Handling

Activities can fail in various ways:
- In most languages, by **throwing an exception**
- In Go, by **returning an error** or **panicking**

Failures can be:
- **Retriable**
- **Non-retriable**

How errors are classified is SDK-specific. You can also attach a **custom retry interval** to a thrown error if you want to control retry timing without relying solely on the retry policy.

---

## Asynchronous and Manual Activity Completion

Activities are usually **synchronous** or **asynchronous** functions. However, it's also possible to implement **manual completion**.

In manual mode:
- The activity handler returns immediately.
- The worker slot is released.
- The activity is later **completed manually**, potentially from another process.

Example: An activity sends a message to Kafka. When the reply arrives, it completes the activity using the task token.

The Temporal service doesn't require both the **task retrieval** and **completion** to occur in the same process. The task token allows this separation.

---

## Manual Completion Caveats

While manual completion is powerful, it is also **dangerous** and should be used sparingly. A tempting use case is **human approval**:

- Start a manual activity.
- Notify the user.
- Wait for the user to respond.
- Complete the activity from a different process.

However, this design has serious flaws:

- Activities must specify a **start-to-close timeout**, which should match the maximum task duration.
- For human approvals, this might be hours or days.
- If the process crashes after task retrieval but before notifying the user, the task is **lost** until the timeout expires.
- This makes recovery slow and brittle.

What you really need is **two timeouts**:
1. A short timeout for the request-to-user.
2. A long timeout for waiting on the user’s response.

Manual completion only allows one timeout, so this design is inappropriate.

---

## Recommended Pattern for Human Interaction

Instead of manual completion, use:
1. A **short activity** to create a request (e.g., send a message or create a ticket).
2. A **signal** or **workflow update** to handle the user's response.

This avoids long-running activities and enables retries and recovery with short timeouts. The workflow blocks waiting for the signal or update and proceeds once the user responds.