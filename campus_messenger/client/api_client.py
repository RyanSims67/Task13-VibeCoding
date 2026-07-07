import requests

class CampusMessengerAPIClient:
    """
    Communicates with the CampusMessenger Flask Server.
    Wraps HTTP requests using the `requests` library.
    """
    def __init__(self, base_url: str = "http://127.0.0.1:5000/api"):
        self.base_url = base_url

    def send_message(self, username: str, room: str, content: str) -> tuple:
        """
        Sends a POST request to create a new message.
        Returns:
            (True, message_dict) on success
            (False, error_message) on failure
        """
        url = f"{self.base_url}/messages"
        payload = {
            "username": username,
            "room": room,
            "content": content
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 201:
                return True, response.json()
            else:
                # Retrieve error message if available in JSON response
                error_msg = response.json().get("error", "Unknown server error")
                return False, error_msg
        except requests.exceptions.ConnectionError:
            return False, "Could not connect to server. Is the Flask server running?"
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"

    def get_messages(self, room: str = None) -> tuple:
        """
        Sends a GET request to retrieve messages. Optionally filters by room.
        Returns:
            (True, messages_list) on success
            (False, error_message) on failure
        """
        url = f"{self.base_url}/messages"
        params = {}
        if room:
            params["room"] = room

        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = response.json().get("error", "Unknown server error")
                return False, error_msg
        except requests.exceptions.ConnectionError:
            return False, "Could not connect to server. Is the Flask server running?"
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"
