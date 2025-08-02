"""
Hello Activity Temporal Workflow

This module defines a Temporal workflow that calls an activity to perform business logic.
"""

from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import say_hello


@workflow.defn
class HelloActivityWorkflow:
    """
    A Temporal workflow that demonstrates activity execution patterns.
    
    This workflow:
    1. Calls an activity to generate a greeting with timestamp
    2. Returns the result
    
    This demonstrates the separation of concerns between:
    - Workflow: Orchestration logic (deterministic)
    - Activities: Business logic (can be non-deterministic)
    """
    
    @workflow.run
    async def run(self, name: str = "World") -> str:
        
        # Call the activity to generate greeting with timestamp
        # Configure activity options: timeout, retry policy
        return await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=10),
                maximum_attempts=3,
            ),
        )
