# Workflow Execution Model and Limits in Temporal

The main unit of execution in Temporal is the **workflow**. An individual workflow execution (instance) has limitations in terms of throughput and size. The *size* refers to the total size of the workflow execution history, which in turn limits how long the workflow can run and how many actions it can take. For example:

- A single workflow execution cannot start 100,000 activities.
- A single workflow execution cannot receive 100,000 signals.
- There is a limit on how many updates a workflow can process per second.

At the same time, Temporal scales horizontally with the number of concurrently running workflow executions. This means that while each individual execution has limited capacity, the **overall system throughput can be extremely high** because more workflows can be added and executed in parallel.

If your problem maps naturally to this model of many concurrent executions, each with limited size but potentially complex business logic then Temporal is a perfect fit.

## Ideal Use Cases

### Payments

Executing a payment transaction often involves complex business logic, but typically requires a limited number of activities per transaction. You can run a large number of payments in parallel, making this a good match for Temporal.

### E-commerce Orders

Each order can be modeled as a separate workflow. Orders may involve multi-step processes (payment, shipping, confirmation, etc.), but each individual workflow remains within limits while the system can handle many such workflows in parallel.

## When the Fit Isn't Perfect

If your use case doesn’t fit neatly into this execution model, it’s not the end of the world. However, it does mean that you’ll need to think more carefully about how to **partition** your larger problem into smaller units that conform to Temporal’s workflow limits. Several techniques exist to achieve this, and we will discuss them in this document.

---

# Scenarios That Require Special Consideration

## Payload Size Constraints

Temporal imposes the following size limits:

- Inputs and outputs of workflows and activities are limited to **2 megabytes** each.
- Signals and updates also share this **2 MB** per-message limit.
- Total payload size across all history entries is limited to **50 megabytes**.

Whenever your activities or workflows must handle large data, you will need to apply specific workarounds, such as offloading payloads to external storage or route activities to a host that contains the data.

## Long-Running Loop Workflows

Some workflows implement long loops, such as a **subscription** workflow that sleeps for a month, then charges the user and sends a notification, repeating this cycle indefinitely. These workflows are expected to never end and, over time, will exceed the execution history size limit. Special techniques are required to handle such indefinite lifetimes.

## Reactive Workflows

Reactive workflows listen to **external events** (e.g., signals) and respond by updating their internal state or performing actions. Over a long lifetime, the number of received signals can exceed workflow limits. Additionally, signal **rates** must be considered. If a single workflow instance cannot handle the expected load, one solution is to **partition** the workload by creating multiple workflow instances and **load balancing** the signals across them.

## Large Dataset Processing Workflows

Sometimes a workflow must process a huge dataset, where an activity or child workflow handles each item. If the dataset contains 100,000 or more items, this exceeds workflow limits and requires specific partitioning or external coordination.


---