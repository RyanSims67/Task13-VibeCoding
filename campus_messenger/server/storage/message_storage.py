import os
import json

class MessageStorage:
    """
    Handles persisting messages to a JSON file.
    It takes care of creating the directories and file if they do not exist.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """
        Creates the data directory and JSON file if they don't exist yet.
        """
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            self.save_all([])

    def load_all(self) -> list:
        """
        Loads all messages from the JSON file.
        Returns a list of dictionaries.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # In case of corruption or read issues, fall back to an empty list
            return []

    def save_all(self, messages: list):
        """
        Saves the entire list of messages to the JSON file.
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
