"""
Simple runner script for the chat interface.

Run this script to start the minimal chat interface:
    python -m library_agent.chat
"""

import asyncio
from library_agent.chat_ui import ChatUI


def main():
    """Main entry point for the chat interface."""
    chat = ChatUI()
    asyncio.run(chat.run())


if __name__ == "__main__":
    main()
