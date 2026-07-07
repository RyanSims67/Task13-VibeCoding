# Implementation Plan - CampusMessenger Distributed App

Build a modular, beginner-friendly distributed chat application in the `campus_messenger` directory. The application consists of a Tkinter GUI client, an API client, a Flask server, and JSON-based message storage.

## User Review Required

> [!NOTE]
> **Simplicity and Clarity**: The code is designed to be highly readable, modular, and well-commented to help with explanation. There are no advanced concepts like WebSockets, user accounts, databases, or complex styling.
> **Room Filtering**: The Tkinter GUI will allow users to select or type a room and view messages filtered by that room, or view all messages.

## Proposed Changes

All files to be created or modified are located inside the `campus_messenger` directory.

---

### Shared Data Model

#### [NEW] [message_model.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/shared/message_model.py)
- Define a simple `Message` class representing a single chat message.
- Properties:
  - `username` (str): Name of the sender.
  - `room` (str): Name of the chat room.
  - `content` (str): Message text.
  - `timestamp` (str): Formatted timestamp (e.g., `YYYY-MM-DD HH:MM:SS`).
- Helper methods:
  - `to_dict()`: Serialize message to a dictionary for JSON/HTTP responses.
  - `from_dict(data)`: Deserialize message from a dictionary.

---

### Storage Layer

#### [NEW] [message_storage.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/storage/message_storage.py)
- Define `MessageStorage` class.
- Handles reading from and writing to a JSON file (by default `campus_messenger/data/messages.json`).
- Ensures the data file and parent folder are created automatically.
- Methods:
  - `load_all()`: Returns list of message dictionaries.
  - `save_all(messages_list)`: Writes list of message dictionaries to the JSON file.

---

### Service Layer

#### [NEW] [message_service.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/services/message_service.py)
- Define `MessageService` class.
- Depends on `MessageStorage`.
- Contains core business logic.
- Methods:
  - `post_message(username, room, content)`: Creates a new `Message` object, serializes it, appends it to the storage, and saves.
  - `get_messages(room=None)`: Retrieves list of `Message` objects, optionally filtered by `room`.

---

### Routing & Server Layer

#### [NEW] [message_routes.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/routes/message_routes.py)
- Define a Flask Blueprint `message_bp` containing the REST API endpoints.
- Endpoints:
  - `POST /api/messages`: Accepts JSON body `{ "username": ..., "room": ..., "content": ... }`. Invokes `MessageService.post_message` and returns `201 Created`.
  - `GET /api/messages?room=...`: Invokes `MessageService.get_messages(room)` and returns messages as JSON.

#### [NEW] [app.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/app.py)
- Creates the Flask application instance.
- Initializes `MessageStorage` (configured to point to `campus_messenger/data/messages.json`) and `MessageService`.
- Exposes `MessageService` to the routes blueprint.
- Runs the server on `127.0.0.1:5000`.

---

### Client Layer

#### [NEW] [api_client.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/client/api_client.py)
- Define `CampusMessengerAPIClient`.
- Communicates with the Flask server using the `requests` library.
- Methods:
  - `send_message(username, room, content)`: Sends POST to `/api/messages`.
  - `get_messages(room=None)`: Sends GET to `/api/messages` with optional room filter.
- Gracefully handles connection failures, returning helpful status/error messages.

#### [NEW] [gui_client.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/client/gui_client.py)
- Tkinter-based desktop interface.
- Components:
  - **Connection Status Bar**: Shows if the client can reach the server.
  - **User Configuration Section**: Inputs for Username and Room (with standard room list dropdown like "General", "Study", "Random" + custom room entry).
  - **Message Board**: Scrollable text area showing messages with formatting `[Timestamp] [Room] Username: Message`.
  - **Compose Section**: Text input field and "Send" button.
  - **Control Buttons**: "Refresh" button to manually update chat, and a toggle/dropdown to filter messages by the selected room or display all.
- Background polling: Automatically polls the server every 3 seconds to fetch new messages using `Tkinter.after()`.

---

### Configuration & Package Dependencies

#### [MODIFY] [requirements.txt](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/requirements.txt)
- Add required library dependencies:
  - `Flask==3.0.3` (or any modern Flask version)
  - `requests==2.32.3` (or any modern requests version)

---

### Tests

#### [NEW] [test_message_storage.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/tests/test_message_storage.py)
- Tests `MessageStorage` reading/writing to a temporary file.

#### [NEW] [test_message_service.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/tests/test_message_service.py)
- Tests `MessageService` business logic (creating message, validation, filtering messages by room).

---

### Documentation

#### [MODIFY] [README.md](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/README.md)
- Write documentation explaining the architecture of CampusMessenger and describing what each file does.

## Verification Plan

### Automated Tests
- Run tests using `python -m unittest discover -s campus_messenger/tests` to verify storage and service logic.

### Manual Verification
1. Start Flask Server: Run `python campus_messenger/server/app.py`.
2. Start GUI Client: Run `python campus_messenger/client/gui_client.py` in multiple terminals to simulate different users.
3. Test sending messages from different users and selecting different rooms.
4. Verify room filtering in the GUI.
5. Verify messages are persisted in `campus_messenger/data/messages.json`.
