"""
Temporal Worker

This module creates and runs a Temporal worker that can execute workflows and activities.
The worker connects to the Temporal service and polls for both workflow and activity tasks.
"""

import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from workflow import HelloActivityWorkflow
from activities import say_hello, format_message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """
    Main function that creates and runs the Temporal worker.
    
    The worker:
    1. Connects to the Temporal service
    2. Registers the HelloActivityWorkflow and activities
    3. Starts polling for workflow and activity tasks on the specified task queue
    """
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    
    # Run the worker with both workflows and activities
    worker = Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[HelloActivityWorkflow],
        activities=[say_hello, format_message],
    )
    
    logger.info("Starting worker for HelloActivityWorkflow and activities...")
    logger.info("Task queue: hello-activity-task-queue")
    logger.info("Registered workflows: HelloActivityWorkflow")
    logger.info("Registered activities: say_hello, format_message")
    logger.info("Press Ctrl+C to stop the worker")
    
    # Run worker until interrupted
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")