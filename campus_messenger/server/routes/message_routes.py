import os
import sys
from flask import Blueprint, request, jsonify, current_app

# Add the workspace root to sys.path so we can import the shared model
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

message_bp = Blueprint("message_bp", __name__)

@message_bp.route("/messages", methods=["GET"])
def get_messages():
    """
    GET /api/messages
    Retrieves all messages, optionally filtered by a specific room.
    """
    service = current_app.config["message_service"]
    room = request.args.get("room") # Get optional 'room' query parameter

    try:
        messages = service.get_messages(room=room)
        # Convert Message objects to dictionaries for JSON response
        messages_json = [msg.to_dict() for msg in messages]
        return jsonify(messages_json), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve messages: {str(e)}"}), 500

@message_bp.route("/messages", methods=["POST"])
def post_message():
    """
    POST /api/messages
    Creates and saves a new message.
    Expects a JSON body containing 'username', 'room', and 'content'.
    """
    service = current_app.config["message_service"]
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid request: missing JSON body."}), 400

    username = data.get("username")
    room = data.get("room")
    content = data.get("content")

    try:
        new_msg = service.post_message(username, room, content)
        return jsonify(new_msg.to_dict()), 201
    except ValueError as ve:
        # Handles validation errors (e.g. empty fields)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to post message: {str(e)}"}), 500
