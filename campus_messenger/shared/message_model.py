from datetime import datetime

class Message:
    """
    A simple data model representing a chat message.
    It contains the sender's username, the chat room, the message content,
    and a timestamp indicating when the message was sent.
    """
    def __init__(self, username: str, room: str, content: str, timestamp: str = None):
        self.username = username
        self.room = room
        self.content = content
        # If no timestamp is provided, generate the current date and time
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """
        Converts the Message object into a dictionary.
        This is useful for saving to a JSON file or sending over HTTP.
        """
        return {
            "username": self.username,
            "room": self.room,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        """
        Creates a Message object from a dictionary.
        This is useful when loading from a JSON file or parsing HTTP request data.
        """
        return cls(
            username=data.get("username", "Unknown"),
            room=data.get("room", "General"),
            content=data.get("content", ""),
            timestamp=data.get("timestamp")
        )
