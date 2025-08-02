"""
Hello World Temporal Workflow

This module defines a simple Temporal workflow that returns a greeting message.
"""

from temporalio import workflow


@workflow.defn
class HelloWorldWorkflow:
    """
    A simple Temporal workflow that demonstrates basic workflow execution.
    
    This workflow doesn't perform any complex operations - it simply returns
    a "Hello World!" message to demonstrate the basic Temporal workflow pattern.
    """
    
    @workflow.run
    async def run(self, name: str = "World") -> str:
        """
        The main workflow method that executes the business logic.
        
        Args:
            name: The name to include in the greeting (defaults to "World")
            
        Returns:
            A greeting string
        """
        return f"Hello {name}!"