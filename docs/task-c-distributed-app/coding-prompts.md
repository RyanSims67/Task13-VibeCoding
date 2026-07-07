[Back to Task C](README.md)

# Task C — Coding Prompts

This file documents the prompts I used with Google Antigravity for Task C.

I used Google Antigravity as my coding agent / VS Code clone for the CampusMessenger app.

I am keeping the prompts here because the task asks for step-by-step work using Markdown files.

## Prompt 1 — Initial CampusMessenger App

This was the first main prompt I used:

```text
I am working on Task C for my Vibe Code / Assisted Code / Agentic Coding assignment.

I want to build a beginner-friendly distributed Python app called CampusMessenger.

The app should be modular and easy for me to understand and explain later.

The basic flow should be:

Tkinter GUI Client
→ API Client
→ HTTP requests
→ Flask Server
→ Message Routes
→ Message Service
→ Message Storage
→ JSON file

Main features:
- enter a username
- choose a chat room
- send a message
- view messages
- refresh messages
- store messages in a JSON file
- filter messages by room
- include simple tests for the service and storage logic

Please keep the code simple and beginner-friendly.

Do not add advanced features like login accounts, encryption, WebSockets, databases, file uploads, or complicated styling.

After creating the files, briefly explain what each file does so I can understand the code.

Put everything you coded into the campus_messenger folder, do not edit the other folders.
```

## Why I Used This Prompt

I wanted the app to be simple but still distributed.

I specifically asked for:

* Tkinter GUI
* API client
* Flask server
* message routes
* service logic
* JSON storage
* tests

I also asked Antigravity not to add advanced features because I wanted to understand the code completely.

## Antigravity Implementation Plan

After the first prompt, Antigravity created an implementation plan.

The plan suggested creating these parts:

* shared message model
* JSON message storage
* message service
* Flask routes
* Flask app
* API client
* Tkinter GUI client
* service tests
* storage tests
* README documentation

I used this plan as the base for the app.

[Implementation Plan](output/implementation_plan.md)

### Screenshot

![Antigravity Implementation Plan](screenshots/antigravity-implementation-plan.png)

## Prompt 2 — Implement the Plan

After reading the plan, I asked Antigravity to implement it.

```text
This plan looks good. Please implement it now inside the campus_messenger folder only.

Keep the code simple and beginner-friendly.

After implementing, show me what files were created or changed, and tell me the commands to run the tests, server, and GUI client.
```

## Prompt 3 — Fix Formatting / Run Issues

When checking the project, I wanted to make sure the files were formatted correctly and easy to run.

I used a prompt like this when something needed fixing:

```text
The CampusMessenger app should stay simple and beginner-friendly.

Please check only the files inside the campus_messenger folder.

Make sure the Python files have proper formatting, line breaks and indentation.

Also make sure campus_messenger/requirements.txt has each dependency on its own line.

Do not change Task A or Task B.

After fixing, tell me the commands to run the tests, the Flask server and the GUI client.
```

## Prompt 4 — Testing

I also asked Antigravity to make sure the service and storage logic could be tested.

```text
Please add simple tests for the CampusMessenger service and storage logic.

The tests should check:
- creating a message
- saving and loading messages
- filtering messages by room
- rejecting empty message data

Use simple unittest tests that I can run with:

python -m unittest discover -s campus_messenger/tests
```

## Prompt 5 — Explanation

I asked Antigravity to explain the generated files so I could understand the project better.

```text
Please explain the CampusMessenger files in simple words.

I need to understand what each file does.

Focus on:
- gui_client.py
- api_client.py
- app.py
- message_routes.py
- message_service.py
- message_storage.py
- message_model.py
- the test files

Explain how a message moves from the GUI to the server and then into the JSON file.
```

## Screenshots

### Google Antigravity Used

![Google Antigravity Used](screenshots/antigravity-used.png)

### AI Prompt / Suggestion Used

![AI Prompt Used](screenshots/ai-suggestion-used.png)

### Implementation Plan

![Antigravity Implementation Plan](screenshots/antigravity-implementation-plan.png)

## What I Learned From Using the Prompts

The prompts helped me keep the app focused.

Instead of asking for a large complicated chat app, I asked for a simple distributed app that I could understand.

The most useful part was asking Antigravity to separate the code into modules.

This made it easier for me to see the flow:

```text
GUI
→ API Client
→ Flask Route
→ Service
→ Storage
→ JSON
```

## Personal Note

I did not want the agent to create a huge app with login, accounts or WebSockets.

I kept repeating that the code should be beginner-friendly because I needed to explain it myself.

This helped keep CampusMessenger small enough to understand, but still big enough to count as a distributed app.