Temporal represents a completely different way of thinking about application architecture and design. In this overview, I will cover the high-level principles and how to approach designing a new application using Temporal versus traditional methods.

### Synchronous vs. Asynchronous Design

Typically, when designing an application, you separate it into two parts: synchronous and asynchronous. In the synchronous part, you operate in the world of APIs—REST or other RPC mechanisms. You make synchronous calls, and the code is fairly straightforward: you receive a call, trigger a handler function, which invokes other APIs, processes some data, possibly interacts with a database, and then returns the result.

However, once you need to provide guarantees of execution, handle long-running operations, or perform background processing, you must shift to asynchronous applications. These involve a completely different set of abstractions—events, emitters, and subscribers. The paradigms are so different that you often need to rethink your application entirely.

Event-driven systems are especially complex from a design standpoint. They lack clear, RPC-style APIs. Durability becomes a concern because, in synchronous processing, state is typically stored within function variables, and failures are handled with simple retries. In asynchronous systems, you must think about what happens if the process crashes.

### Temporal and Durable Execution

Temporal offers durable execution, allowing you to stay in the synchronous paradigm much longer. While it’s not the only way to design applications, it is a powerful starting point in many cases. You can think of your system as a set of clearly defined services, each exposing RPC APIs. The key difference is that Temporal guarantees that your synchronous function can run as long as needed. You don’t need to worry about crashes, because state can be safely stored inside the function and variables. Operations can take as long as necessary without shifting to the asynchronous paradigm.

Though integration with fully asynchronous systems or existing async applications is possible, that’s a more advanced topic for later.

### Logical Model vs. Physical Model

When designing with Temporal, it helps to distinguish between the logical and physical models.

- **Logical model**: This is how you conceptualize your application—workflows, activities, Nexus operations, and their corresponding abstractions like signals, updates, and queries. For example, an order processing workflow with five activities is part of the logical design.
  
- **Physical model**: This concerns how components are deployed. You decide which team owns which workflows or activities and map them to specific process pools, services, executables, and namespaces.

Designing the logical model first simplifies your process. Trying to consider both models simultaneously only adds unnecessary complexity.

### Long-Running Durable Functions

Thinking of your system as a collection of long-running functions that cannot crash covers a wide array of scenarios. These functions—workflows—can react to external events through signals or updates and respond to queries. They behave more like **durable actors**: maintaining state, reacting to external stimuli, executing internal logic and timers.

Some workflows, like entity workflows, are long-lived and represent a specific business entity. For instance, a customer account workflow might exist for each customer, handling operations like deposits or withdrawals and performing periodic tasks like sending end-of-month invoices.

### Activities and External Communication

Activities in Temporal are pure functions used to communicate with the external world. Workflows cannot perform direct I/O, so all such interactions must go through activities. Any time a workflow updates external data or calls an external API, it must use an activity. While workflows can return results (e.g., to parent workflows), most workflows primarily sequence activities.

### Design Limitations and Scaling

The main complexity in designing with Temporal stems from understanding the limitations of the execution model:

- **Throughput limits**: A single workflow instance has a limited throughput, generally not exceeding 5–10 signals per second depending on database latency.
- **Data size limits**: Workflows have history size limits and cannot start more than a few thousand activities. Parallelism is also limited—only up to 1,000 activities can run in parallel.
- **Scalability model**: A single workflow has tight limits, but Temporal can scale to support virtually unlimited workflows across many workers. This forces good architectural practices from the beginning, encouraging you to break logic into small, independently scalable units.

- **Payload size limits**: Input/output sizes for workflow arguments, results, activities, heartbeats, signals, and updates have strict limits—typically 2MB maximum (even that is not recommended). Systems should be designed with this constraint in mind.

### Logical and Physical Design Summary

- **Logical design**: It’s conceptually simple. You work with workflows, activities, signals, updates, and child workflows. The key challenge is designing around throughput and size limits.
  
- **Physical design**: Focuses on ownership and deployment, similar to service-oriented architecture. Architecture often mirrors organizational structure (per Conway's Law). For example, if one team owns some workflows or activities, they should own their deployment. Also, resource requirements—such as the need for GPUs or CPU-heavy tasks—can necessitate separation into different deployments. Geographical distribution might also require localized worker pools.

In some cases, physical limitations (like restricting parallel activity execution) may influence your logical design, especially when Temporal lacks built-in support for those constraints.

### Versioning and Upgrades

Finally, upgrades introduce another layer of complexity. You must plan for versioning your workflows and activities. This may require advanced deployment strategies such as **Rainbow Deploys**, which support multiple service versions running simultaneously.