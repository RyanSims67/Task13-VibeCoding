import os
import sys
from flask import Flask, jsonify

# Add the workspace root to sys.path so we can import the other components
# __file__ is campus_messenger/server/app.py
# parent 1: campus_messenger/server
# parent 2: campus_messenger
# parent 3: workspace root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from campus_messenger.server.storage.message_storage import MessageStorage
from campus_messenger.server.services.message_service import MessageService
from campus_messenger.server.routes.message_routes import message_bp

def create_app(data_file_path=None) -> Flask:
    """
    App factory to initialize Flask application, storage, and service layer.
    This factory pattern is also very helpful for writing unit tests.
    """
    app = Flask(__name__)

    # Default to campus_messenger/data/messages.json if not specified
    if not data_file_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file_path = os.path.join(base_dir, "data", "messages.json")

    # Initialize the Storage and Service
    storage = MessageStorage(data_file_path)
    service = MessageService(storage)

    # Store the service in the Flask app configuration so routes can access it
    app.config["message_service"] = service

    # Register the routes blueprint with the /api prefix
    app.register_blueprint(message_bp, url_prefix="/api")

    # Add a friendly homepage endpoint for testing if the server is running
    @app.route("/")
    def index():
        return jsonify({
            "status": "online",
            "message": "Welcome to the CampusMessenger Server API!",
            "endpoints": {
                "get_messages": "GET /api/messages?room=<room_name>",
                "post_message": "POST /api/messages"
            }
        })

    return app

if __name__ == "__main__":
    # Create the Flask application and run it locally
    app = create_app()
    print("Starting CampusMessenger server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
