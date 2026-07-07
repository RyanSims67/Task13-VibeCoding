import os
import sys
import unittest
import tempfile
import json

# Add the workspace root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from campus_messenger.server.storage.message_storage import MessageStorage

class TestMessageStorage(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for storage tests
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close() # Close it so MessageStorage can open it
        self.storage = MessageStorage(self.temp_file.name)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_file_created_initially(self):
        """Verify that the JSON file is initialized as an empty list."""
        self.assertTrue(os.path.exists(self.temp_file.name))
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(data, [])

    def test_save_and_load_messages(self):
        """Verify writing and loading lists of messages."""
        test_data = [
            {"username": "Alice", "room": "Study", "content": "Hello", "timestamp": "2026-01-01 10:00:00"},
            {"username": "Bob", "room": "General", "content": "Hi", "timestamp": "2026-01-01 10:01:00"}
        ]
        self.storage.save_all(test_data)
        
        loaded_data = self.storage.load_all()
        self.assertEqual(len(loaded_data), 2)
        self.assertEqual(loaded_data[0]["username"], "Alice")
        self.assertEqual(loaded_data[1]["content"], "Hi")

    def test_load_corrupted_file(self):
        """Verify that a corrupted or invalid JSON file falls back to an empty list."""
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            f.write("corrupted json data")
        
        loaded_data = self.storage.load_all()
        self.assertEqual(loaded_data, [])

if __name__ == "__main__":
    unittest.main()
