import tkinter as tk
from tkinter import ttk, messagebox

class Stocks:
    def __init__(self, app):
        self.app = app
        

    def show_stocks(self):
        self.app.clear_main_frame()
        self.app.content_label.config(text="Gestion des Stocks")
        self.show_stock_table()

    def show_stock_table(self):
        # Barre de recherche
        search_frame = tk.Frame(self.app.main_frame)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)
        self.search_button = tk.Button(search_frame, text="Rechercher", command=self.filter_products, font=("Arial", 12), bg="#3498db", fg="white")
        self.search_button.grid(row=0, column=1, padx=10, pady=10)
        search_frame.pack(fill=tk.X)

        # Tableau des produits
        table_frame = tk.Frame(self.app.main_frame)
        self.table = ttk.Treeview(table_frame, columns=("Nom", "Quantité", "Prix", "Description"), show="headings")
        self.table.heading("Nom", text="Nom")
        self.table.heading("Quantité", text="Quantité")
        self.table.heading("Prix", text="Prix")
        self.table.heading("Description", text="Description")

        #  interagir avec la base de données pour la table
        self.populate_stock_table()
        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Boutons d'action sous le tableau
        action_frame = tk.Frame(self.app.main_frame)
        self.add_button = tk.Button(action_frame, text="Ajouter Produit", command=self.add_product, font=("Arial", 12), bg="#2ecc71", fg="white")
        self.add_button.grid(row=0, column=0, padx=10, pady=10)
        self.edit_button = tk.Button(action_frame, text="Modifier Produit", command=self.edit_product, font=("Arial", 12), bg="#f39c12", fg="white")
        self.edit_button.grid(row=0, column=1, padx=10, pady=10)
        self.delete_button = tk.Button(action_frame, text="Supprimer Produit", command=self.delete_product, font=("Arial", 12), bg="#e74c3c", fg="white")
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)
        action_frame.pack()

    def populate_stock_table(self):
        # interagir avec la base de données pour obtenir les produits
        pass

    def filter_products(self):
        search_term = self.search_entry.get().lower()
        # Filtrage des produits à partir de la base de données
        pass

    def add_product(self):
        # Interagir avec la base de données pour ajouter un produit
        pass

    def edit_product(self):
        # Interagir avec la base de données pour modifier un produit
        pass

    def delete_product(self):
        # Interagir avec la base de données pour supprimer un produit
        pass
