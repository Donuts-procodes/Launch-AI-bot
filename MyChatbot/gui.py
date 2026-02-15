import customtkinter as ctk
import threading
from chat import get_response

# --- GUI SETUP ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config - Changed title to be generic
        self.title("AI Assistant") 
        self.geometry("500x700")
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        # 1. Title Label
        self.title_label = ctk.CTkLabel(
            self, 
            text="⚡ SYSTEM ONLINE ⚡", 
            font=("Roboto Medium", 16),
            text_color="#00e5ff" 
        )
        self.title_label.grid(row=0, column=0, pady=10)

        # 2. Chat Area
        self.chat_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=15,
            fg_color="#121212" 
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
            fg_color="#00b8d4", 
            hover_color="#00838f",
            font=("Arial", 18, "bold")
        )
        self.send_btn.pack(side="right")

        # Initial Greeting - Replaced "Ayush" with "User"
        self.add_message("Bot", "Greetings, User. Systems are operational. 🚀")

    def add_message(self, sender, text):
        if sender == "You":
            bubble_color = "#37474f"   
            text_color = "white"
            align_side = "right"
        else:
            bubble_color = "#00695c"   
            text_color = "white"
            align_side = "left"

        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.pack(pady=5, fill="x")

        bubble = ctk.CTkLabel(
            msg_container, 
            text=text, 
            fg_color=bubble_color, 
            text_color=text_color, 
            corner_radius=15,
            wraplength=350,       
            font=("Arial", 14),
            padx=15, pady=10,     
            justify="left",       
            anchor="w"            
        )
        
        bubble.pack(side=align_side, padx=10)
        self.after(10, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        user_input = self.entry.get()
        if not user_input.strip():
            return

        self.add_message("You", user_input)
        self.entry.delete(0, "end")

        threading.Thread(target=self.get_bot_reply, args=(user_input,)).start()

    def get_bot_reply(self, user_input):
        response = get_response(user_input)
        self.add_message("Bot", response)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
