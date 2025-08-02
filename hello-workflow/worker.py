"""
Temporal Worker

This module creates and runs a Temporal worker that can execute the HelloWorldWorkflow.
The worker connects to the Temporal service and polls for workflow tasks.
"""

import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from workflow import HelloWorldWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """
    Main function that creates and runs the Temporal worker.
    
    The worker:
    1. Connects to the Temporal service
    2. Registers the HelloWorldWorkflow
    3. Starts polling for workflow tasks on the specified task queue
    """
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    
    # Run the worker
    worker = Worker(
        client,
        task_queue="hello-world-task-queue",
        workflows=[HelloWorldWorkflow],
    )
    
    logger.info("Starting worker for HelloWorldWorkflow...")
    logger.info("Task queue: hello-world-task-queue")
    logger.info("Press Ctrl+C to stop the worker")
    
    # Run worker until interrupted
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")