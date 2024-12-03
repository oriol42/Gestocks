import tkinter as tk
from tkinter import ttk


class SalesHistory:
    def __init__(self, app):
        self.app = app
        

    def show_sales_history(self):
        self.app.clear_main_frame()
        self.app.content_label.config(text="Historique des Ventes")
        self.show_sales_history_table()

    def show_sales_history_table(self):
        table_frame = tk.Frame(self.app.main_frame)
        self.table = ttk.Treeview(table_frame, columns=("Produit", "Quantité", "Prix Total", "Date"), show="headings")
        self.table.heading("Produit", text="Produit")
        self.table.heading("Quantité", text="Quantité")
        self.table.heading("Prix Total", text="Prix Total")
        self.table.heading("Date", text="Date")

        #  récupérez l'historique des ventes depuis la base de données ici
        self.populate_sales_history_table()
        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True)

    def populate_sales_history_table(self):
        #: Interagir avec la base de données pour l'historique des ventes
        pass
