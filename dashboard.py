import tkinter as tk
from tkinter import ttk
import utils
import sqlite3
import os

# Fonction d'affichage du tableau de bord
def create_dashboard_frame(main_frame):
    # Frame principale du tableau de bord
    dashboard_frame = tk.Frame(main_frame, bg="#f4f6f9", padx=20, pady=20)
    
    # Titre du tableau de bord
    title_label = tk.Label(dashboard_frame, text="Tableau de Bord", font=("Helvetica", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
    title_label.pack(pady=5)

    # Résumé des ventes récentes
    sales_summary_frame = tk.Frame(dashboard_frame, bg="#ffffff", pady=10, padx=20, bd=2, relief="groove")
    sales_summary_frame.pack(fill=tk.X, pady=10)

    # Tableau des produits disponibles
    dashboard_treeview = ttk.Treeview(sales_summary_frame, columns=("Ventes du jour", "Ventes du mois", "Benefice Journalier", "Benefice mensuel", "Stock disponible", "Produits en rupture de stocks"), 
                                  show="headings", height=2)

    # Titre des colonnes
    dashboard_treeview.heading("#1", text="Ventes du jour", anchor="w")
    dashboard_treeview.heading("#2", text="Ventes du mois", anchor="w")
    dashboard_treeview.heading("#3", text="Benefice Journalier", anchor="w")
    dashboard_treeview.heading("#4", text="Benefice mensuel", anchor="w")
    dashboard_treeview.heading("#5", text="Stock disponible", anchor="w")
    dashboard_treeview.heading("#6", text="Produits en rupture de stocks", anchor="w")

    # Style de police et de couleur pour améliorer la lisibilité
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 1), rowheight=30)  # Taille de la police et hauteur de ligne
    style.configure("Treeview.Heading", font=("Helvetica", 1, "bold"), foreground="#000000", background="#64b5f6")  # Couleur du texte des en-têtes en noir
    style.configure("Treeview", background="#ffffff", fieldbackground="#f8f9fa", foreground="#333333")  # Couleurs des lignes

    dashboard_treeview.pack(fill="both", expand=True)
    
    utils.update_dashboard_treeview(dashboard_treeview)

    # Bouton "Produits en rupture de stock"
    stock_button = tk.Button(
        sales_summary_frame,
        text="Produits en rupture de stock",
        font=("Helvetica", 12),
        bg="#ffffff",  # Couleur identique à celle du cadre
        fg="#34495e",
        relief="flat",
        activebackground="#ffffff",  # Arrière-plan au clic
        command=lambda:view_out_of_stock(main_frame) # Fonction pour gérer les produits en rupture
    )
    stock_button.pack(pady=5)

    # Section des alertes de stock faible
    stock_alert_frame = tk.Frame(dashboard_frame, bg="#ffffff", pady=10, padx=20, bd=2, relief="groove")
    stock_alert_frame.pack(fill=tk.X, pady=20)

    stock_alert_title = tk.Label(stock_alert_frame, text="Alertes de Stock Faible", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#e74c3c")
    stock_alert_title.pack(pady=10)

    low_stock_items = utils.get_low_stock_items() # Fonction dynamique pour récupérer les produits en stock faible
    

    if not low_stock_items:
        empty_label = tk.Label(stock_alert_frame, text="Aucune alerte de stock faible", font=("Helvetica", 12), bg="#ffffff", fg="#34495e")
        empty_label.pack(pady=5)
    else:
        canvas = tk.Canvas(stock_alert_frame)
        scrollbar = tk.Scrollbar(stock_alert_frame, orient="vertical", command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        alert_container = tk.Frame(canvas, bg="#ffffff")
        row, col, num_columns = 0, 0, 4

        for product, stock in low_stock_items:
            alert_card = tk.Frame(alert_container, bg="#ecf0f1", bd=1, relief="solid", padx=15, pady=10, width=230)
            alert_card.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            alert_label = tk.Label(alert_card, text=f"{product}: {stock}", font=("Helvetica", 12), bg="#ecf0f1", fg="#e74c3c")
            alert_label.pack()
            col += 1
            if col >= num_columns:
                col, row = 0, row + 1

        canvas.create_window((0, 0), window=alert_container, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        alert_container.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    return dashboard_frame, dashboard_treeview,stock_alert_frame


# Fonction pour afficher les produits en rupture de stock
def view_out_of_stock(main_frame):
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'DataBase', 'GESTOCK.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Requête pour récupérer les produits en rupture de stock
    cursor.execute("SELECT nom FROM stocks WHERE quantite = 0")
    result = cursor.fetchall()

    # Création du Toplevel
    list_window = tk.Toplevel(main_frame)
    list_window.title("Produits en Rupture de Stock")
    list_window.geometry("400x300")
    list_window.config(bg="#f4f6f9")  # Couleur de fond douce

    # Titre
    title_label = tk.Label(
        list_window,
        text="Produits en Rupture de Stock",
        font=("Helvetica", 16, "bold"),
        bg="#f4f6f9",
        fg="#e74c3c"
    )
    title_label.pack(pady=10)

    # Vérification s'il y a des produits en rupture de stock
    if not result:
        empty_label = tk.Label(
            list_window,
            text="Aucun produit en rupture de stock.",
            font=("Helvetica", 12),
            bg="#f4f6f9",
            fg="#34495e"
        )
        empty_label.pack(pady=20)
    else:
        # Conteneur pour les noms
        container_frame = tk.Frame(list_window, bg="#ffffff", padx=10, pady=10, bd=2, relief="groove")
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Affichage des noms
        for row in result:
            nom = row[0]
            product_label = tk.Label(
                container_frame,
                text=f"- {nom}",
                font=("Helvetica", 12),
                bg="#ffffff",
                fg="#2c3e50",
                anchor="w"
            )
            product_label.pack(anchor="w", pady=2)

    # Bouton de fermeture
    close_button = tk.Button(
        list_window,
        text="Fermer",
        font=("Helvetica", 12, "bold"),
        bg="#e74c3c",
        fg="#ffffff",
        relief="flat",
        command=list_window.destroy
    )
    close_button.pack(pady=10)

    # Fermeture de la connexion à la base de données
    conn.close()
    

# Fonctions dynamiques de récupération des données
def get_sales_data():
    return {}  # Aucune donnée par défaut

