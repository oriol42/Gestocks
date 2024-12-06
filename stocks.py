import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from utils import ManageProduct


class Stocks:
    def __init__(self, app):
        self.app = app

    def show_stocks(self):
        # Nettoyer et configurer l'interface principale
        self.app.clear_main_frame()
        self.app.content_label.config(text="Gestion des Stocks")
        self.show_stock_table()

    def show_stock_table(self):
        # Barre de recherche
        search_frame = tk.Frame(self.app.main_frame)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)
        self.search_button = tk.Button(
            search_frame,
            text="Rechercher",
            command=self.filter_products,
            font=("Arial", 12),
            bg="#3498db",
            fg="white"
        )
        self.search_button.grid(row=0, column=1, padx=10, pady=10)
        search_frame.pack(fill=tk.X)

        # Tableau des produits
        table_frame = tk.Frame(self.app.main_frame)
        self.table = ttk.Treeview(
            table_frame,
            columns=("id","name", "quantity", "Price", "description"),
            show="headings"
        )
        self.table.heading("id",text="ID")
        self.table.heading("name", text="Nom")
        self.table.heading("quantity", text="Quantité")
        self.table.heading("Price", text="Prix(FCFA)")
        self.table.heading("description", text="Description")
        self.table.column("id",width=0,stretch=tk.NO)

        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Ajouter les boutons
        action_frame = tk.Frame(self.app.main_frame)
        self.manage = ManageProduct(self.app)
        self.add_button = tk.Button(
            action_frame,
            text="Ajouter Produit",
            command=self.manage.AddProduct,
            font=("Arial", 12),
            bg="#2ecc71",
            fg="white"
        )
        
        self.add_button.grid(row=0, column=0, padx=10, pady=10)
        self.edit_button = tk.Button(
            action_frame,
            text="Modifier Produit",
            command = self.manage.updateProduct,
            font=("Arial", 12),
            bg="#f39c12",
            fg="white"
        )
        self.edit_button.grid(row=0, column=1, padx=10, pady=10)
        self.delete_button = tk.Button(
            action_frame,
            text="Supprimer Produit",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white"
        )
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)
        action_frame.pack()

        # Remplir le tableau
        self.populate_stock_table()

    def populate_stock_table(self):
        # Supprimer les données existantes dans le tableau
        for item in self.table.get_children():
            self.table.delete(item)

        # Charger les données de la base de données
        try:
            dbPath = os.path.join(os.path.dirname(__file__), 'database', 'GESTOCK.db')
            conn = sqlite3.connect(dbPath)
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, quantity, Price, description FROM Stocks")
            rows = cursor.fetchall()

            for row in rows:
                self.table.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données : {e}")

        finally:
            if 'conn' in locals():
                conn.close()

    def filter_products(self):
        search_term = self.search_entry.get().lower()
        # Appliquer un filtre de recherche (peut être implémenté si nécessaire)
        pass