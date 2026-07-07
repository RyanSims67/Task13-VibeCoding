import os
import sys

# Add the workspace root to sys.path so we can import the shared model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from campus_messenger.shared.message_model import Message
from campus_messenger.server.storage.message_storage import MessageStorage

class MessageService:
    """
    Implements business logic for managing messages.
    Interacts with the MessageStorage layer to persist changes.
    """
    def __init__(self, storage: MessageStorage):
        self.storage = storage

    def post_message(self, username: str, room: str, content: str) -> Message:
        """
        Validates and creates a new message, then persists it via storage.
        """
        username = username.strip()
        room = room.strip()
        content = content.strip()

        if not username:
            raise ValueError("Username cannot be empty.")
        if not room:
            raise ValueError("Room name cannot be empty.")
        if not content:
            raise ValueError("Message content cannot be empty.")

        # Create new Message object
        new_msg = Message(username=username, room=room, content=content)

        # Load existing messages, append the new one, and save
        all_messages = self.storage.load_all()
        all_messages.append(new_msg.to_dict())
        self.storage.save_all(all_messages)

        return new_msg

    def get_messages(self, room: str = None) -> list:
        """
        Retrieves messages. If a room is specified, filters messages for that room.
        Returns a list of Message objects.
        """
        all_dict = self.storage.load_all()
        # Convert dictionaries to Message objects
        messages = [Message.from_dict(d) for d in all_dict]

        if room:
            # Filter messages by room (case-insensitive for convenience)
            target_room = room.strip().lower()
            messages = [m for m in messages if m.room.strip().lower() == target_room]

        return messages
