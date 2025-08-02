"""
Hello World Temporal Activities

This module defines activities that are called by workflows to perform business logic.
Activities are functions that can interact with external systems and are designed to handle failures.
"""

import asyncio
import logging
from temporalio import activity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@activity.defn
async def say_hello(name: str) -> str:
    """
    Activity that generates a personalized greeting message.
    
    This activity demonstrates:
    - Basic activity execution
    - Input parameter handling
    - Return value generation
    - Activity heartbeat (for longer operations)
    
    Args:
        name: The name to include in the greeting
        
    Returns:
        A personalized greeting string
    """
    logger.info(f"Activity started: generating greeting for '{name}'")
    
    # Simulate some processing time
    await asyncio.sleep(2)
    
    # Send heartbeat (important for long-running activities)
    activity.heartbeat("Processing greeting...")
    
    # Generate the greeting
    greeting = f"Hello {name}!"
    
    logger.info(f"Activity completed: generated greeting '{greeting}'")
    return greeting


@activity.defn
async def format_message(greeting: str, timestamp: str) -> str:
    """
    Activity that formats a message with timestamp.
    
    This demonstrates calling multiple activities in sequence.
    
    Args:
        greeting: The greeting message
        timestamp: The timestamp to include
        
    Returns:
        A formatted message with timestamp
    """
    logger.info(f"Activity started: formatting message")
    
    # Simulate processing
    await asyncio.sleep(1)
    
    formatted = f"{greeting} (Generated at {timestamp})"
    
    logger.info(f"Activity completed: formatted message '{formatted}'")
    return formatted