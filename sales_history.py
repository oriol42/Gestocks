import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

class SalesHistory:
    def __init__(self, app):
        self.app = app
        self.sales_history = []  # Historique des ventes (à récupérer depuis la base de données)

    def show_sales_history(self):
        """Affiche l'historique des ventes."""
        self.app.clear_main_frame()
        # Remplacer config par configure
        self.app.content_label.configure(text="Historique des Ventes", font=("Helvetica", 18, "bold"), text_color="#34495e")
        self.show_sales_history_table()

    def show_sales_history_table(self):
        """Affiche le tableau de l'historique des ventes avec un design moderne."""
        table_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#F9F9F9", corner_radius=15, border_width=2, border_color="#BDC3C7")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Créer un tableau pour afficher les ventes
        self.table = ttk.Treeview(table_frame, columns=("Produit", "Quantité", "Prix Total", "Date"), show="headings", height=10)
        self.table.heading("Produit", text="Produit")
        self.table.heading("Quantité", text="Quantité")
        self.table.heading("Prix Total", text="Prix Total (FCFA)")
        self.table.heading("Date", text="Date")

        # Ajouter un style au Treeview pour l'intégrer à customtkinter
        self.table.tag_configure("odd_row", background="#f5f5f5")
        self.table.tag_configure("even_row", background="#e0e0e0")
        
        # Récupérer les données historiques des ventes
        self.populate_sales_history_table()
        
        # Placer le Treeview dans la fenêtre
        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def populate_sales_history_table(self):
        """Récupère les données des ventes depuis la base de données."""
        # Remplacez cette méthode par la logique réelle de récupération des données depuis la base de données.
        
        # Exemple avec une base de données SQLite :
        # Connexion à la base de données
        # conn = sqlite3.connect('votre_base_de_donnees.db')  # Remplacez par le nom de votre base de données
        # cursor = conn.cursor()
        
        # Exécutez une requête pour récupérer les ventes, vous pouvez ajuster selon vos besoins
        # cursor.execute("SELECT produit, quantite, prix_total, date_vente FROM historique_ventes")
        # rows = cursor.fetchall()
        
        # Après avoir récupéré les données, vous pouvez remplir self.sales_history
        # self.sales_history = rows

        # Exemple simulé de données à supprimer une fois que vous récupérez les vraies données de la base de données :
        self.sales_history = [
            ("Produit A", 3, 6000, "2024-12-15"),
            ("Produit B", 1, 3500, "2024-12-14"),
            ("Produit C", 5, 25000, "2024-12-13"),
            ("Produit A", 2, 4000, "2024-12-12"),
            ("Produit B", 4, 14000, "2024-12-11"),
        ]
        
        # Vous pouvez maintenant parcourir self.sales_history pour afficher les données dans la table
        for index, sale in enumerate(self.sales_history):
            row_tag = "even_row" if index % 2 == 0 else "odd_row"
            self.table.insert("", "end", values=sale, tags=(row_tag,))
        
        # Assurez-vous de fermer la connexion à la base de données une fois la récupération effectuée
        # conn.close()

