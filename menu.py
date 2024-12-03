import tkinter as tk

class Menu:
    def __init__(self, parent_frame, show_content_callback):
        self.frame = parent_frame
        self.show_content_callback = show_content_callback

        self.menu_buttons = [
            ("Stocks", "Stocks"),
            ("Ventes", "Ventes"),
            ("Historique des ventes", "Historique des ventes")
        ]
        
        self.buttons = []
        for text, section in self.menu_buttons:
            button = tk.Button(self.frame, text=text, command=lambda s=section: self.show_content(s), bg="#34495e", fg="white", relief="flat", width=20, anchor="w", padx=10, pady=10)
            button.pack(fill=tk.X, pady=5)
            self.buttons.append(button)

    def show_content(self, section):
        self.show_content_callback(section)
