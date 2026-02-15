import customtkinter as ctk
import threading
from chat import get_response

# --- GUI SETUP ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Ayush's AI Assistant")
        self.geometry("500x700")
        
        # Grid Configuration (Makes it resizable and responsive)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Chat area expands

        # 1. Title Label (Cyberpunk Style)
        self.title_label = ctk.CTkLabel(
            self, 
            text="⚡ SYSTEM ONLINE ⚡", 
            font=("Roboto Medium", 16),
            text_color="#00e5ff" # Neon Cyan text
        )
        self.title_label.grid(row=0, column=0, pady=10)

        # 2. Chat Area (Scrollable)
        self.chat_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=15,
            fg_color="#121212" # Very dark background for chat
        )
        self.chat_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # 3. Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Entry Box
        self.entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Enter command...", 
            height=45,
            font=("Arial", 14),
            corner_radius=20,
            border_color="#333333",
            fg_color="#1e1e1e"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        # Send Button
        self.send_btn = ctk.CTkButton(
            self.input_frame, 
            text="➤", 
            width=50, 
            height=45, 
            command=self.send_message, 
            corner_radius=20,
            fg_color="#00b8d4", # Bright Cyan Button
            hover_color="#00838f",
            font=("Arial", 18, "bold")
        )
        self.send_btn.pack(side="right")

        # Initial Greeting
        self.add_message("Bot", "Greetings, Ayush. Systems are operational. 🚀")

    def add_message(self, sender, text):
        # --- COLOR SCHEME & ALIGNMENT ---
        if sender == "You":
            bubble_color = "#37474f"   # Dark Charcoal for User
            text_color = "white"
            align_side = "right"
        else:
            bubble_color = "#00695c"   # Deep Teal for Bot (Matrix vibes)
            text_color = "white"
            align_side = "left"

        # Container Frame (Invisible, just holds the bubble)
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.pack(pady=5, fill="x")

        # The Bubble Itself
        bubble = ctk.CTkLabel(
            msg_container, 
            text=text, 
            fg_color=bubble_color, 
            text_color=text_color, 
            corner_radius=15,
            wraplength=350,       # Wrap text if it gets too long
            font=("Arial", 14),
            padx=15, pady=10,     # Internal padding (breathing room)
            justify="left",       # ✅ KEY FIX: Left-aligns multiple lines
            anchor="w"            # ✅ KEY FIX: Anchors text to the West (Left)
        )
        
        # Pack bubble to Left or Right
        bubble.pack(side=align_side, padx=10)

        # Auto-scroll to the bottom
        # We use .after() to ensure the GUI updates before scrolling
        self.after(10, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        user_input = self.entry.get()
        if not user_input.strip():
            return

        # 1. Show User Message Immediately
        self.add_message("You", user_input)
        self.entry.delete(0, "end")

        # 2. Get Bot Response in Background Thread
        # This prevents the window from freezing while searching Wikipedia
        threading.Thread(target=self.get_bot_reply, args=(user_input,)).start()

    def get_bot_reply(self, user_input):
        response = get_response(user_input)
        # Update GUI safely
        self.add_message("Bot", response)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()