[Back to Task C](README.md)

# Task C — Code Understanding

This file explains the CampusMessenger code in my own words.

The task says that I should understand the code completely, so I wrote this file to show what each important file does.

## Main App Flow

The app works like this:

```text
GUI client
    ↓
API client
    ↓
Flask server
    ↓
Routes
    ↓
Service
    ↓
Storage
    ↓
JSON file
```

The GUI does not save messages by itself.

When I send a message, the GUI passes the data to the API client. The API client sends it to the Flask server. The server route receives it and uses the service. The service uses the storage file to save it in JSON.

## `campus_messenger/client/gui_client.py`

This file creates the desktop window using Tkinter.

This is the file I interact with when I run the app.

It contains the visible parts of the app:

* username input
* room selection
* filter by selected room checkbox
* chat board
* message input field
* send button
* manual refresh button
* connection status

I understand this file as the user interface file.

When I click **Send**, the GUI reads:

* username
* room
* message text

Then it calls the API client instead of saving the message directly.

When I click **Manual Refresh**, the GUI asks the API client to get the newest messages from the server.

## `campus_messenger/client/api_client.py`

This file connects the GUI to the Flask server.

The GUI does not know all the server route details. It just calls methods from this file.

For example, this file handles:

* sending a message to the server
* getting messages from the server
* handling connection problems

I understand this file as the bridge between the desktop GUI and the backend server.

Without this file, the GUI would have to contain HTTP request code directly, which would make the GUI harder to understand.

## `campus_messenger/server/app.py`

This file starts the Flask server.

I used this file when I ran:

```text
python campus_messenger/server/app.py
```

The server needs to be running before the GUI can connect.

This file creates the Flask app and connects the message routes.

I understand this file as the starting point for the backend.

## `campus_messenger/server/routes/message_routes.py`

This file contains the Flask API routes.

The routes are the URLs that the API client talks to.

The routes are used for things like:

* receiving a new message
* returning stored messages
* filtering messages by room

I understand this file as the part that receives HTTP requests.

The route file should not do all the logic by itself. It should pass the work to the service file.

## `campus_messenger/server/services/message_service.py`

This file contains the main message logic.

It handles the rules for messages.

For example, it is responsible for:

* creating a message
* checking that message data is valid
* getting messages
* filtering messages by room

I understand this file as the main logic layer of the app.

This file is important because it keeps the logic separate from the Flask routes.

## `campus_messenger/server/storage/message_storage.py`

This file saves and loads messages.

It works with the JSON file:

```text
campus_messenger/data/messages.json
```

I understand this file as the file-handling part of the app.

The rest of the program does not need to know the details of opening, reading or writing the JSON file.

This keeps the storage code separate from the GUI and server routes.

## `campus_messenger/shared/message_model.py`

This file defines what one message looks like.

A message contains:

* username
* room
* content
* timestamp

This file also helps convert a message into a dictionary so it can be saved in JSON or returned through the API.

I understand this file as the shared data structure.

It makes the message format clear and consistent.

## `campus_messenger/tests/test_message_service.py`

This file tests the service logic.

It checks that the message service can:

* create messages
* return messages
* filter messages by room
* reject invalid or empty message data

I understand this test file as proof that the logic works without needing to click through the GUI every time.

## `campus_messenger/tests/test_message_storage.py`

This file tests the JSON storage.

It checks that messages can be saved and loaded correctly.

This is important because the app depends on the JSON file to keep messages.

## What Happens When I Send a Message

This is what happens when I send a message from the GUI:

```text
1. I type a username, choose a room and type a message.
2. I click Send.
3. gui_client.py reads the input fields.
4. gui_client.py calls api_client.py.
5. api_client.py sends a POST request to the Flask server.
6. message_routes.py receives the request.
7. message_routes.py sends the data to message_service.py.
8. message_service.py creates the message.
9. message_storage.py saves the message in messages.json.
10. The GUI refreshes and shows the message on the chat board.
```

## What Happens When I Refresh Messages

This is what happens when I refresh messages:

```text
1. I click Manual Refresh.
2. gui_client.py asks api_client.py for messages.
3. api_client.py sends a GET request to the server.
4. message_routes.py receives the request.
5. message_service.py gets the messages.
6. message_storage.py loads the messages from JSON.
7. The server returns the messages.
8. The GUI displays them in the chat board.
```

## Why I Understand the Distributed Part

I tested the app by opening two GUI windows.

One window used the username `Student`.

The other window used the username `John`.

When I sent a message from one window, both clients showed the messages after refreshing.

This helped me understand that the messages were not only inside one GUI window. They were saved through the server and shared between clients.

## Screenshot Evidence

### Client Connected to Server

![Client Connected to Server](screenshots/client-connected-to-server.png)

This screenshot helped me prove that two clients can see the same messages.

### Tests Passed

![Tests Passed](screenshots/antigravity-tests.png)

This screenshot shows that the service and storage tests passed.

## Personal Note

The part that made the most sense to me was the separation between the GUI and the storage.

Before this task, I would probably have saved data directly inside the GUI file.

Now I understand that the GUI should mainly handle the user interface, while the server, service and storage files handle the backend work.