"""
Hello World Temporal Activities

This module defines activities that are called by workflows to perform business logic.
Activities are functions that can interact with external systems and are retried on failures.
They are expected to be idempotent.
"""

import asyncio
import logging
from datetime import datetime
from temporalio import activity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@activity.defn
async def say_hello(name: str) -> str:
    logger.info(f"Activity started: generating greeting for '{name}'")
    
    # Simulate some processing time
    await asyncio.sleep(2)
    
    # Get current time (this is allowed in activities, not workflows)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate the greeting with timestamp
    greeting = f"Hello {name}! (Generated at {current_time})"
    
    logger.info(f"Activity completed: generated greeting '{greeting}'")
    return greeting