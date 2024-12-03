import tkinter as tk
from tkinter import ttk
from stocks import Stocks
from sales import Sales
from sales_history import SalesHistory

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock et Ventes")
        self.root.geometry("1000x700")
        self.root.config(bg="#f4f4f9")

        # Initialisation des modules
        self.stocks = Stocks(self)
        self.sales = Sales(self)
        self.sales_history_module = SalesHistory(self)

        # Définition de la barre supérieure
        self.top_frame = tk.Frame(self.root, bg="#3498db", height=50)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)

        self.title_label = tk.Label(self.top_frame, text="Gestion de Stock et Ventes", font=("Arial", 18, "bold"), fg="white", bg="#3498db")
        self.title_label.pack(side=tk.LEFT, padx=20)

        # Définition du menu latéral
        self.sidebar_frame = tk.Frame(self.root, bg="#2c3e50", width=200, height=600)
        self.sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        self.menu_buttons = [
            ("Stocks", self.stocks.show_stocks),
            ("Ventes", self.sales.show_sales),
            ("Historique des ventes", self.sales_history_module.show_sales_history)
        ]

        self.buttons = []
        for text, command in self.menu_buttons:
            button = tk.Button(self.sidebar_frame, text=text, command=command, bg="#34495e", fg="white", relief="flat", width=20, anchor="w", padx=10, pady=10)
            button.pack(fill=tk.X, pady=5)
            self.buttons.append(button)

        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.content_label = tk.Label(self.main_frame, text="Sélectionner une option", font=("Arial", 16))
        self.content_label.pack(pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            if widget != self.content_label:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
