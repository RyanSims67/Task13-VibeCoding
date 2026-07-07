[Back to Task C](README.md)

# Task C — Architecture

This file explains how I structured CampusMessenger.

I tried to keep the architecture simple because I need to understand every file and be able to explain it.

CampusMessenger is split into a client side and a server side. The GUI does not save messages by itself. It sends messages to the Flask server, and the server saves them in a JSON file.

## My App Flow

This is the flow I used for the app:

```text
Tkinter GUI Client
    ↓
API Client
    ↓ HTTP requests
Flask Server
    ↓
Message Routes
    ↓
Message Service
    ↓
Message Storage
    ↓
JSON file
```

## Project Structure

The main code is inside:

```text
campus_messenger/
```

The important folders are:

```text
campus_messenger/
    client/
    server/
    shared/
    tests/
    data/
```

I separated the files because I did not want one large Python file that does everything.

## Client Side

The client side is inside:

```text
campus_messenger/client/
```

It has:

```text
api_client.py
gui_client.py
```

### `gui_client.py`

This is the visible app window.

It creates the CampusMessenger GUI with:

* username input
* chat room selection
* message box
* send button
* manual refresh button
* chat board
* connection status

When I tested it, I opened two GUI windows at the same time. One user was `Student`, and the other user was `John`.

Both clients showed the same messages, which proved that the GUI was not working alone locally. It was getting data from the server.

### `api_client.py`

This file is the connection between the GUI and the Flask server.

The GUI calls this file when it needs to:

* send a message
* get messages
* filter messages by room

I understand this file as the middle step between the desktop app and the backend server.

## Server Side

The server side is inside:

```text
campus_messenger/server/
```

It has:

```text
app.py
routes/message_routes.py
services/message_service.py
storage/message_storage.py
```

### `app.py`

This starts the Flask server.

I used this file when I ran the server from the terminal.

The server has to be running before the GUI client can connect.

### `message_routes.py`

This file contains the Flask routes.

The routes receive requests from the API client.

For example, when the GUI sends a message, the route receives the message data and passes it to the service.

### `message_service.py`

This file contains the main message logic.

It handles things like:

* creating a message
* checking the username, room and content
* getting all messages
* filtering messages by room

I think this file is important because it keeps the logic out of the route file.

### `message_storage.py`

This file handles saving and loading messages.

The messages are stored in:

```text
campus_messenger/data/messages.json
```

This means the messages can stay saved even after closing the program.

## Shared Message Model

The shared model is inside:

```text
campus_messenger/shared/message_model.py
```

This file defines what one message looks like.

A message has:

* username
* room
* content
* timestamp

I used this so the message structure stays consistent.

## Testing Structure

The tests are inside:

```text
campus_messenger/tests/
```

The tests check the service and storage parts.

I ran:

```text
python -m unittest discover -s campus_messenger/tests
```

The result was:

```text
Ran 6 tests

OK
```

This showed that the message service and storage logic worked.

## Screenshots

### Project Structure

![Project Structure](screenshots/project-structure.png)

This screenshot shows the `campus_messenger` folder and the separated client, server, shared, tests and data folders.

### Server Running

![Server Running](screenshots/server-running.png)

This screenshot shows the Flask server running.

### Client Connected to Server

![Client Connected to Server](screenshots/client-connected-to-server.png)

This screenshot shows two CampusMessenger clients open at the same time.

One client uses the username `Student`, and the other uses `John`.

Both clients show the same messages, so this proves that the messages are shared through the server.

### Tests Passed

![Tests Passed](screenshots/antigravity-tests.png)

This screenshot shows the unit tests passing.

## What I Learned From This Structure

The main thing I learned is that the GUI should not do everything.

Before this, I would probably have made one file that shows the GUI and saves the data directly.

For this task, I separated it like this:

```text
GUI = what the user sees
API client = sends requests
Flask server = receives requests
Service = handles logic
Storage = saves JSON data
```

This made the project easier to understand.

## Short Personal Note

The most useful proof for me was opening two GUI windows at the same time.

When I sent a message from one client and saw it appear in the other client, I could clearly see that the app was working as a distributed client/server app.