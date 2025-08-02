"""
Hello World Temporal Activities

This module defines activities that are called by workflows to perform business logic.
Activities are functions that can interact with external systems and are retried on failures.
They are expected to be idempotent.
"""

import asyncio
import logging
from temporalio import activity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@activity.defn
async def say_hello(name: str) -> str:

    logger.info(f"Activity started: generating greeting for '{name}'")
    
    # Simulate some processing time
    await asyncio.sleep(2)
    
    # Generate the greeting
    greeting = f"Hello {name}!"
    
    logger.info(f"Activity completed: generated greeting '{greeting}'")
    return greeting


@activity.defn
async def format_message(greeting: str, timestamp: str) -> str:
    logger.info(f"Activity started: formatting message")
    
    # Simulate processing
    await asyncio.sleep(1)
    
    formatted = f"{greeting} (Generated at {timestamp})"
    
    logger.info(f"Activity completed: formatted message '{formatted}'")
    return formatted