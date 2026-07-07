# Walkthrough - CampusMessenger Implementation

I have completed the implementation of Task C: CampusMessenger, a modular, beginner-friendly distributed chat application.

## Changes Made

Below is a summary of the files created in [campus_messenger](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger):

### Configuration & Package Setup
* Created [requirements.txt](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/requirements.txt): Lists requirements `Flask` and `requests`.
* Created [__init__.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/__init__.py): Top-level module initializer.

### Shared Layer
* Created [shared/message_model.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/shared/message_model.py): Defines the `Message` class with `to_dict` and `from_dict` methods for serialization and deserialization.

### Server Layer
* Created [server/storage/message_storage.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/storage/message_storage.py): Manages reading and writing messages to a local JSON file (configured at `campus_messenger/data/messages.json`). Automatically initializes the directory structure and handles empty files safely.
* Created [server/services/message_service.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/services/message_service.py): Handles business validation (checking for empty fields) and room filtering logic.
* Created [server/routes/message_routes.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/routes/message_routes.py): Flask Blueprint routing `GET /api/messages` and `POST /api/messages` requests to `MessageService`.
* Created [server/app.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/server/app.py): Bootstraps storage, services, and registers API endpoints. Exposes a friendly home index page.

### Client Layer
* Created [client/api_client.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/client/api_client.py): Translates client action requests into HTTP requests to the Flask server, capturing network connection errors cleanly.
* Created [client/gui_client.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/client/gui_client.py): Python Tkinter GUI displaying user parameters, a chat history box, room combo box, filter checkbox, manual refresh button, and text input box. Includes auto-polling of messages every 3 seconds.

### Tests
* Created [tests/test_message_storage.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/tests/test_message_storage.py): Unit tests for the storage layer.
* Created [tests/test_message_service.py](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/tests/test_message_service.py): Unit tests for input validation and filtering in the service layer.

### Documentation
* Created [README.md](file:///c:/Users/ryano/Task13-VibeCoding/campus_messenger/README.md): Beginner-friendly documentation summarizing the project structure, what each file does, and how to run it.

---

## Validation Results

### 1. Automated Tests
I ran the automated unit tests covering the storage and service logic. All tests passed successfully:

```
test_get_messages_filtering (test_message_service.TestMessageService.test_get_messages_filtering)
Verify that messages can be retrieved and filtered correctly by room name. ... ok
test_post_message_invalid_inputs (test_message_service.TestMessageService.test_post_message_invalid_inputs)
Verify that empty inputs throw ValueErrors. ... ok
test_post_message_valid (test_message_service.TestMessageService.test_post_message_valid)
Verify successful creation of a message with valid fields. ... ok
test_file_created_initially (test_message_storage.TestMessageStorage.test_file_created_initially)
Verify that the JSON file is initialized as an empty list. ... ok
test_load_corrupted_file (test_message_storage.TestMessageStorage.test_load_corrupted_file)
Verify that a corrupted or invalid JSON file falls back to an empty list. ... ok
test_save_and_load_messages (test_message_storage.TestMessageStorage.test_save_and_load_messages)
Verify writing and loading lists of messages. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.062s

OK
```

### 2. Manual Verification
You can manually run and test the application with the following steps:
1. Start the backend: `python campus_messenger/server/app.py`.
2. Start the Tkinter client: `python campus_messenger/client/gui_client.py`.
3. Try typing different messages in different rooms (e.g. "General", "Study", or customize).
4. Verify you can toggle the "Filter by selected room" checkbutton to show either only the messages from the currently selected room or all messages in the server history.
5. Open a second client to simulate another student and watch messages refresh in real time.
