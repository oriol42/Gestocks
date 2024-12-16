import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from stocks import Stocks
from sales import Sales
from sales_history import SalesHistory

# Définir un style de base pour customtkinter
ctk.set_appearance_mode("light")  # Mode clair (ou "dark" pour un thème sombre)
ctk.set_default_color_theme("blue")  # Choisir un thème parmi ceux disponibles (light, dark, blue)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock et Ventes")
        self.root.geometry("1000x700")
        self.root.config(bg="#F4F4F9")  # Fond clair pour l'application

        # Initialisation des modules
        self.stocks = Stocks(self)
        self.sales = Sales(self)
        self.sales_history_module = SalesHistory(self)

        # Définition de la barre supérieure
        self.top_frame = ctk.CTkFrame(self.root, fg_color="#2C3E50", height=50)  # Bleu foncé pour la barre
        self.top_frame.pack(fill=tk.X, side=tk.TOP)

        self.title_label = ctk.CTkLabel(self.top_frame, text="Gestion de Stock et Ventes", font=("Arial", 18, "bold"), text_color="white", fg_color="#2C3E50")
        self.title_label.pack(side=tk.LEFT, padx=20)

        # Définition du menu latéral avec customtkinter pour des boutons plus modernes
        self.sidebar_frame = ctk.CTkFrame(self.root, width=220, height=600, corner_radius=10, fg_color="#34495e")  # Gris foncé
        self.sidebar_frame.pack(fill=tk.Y, side=tk.LEFT, padx=20, pady=20)

        # Création de boutons plus modernes dans la sidebar
        self.menu_buttons = [
            ("Stocks", self.stocks.show_stocks),
            ("Ventes", self.sales.show_sales),
            ("Historique des ventes", self.sales_history_module.show_sales_history)
        ]

        self.buttons = []
        for text, command in self.menu_buttons:
            button = ctk.CTkButton(self.sidebar_frame, text=text, command=command, width=200, height=40, font=("Arial", 14), fg_color="#2C3E50", hover_color="#1ABC9C", anchor="w")
            button.pack(fill=tk.X, pady=10)
            self.buttons.append(button)

        # Définition du cadre principal pour afficher les contenus
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#F4F4F9", corner_radius=10)  # Fond clair dans le cadre principal
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Label par défaut dans le cadre principal
        self.content_label = ctk.CTkLabel(self.main_frame, text="Sélectionner une option", font=("Arial", 16), text_color="#2D3436")
        self.content_label.pack(pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            if widget != self.content_label:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()