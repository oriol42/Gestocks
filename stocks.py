import tkinter as tk
import customtkinter as ctk
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
        self.app.content_label.configure(text="Gestion des Stocks")  # Changement ici
        self.show_stock_table()
        self.show_low_stock_list()

    def show_stock_table(self):
        # Barre de recherche avec entrée et bouton
        search_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#ecf0f1", corner_radius=10)
        self.search_entry = ctk.CTkEntry(search_frame, font=("Arial", 12), width=200)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)
        self.search_button = ctk.CTkButton(
            search_frame,
            text="Rechercher",
            command=self.filter_products,
            font=("Arial", 12),
            fg_color="#3498db",  # Bleu pour le bouton
            hover_color="#1abc9c"  # Vert clair pour survol
        )
        self.search_button.grid(row=0, column=1, padx=10, pady=10)
        search_frame.pack(fill=tk.X, pady=20)

        # Tableau des produits
        table_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#ecf0f1", corner_radius=10)
        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "quantity", "Price", "description"),
            show="headings"
        )
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Nom")
        self.table.heading("quantity", text="Quantité")
        self.table.heading("Price", text="Prix(FCFA)")
        self.table.heading("description", text="Description")
        self.table.column("id", width=0, stretch=tk.NO)

        # Configurer les colonnes pour bien afficher les données
        self.table.column("name", width=200, anchor="w")
        self.table.column("quantity", width=100, anchor="center")
        self.table.column("Price", width=100, anchor="center")
        self.table.column("description", width=300, anchor="w")

        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Ajouter les boutons d'action
        action_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#ecf0f1", corner_radius=10)

        # Création d'un objet manage de la classe ManageProduct
        self.manage = ManageProduct(self.app)

        self.add_button = ctk.CTkButton(
            action_frame,
            text="Ajouter Produit",
            command=self.manage.AddProduct,
            font=("Arial", 12),
            fg_color="#2ecc71",  # Vert pour "Ajouter"
            hover_color="#27ae60"
        )
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.edit_button = ctk.CTkButton(
            action_frame,
            text="Modifier Produit",
            command=self.manage.UpdateProduct,
            font=("Arial", 12),
            fg_color="#f39c12",  # Jaune pour "Modifier"
            hover_color="#e67e22"
        )
        self.edit_button.grid(row=0, column=1, padx=10, pady=10)

        self.delete_button = ctk.CTkButton(
            action_frame,
            text="Supprimer Produit",
            command=self.manage.DeleteProduct,
            font=("Arial", 12),
            fg_color="#e74c3c",  # Rouge pour "Supprimer"
            hover_color="#c0392b"
        )
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)

        action_frame.pack(pady=20)

        # Remplir le tableau des produits
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

    def show_low_stock_list(self):
        # Barre de saisie pour définir le seuil
        low_stock_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#ecf0f1", corner_radius=10)
        low_stock_label = ctk.CTkLabel(low_stock_frame, text="Stocks faibles", font=("Arial", 14), text_color="#e74c3c")
        low_stock_label.grid(row=0, column=0, padx=10, pady=10)

        # Champ de saisie pour le seuil
        self.threshold_entry = ctk.CTkEntry(low_stock_frame, font=("Arial", 12), width=150)
        self.threshold_entry.grid(row=1, column=0, padx=10, pady=10)

        # Bouton Appliquer pour filtrer les stocks faibles
        self.apply_button = ctk.CTkButton(
            low_stock_frame,
            text="Appliquer",
            command=self.apply_low_stock_threshold,
            font=("Arial", 12),
            fg_color="#3498db",
            hover_color="#1abc9c"
        )
        self.apply_button.grid(row=1, column=1, padx=10, pady=10)

        low_stock_frame.pack(fill=tk.X, pady=20)

        # Tableau des stocks faibles
        low_stock_table_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#ecf0f1", corner_radius=10)
        self.low_stock_table = ttk.Treeview(
            low_stock_table_frame,
            columns=("id", "name", "quantity"),
            show="headings"
        )
        self.low_stock_table.heading("id", text="ID")
        self.low_stock_table.heading("name", text="Nom")
        self.low_stock_table.heading("quantity", text="Quantité")

        # Configurer les colonnes du Treeview
        self.low_stock_table.column("id", width=50, anchor="center")
        self.low_stock_table.column("name", width=200, anchor="w")
        self.low_stock_table.column("quantity", width=100, anchor="center")

        self.low_stock_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        low_stock_table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def apply_low_stock_threshold(self):
        try:
            # Récupérer le seuil de stock faible défini par l'utilisateur
            threshold = int(self.threshold_entry.get())
            # Mettre à jour la liste des stocks faibles
            self.populate_low_stock_list(threshold)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un seuil valide.")

    def populate_low_stock_list(self, threshold=10):
        # Supprimer les anciennes données des stocks faibles
        for item in self.low_stock_table.get_children():
            self.low_stock_table.delete(item)

        # Charger les produits avec une quantité inférieure au seuil
        try:
            dbPath = os.path.join(os.path.dirname(__file__), 'database', 'GESTOCK.db')
            conn = sqlite3.connect(dbPath)
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, quantity FROM Stocks WHERE quantity < ?", (threshold,))
            rows = cursor.fetchall()

            # Remplir le tableau avec les produits ayant des stocks faibles
            for row in rows:
                self.low_stock_table.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des stocks faibles : {e}")

        finally:
            if 'conn' in locals():
                conn.close()

    def filter_products(self):
        search_term = self.search_entry.get().lower()
        # Appliquer un filtre de recherche (peut être implémenté si nécessaire)
        pass
