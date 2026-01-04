"""
Minimal chat interface UI using prompt_toolkit.

This module provides a simple terminal-based chat interface where users can
type messages and receive responses from an async function.
"""

import asyncio
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


class ChatUI:
    """
    A minimal terminal-based chat interface.

    Features:
    - Async message input and output
    - Chat history display
    - Clean terminal formatting
    - Support for exit commands (/quit, /exit)
    """

    def __init__(self):
        """
        Initialize the chat UI.

        """
        self.session: PromptSession = PromptSession()
        self.chat_history: list[tuple[str, str]] = []
        self.running = False

    async def generate_response(self, message: str) -> str:
        """
        Placeholder async function that generates a response to a user message.

        This will be implemented later with actual AI/agent logic.

        Args:
            message: The user's input message

        Returns:
            A response string (currently just returns "in progress...")
        """
        # Simulate some processing time
        await asyncio.sleep(1)
        return "in progress..."

    async def get_user_input(self, prompt: str = "You: ") -> Optional[str]:
        """
        Get input from the user asynchronously.

        Args:
            prompt: The prompt string to display

        Returns:
            The user's input string, or None if interrupted
        """
        try:
            with patch_stdout():
                user_input = await self.session.prompt_async(prompt)
            return user_input.strip()
        except (KeyboardInterrupt, EOFError):
            return None

    def display_message(self, role: str, message: str):
        """
        Display a message in the chat.

        Args:
            role: The role/sender of the message (e.g., "You", "AI")
            message: The message content
        """
        print(f"{role}: {message}")

    def display_thinking(self):
        """Display a thinking/loading indicator."""
        print("AI: Thinking...")

    def is_exit_command(self, message: str) -> bool:
        """
        Check if the message is an exit command.

        Args:
            message: The user's input

        Returns:
            True if the message is an exit command
        """
        return message.lower() in ['/quit', '/exit', 'quit', 'exit']

    async def run(self):
        """
        Run the chat interface main loop.

        This method handles the main chat loop:
        1. Display welcome message
        2. Get user input
        3. Check for exit commands
        4. Get response from the response function
        5. Display response
        6. Repeat
        """
        self.running = True

        # Welcome message
        print("=" * 60)
        print("Welcome to the Minimal Chat Interface!")
        print("Type your message and press Enter to chat.")
        print("Type '/quit' or '/exit' to exit, or press Ctrl+C")
        print("=" * 60)
        print()

        try:
            while self.running:
                # Get user input
                user_message = await self.get_user_input("You: ")

                # Handle interruption or empty input
                if user_message is None:
                    print("\nGoodbye!")
                    break

                if not user_message:
                    continue

                # Check for exit command
                if self.is_exit_command(user_message):
                    print("Goodbye!")
                    break

                # Display thinking indicator
                self.display_thinking()

                # Get response from the async function
                try:
                    response = await self.generate_response(user_message)

                    # Clear the "Thinking..." line and display actual response
                    print(f"\rAI: {response}")

                    # Store in history
                    self.chat_history.append((user_message, response))

                except Exception as e:
                    print(f"\rAI: Error generating response: {e}")

                print()  # Empty line for readability

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
        finally:
            self.running = False

    def get_history(self) -> list[tuple[str, str]]:
        """
        Get the chat history.

        Returns:
            List of (user_message, ai_response) tuples
        """
        return self.chat_history.copy()
