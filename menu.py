import tkinter as tk
import customtkinter as ctk

class Menu:
    def __init__(self, parent_frame, show_content_callback):
        self.frame = parent_frame
        self.show_content_callback = show_content_callback

        # Définir les sections du menu avec des couleurs et des polices modernes
        self.menu_buttons = [
            ("Stocks", "Stocks"),
            ("Ventes", "Ventes"),
            ("Historique des ventes", "Historique des ventes")
        ]
        
        self.buttons = []
        for text, section in self.menu_buttons:
            # Remplacer le bouton classique par un bouton CTkButton avec un design moderne
            button = ctk.CTkButton(self.frame, text=text, command=lambda s=section: self.show_content(s),
                                   width=200, height=40, font=("Helvetica", 14, "bold"), fg_color="#34495e",  # Couleur de fond
                                   hover_color="#1abc9c", anchor="w", corner_radius=10)  # Couleur de survol
            button.pack(fill=tk.X, pady=10, padx=20)  # Ajouter de l'espace entre les boutons
            self.buttons.append(button)

        # Fond de la fenêtre parent
        self.frame.configure(fg_color="#f4f6f7")  # Un fond doux et moderne

    def show_content(self, section):
        self.show_content_callback(section)
