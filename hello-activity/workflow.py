"""
Hello Activity Temporal Workflow

This module defines a Temporal workflow that calls activities to perform business logic.
"""

from datetime import datetime, timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import say_hello, format_message


@workflow.defn
class HelloActivityWorkflow:
    """
    A Temporal workflow that demonstrates activity execution patterns.
    
    This workflow:
    1. Calls an activity to generate a greeting
    2. Calls another activity to format the message with timestamp
    3. Returns the final formatted result
    
    This demonstrates the separation of concerns between:
    - Workflow: Orchestration logic (deterministic)
    - Activities: Business logic (can be non-deterministic)
    """
    
    @workflow.run
    async def run(self, name: str = "World") -> str:
        """
        The main workflow method that orchestrates activity calls.
        
        Args:
            name: The name to include in the greeting (defaults to "World")
            
        Returns:
            A formatted greeting string with timestamp
        """
        
        # Call the first activity to generate greeting
        # Configure activity options: timeout, retry policy
        greeting = await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=10),
                maximum_attempts=3,
            ),
        )
        
        # Must use workflow.now() instead of datetime.now() inside a workflow
        current_time = workflow.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Call the second activity to format the message
        formatted_message = await workflow.execute_activity(
            format_message,
            args=[greeting, current_time],
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=5),
                maximum_attempts=2,
            ),
        )
        
        return formatted_message