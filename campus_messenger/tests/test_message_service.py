import os
import sys
import unittest
import tempfile

# Add the workspace root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from campus_messenger.server.storage.message_storage import MessageStorage
from campus_messenger.server.services.message_service import MessageService

class TestMessageService(unittest.TestCase):
    def setUp(self):
        # Create a temp file for storage configuration
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        
        self.storage = MessageStorage(self.temp_file.name)
        self.service = MessageService(self.storage)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_post_message_valid(self):
        """Verify successful creation of a message with valid fields."""
        msg = self.service.post_message("Alice", "General", "Hello study buddies!")
        self.assertEqual(msg.username, "Alice")
        self.assertEqual(msg.room, "General")
        self.assertEqual(msg.content, "Hello study buddies!")
        self.assertIsNotNone(msg.timestamp)

        # Check that it actually persisted to storage
        all_messages = self.storage.load_all()
        self.assertEqual(len(all_messages), 1)
        self.assertEqual(all_messages[0]["username"], "Alice")

    def test_post_message_invalid_inputs(self):
        """Verify that empty inputs throw ValueErrors."""
        with self.assertRaises(ValueError):
            self.service.post_message("   ", "General", "Hello")  # Empty username
        
        with self.assertRaises(ValueError):
            self.service.post_message("Alice", "", "Hello")  # Empty room
        
        with self.assertRaises(ValueError):
            self.service.post_message("Alice", "General", "   ")  # Empty content

    def test_get_messages_filtering(self):
        """Verify that messages can be retrieved and filtered correctly by room name."""
        self.service.post_message("Alice", "Study", "Focus session starting!")
        self.service.post_message("Bob", "Random", "Anyone want lunch?")
        self.service.post_message("Charlie", "Study", "I'm in.")

        # Test listing all messages (no filter)
        all_msgs = self.service.get_messages()
        self.assertEqual(len(all_msgs), 3)

        # Test filtering to "Study" (case-insensitive checking)
        study_msgs = self.service.get_messages(room="study")
        self.assertEqual(len(study_msgs), 2)
        self.assertEqual(study_msgs[0].username, "Alice")
        self.assertEqual(study_msgs[1].username, "Charlie")

        # Test filtering to "Random"
        random_msgs = self.service.get_messages(room="Random")
        self.assertEqual(len(random_msgs), 1)
        self.assertEqual(random_msgs[0].username, "Bob")

if __name__ == "__main__":
    unittest.main()
