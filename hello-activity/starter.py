"""
Workflow Starter

This module demonstrates how to start a Temporal workflow execution that calls activities.
It connects to the Temporal service and initiates the HelloActivityWorkflow.
"""

import asyncio
import logging
from temporalio.client import Client

from workflow import HelloActivityWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """
    Main function that starts the HelloActivityWorkflow.
    
    This function:
    1. Connects to the Temporal service
    2. Starts a new workflow execution
    3. Waits for the workflow to complete
    4. Prints the result
    """
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    
    # Start workflow
    workflow_id = "hello-activity-workflow-001"
    name_input = "Temporal"
    
    logger.info(f"Starting workflow with ID: {workflow_id}")
    logger.info(f"Input parameter: {name_input}")
    
    # Execute the workflow
    handle = await client.start_workflow(
        HelloActivityWorkflow.run,
        name_input,
        id=workflow_id,
        task_queue="hello-activity-task-queue",
    )
    
    logger.info(f"Workflow started. WorkflowId: {handle.id}, RunId: {handle.result_run_id}")
    
    # Wait for workflow completion and get result
    result = await handle.result()
    
    logger.info(f"Workflow completed successfully!")
    logger.info(f"Result: {result}")
    

if __name__ == "__main__":
    asyncio.run(main())