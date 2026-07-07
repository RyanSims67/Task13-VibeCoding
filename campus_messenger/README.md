# CampusMessenger Distributed App

CampusMessenger is a modular, beginner-friendly distributed chat application built in Python using Flask for the server and Tkinter for the client interface.

## Architecture Flow

The basic data flow is as follows:
`Tkinter GUI Client` → `API Client` → `HTTP requests` → `Flask Server` → `Message Routes` → `Message Service` → `Message Storage` → `JSON file`

## File Overview

Here is a brief description of what each file does:

### 1. Root Configuration & Package Setup
- **[requirements.txt](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/requirements.txt)**: Lists the third-party libraries needed (`Flask` and `requests`).
- **[__init__.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/__init__.py)**: Tells Python that the `campus_messenger` directory is a package, allowing modular imports.

### 2. Client Side
- **[client/api_client.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/client/api_client.py)**: Acts as the intermediary API wrapper. It uses the `requests` library to send POST and GET requests to the Flask server, returning a simple success/failure status and response payload. This isolates the networking details from the GUI logic.
- **[client/gui_client.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/client/gui_client.py)**: The graphical user interface built with Tkinter. It allows users to set a username, select or type a chat room, type/send messages, manual refresh, and check/uncheck a filter checkbox to display only messages from the currently selected room or display all. It also automatically polls the server for new messages every 3 seconds.

### 3. Server Side
- **[server/app.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/app.py)**: The entry point for the backend. It sets up Flask, instantiates the storage and service layers, and launches the HTTP server at `http://127.0.0.1:5000`.
- **[server/routes/message_routes.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/routes/message_routes.py)**: Defines the REST API endpoints.
  - `GET /api/messages` to fetch messages (supports an optional `room` query parameter for filtering).
  - `POST /api/messages` to post a new message.
- **[server/services/message_service.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/services/message_service.py)**: Implements business and validation logic. It checks that user fields are not empty, creates message instances, and performs filtering of messages by room name.
- **[server/storage/message_storage.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/storage/message_storage.py)**: Handles loading and saving message lists directly to a JSON file. It automatically ensures the database directory and file exist.

### 4. Shared Layers
- **[shared/message_model.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/shared/message_model.py)**: Defines the `Message` data model class, including serialization and deserialization helpers (`to_dict` and `from_dict`) so messages can easily be saved to disk or sent over HTTP.

### 5. Tests
- **[tests/test_message_storage.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/tests/test_message_storage.py)**: Verifies file creation, saving, and reading logic of the `MessageStorage` layer with a temporary JSON file.
- **[tests/test_message_service.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/tests/test_message_service.py)**: Verifies input validation, message formatting, and room-filtering logic in `MessageService`.

---

## How to Run

### Step 1: Install Dependencies
Run the following command in your terminal from the workspace root:
```bash
pip install -r campus_messenger/requirements.txt
```

### Step 2: Start the Flask Server
Run the backend server:
```bash
python campus_messenger/server/app.py
```
Leave this running in the background. You can open `http://127.0.0.1:5000/` in your browser to verify it is online.

### Step 3: Run the GUI Client
In a new terminal window, start the GUI client:
```bash
python campus_messenger/client/gui_client.py
```
You can open multiple instances of the GUI client in different terminals to simulate multiple users chatting in different rooms.
