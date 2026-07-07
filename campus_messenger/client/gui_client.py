import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# Add the workspace root to sys.path so we can import the api_client package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from campus_messenger.client.api_client import CampusMessengerAPIClient

class CampusMessengerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusMessenger")
        self.root.geometry("600x550")
        self.root.minimum_size = (500, 450)

        # Initialize API client
        self.api = CampusMessengerAPIClient()

        # Build UI layout
        self._create_widgets()

        # Start auto-refresh loop (every 3 seconds)
        self.poll_messages()

    def _create_widgets(self):
        # Configure grid weight for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # ----------------------------------------------------
        # TOP FRAME: User settings (Username, Room selection)
        # ----------------------------------------------------
        top_frame = ttk.LabelFrame(self.root, text=" User & Room Settings ", padding=10)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(3, weight=1)

        # Username label & entry
        ttk.Label(top_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_var = tk.StringVar(value="Student")
        self.username_entry = ttk.Entry(top_frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Room label & editable combobox
        ttk.Label(top_frame, text="Chat Room:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.room_var = tk.StringVar(value="General")
        self.room_combobox = ttk.Combobox(top_frame, textvariable=self.room_var)
        self.room_combobox["values"] = ("General", "Study", "Random", "Dorm", "Gaming")
        self.room_combobox.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        # Refresh messages when room changes
        self.room_combobox.bind("<<ComboboxSelected>>", lambda e: self.refresh_messages())

        # Filter Checkbox: Show all messages or only from selected room
        self.filter_room_var = tk.BooleanVar(value=True)
        self.filter_checkbox = ttk.Checkbutton(
            top_frame, 
            text="Filter by selected room", 
            variable=self.filter_room_var,
            command=self.refresh_messages
        )
        self.filter_checkbox.grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=2)

        # ----------------------------------------------------
        # MIDDLE FRAME: Message Display Board
        # ----------------------------------------------------
        middle_frame = ttk.LabelFrame(self.root, text=" Chat Board ", padding=10)
        middle_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=1)

        # Scrolled Text Box for showing messages
        self.chat_display = ScrolledText(middle_frame, wrap=tk.WORD, state="disabled", font=("Arial", 10))
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # ----------------------------------------------------
        # BOTTOM FRAME: Composing and Sending Messages
        # ----------------------------------------------------
        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        bottom_frame.columnconfigure(0, weight=1)

        # Message input entry
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(bottom_frame, textvariable=self.message_var)
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        # Bind the Enter key to automatically send the message
        self.message_entry.bind("<Return>", lambda e: self.send_message())

        # Send Button
        self.send_button = ttk.Button(bottom_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, sticky="ew", pady=5)

        # Refresh Button
        self.refresh_button = ttk.Button(bottom_frame, text="Manual Refresh", command=self.refresh_messages)
        self.refresh_button.grid(row=0, column=2, sticky="ew", padx=(10, 0), pady=5)

        # ----------------------------------------------------
        # STATUS BAR: Connection status at the bottom
        # ----------------------------------------------------
        self.status_label = ttk.Label(self.root, text="Connecting to server...", relief=tk.SUNKEN, anchor="w", padding=5)
        self.status_label.grid(row=3, column=0, sticky="ew")

    def send_message(self):
        """
        Sends the typed message to the server via API client.
        """
        username = self.username_var.get().strip()
        room = self.room_var.get().strip()
        content = self.message_var.get().strip()

        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        if not room:
            messagebox.showwarning("Warning", "Please enter/select a chat room.")
            return
        if not content:
            # Don't send empty messages
            return

        # Attempt to send message
        success, response = self.api.send_message(username, room, content)
        if success:
            # Clear input field on success
            self.message_var.set("")
            self.refresh_messages()
        else:
            messagebox.showerror("Error Sending Message", response)

    def refresh_messages(self, is_auto=False):
        """
        Fetches the latest messages from the server.
        """
        room_filter = self.room_var.get().strip() if self.filter_room_var.get() else None

        # Fetch messages from API
        success, response = self.api.get_messages(room=room_filter)
        if success:
            self._update_status(True)
            self._display_messages(response)
        else:
            self._update_status(False, response)
            # Only show pop-up error dialog on manual refresh to avoid annoying the user during background polling
            if not is_auto:
                messagebox.showerror("Connection Error", response)

    def _display_messages(self, messages: list):
        """
        Helper method to render messages list in the ScrolledText box.
        """
        self.chat_display.config(state="normal")
        # Clear existing text
        self.chat_display.delete("1.0", tk.END)

        if not messages:
            self.chat_display.insert(tk.END, "No messages in this chat room yet. Be the first to say hello!\n")
        else:
            for msg in messages:
                timestamp = msg.get("timestamp", "")
                room = msg.get("room", "")
                username = msg.get("username", "")
                content = msg.get("content", "")
                # Format: [HH:MM:SS] [Room] Username: Message Content
                formatted = f"[{timestamp}] [{room}] {username}: {content}\n"
                self.chat_display.insert(tk.END, formatted)

        self.chat_display.config(state="disabled")
        # Automatically scroll to the bottom to see new messages
        self.chat_display.see(tk.END)

    def _update_status(self, is_connected: bool, error_msg: str = ""):
        """
        Updates the status bar label at the bottom.
        """
        if is_connected:
            self.status_label.config(text="Status: Connected to Server", foreground="green")
        else:
            self.status_label.config(text=f"Status: Disconnected ({error_msg})", foreground="red")

    def poll_messages(self):
        """
        Automatically polls the server for new messages every 3 seconds.
        """
        self.refresh_messages(is_auto=True)
        self.root.after(3000, self.poll_messages)

if __name__ == "__main__":
    # Create the Tkinter root window and launch the app
    root = tk.Tk()
    app = CampusMessengerGUI(root)
    root.mainloop()
