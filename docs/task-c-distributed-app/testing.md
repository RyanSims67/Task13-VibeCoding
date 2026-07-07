[Back to Task C](README.md)

# Task C — Testing

This file documents how I tested CampusMessenger.

I tested the app in two ways:

* automated tests
* manual testing with the server and GUI client

## Automated Tests

The automated tests are inside:

```text
campus_messenger/tests/
```

The test files are:

```text
test_message_service.py
test_message_storage.py
```

I ran the tests with this command:

```text
python -m unittest discover -s campus_messenger/tests
```

The result was:

```text
Ran 6 tests

OK
```

## What the Tests Check

The tests check the backend logic, not the GUI.

I focused on the service and storage files because those are easier to test automatically.

The tests check things like:

* creating a message
* saving messages
* loading messages
* filtering messages by room
* handling invalid or empty message data

## Test Screenshot

### Tests Passed

![Tests Passed](screenshots/antigravity-tests.png)

This screenshot shows that the unit tests passed.

## Manual Testing

I also tested the app manually.

First, I started the Flask server with:

```text
python campus_messenger/server/app.py
```

Then I opened the GUI client with:

```text
python campus_messenger/client/gui_client.py
```

After that, I opened a second GUI client window to test if two clients could share messages through the same server.

## Manual Test Steps

I manually tested these steps:

```text
1. Start the Flask server.
2. Open the first GUI client.
3. Enter username Student.
4. Choose the General room.
5. Send a message.
6. Open a second GUI client.
7. Enter username John.
8. Choose the General room.
9. Send another message.
10. Refresh the clients.
11. Check that both clients show the same messages.
```

## Manual Test Result

The manual test worked.

Both GUI clients showed the same messages.

This showed that the messages were not only stored inside one GUI window. They were sent to the Flask server and loaded again by both clients.

## Manual Testing Screenshots

### Server Running

![Server Running](screenshots/server-running.png)

This screenshot shows the Flask server running.

### Client Connected to Server

![Client Connected to Server](screenshots/client-connected-to-server.png)

This screenshot shows two clients connected to the same server.

## What I Did Not Test

I did not add advanced tests for:

* login accounts
* encryption
* databases
* WebSockets
* file uploads

I did not include those features because the app was intentionally kept simple for this task.

## Short Personal Reflection

The automated tests helped me check the service and storage logic.

The manual test helped me check the distributed part of the app.

The most useful manual test was opening two GUI clients at the same time. When both clients showed the same messages, I could see that the client/server connection was working.