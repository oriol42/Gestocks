import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import utils
import sqlite3,shutil
import os

# Fonction d'affichage du tableau de bord
def create_dashboard_frame(main_frame):
    # Frame principale du tableau de bord
    dashboard_frame = ctk.CTkFrame(main_frame, fg_color="#f4f6f9", corner_radius=10)
    
    # Titre du tableau de bord
    title_label = ctk.CTkLabel(dashboard_frame, text="Tableau de Bord", font=("Helvetica", 18, "bold"), text_color="#2c3e50")
    title_label.pack(pady=5)

    # Résumé des ventes récentes
    sales_summary_frame = ctk.CTkFrame(dashboard_frame, fg_color="#ffffff", corner_radius=10)
    sales_summary_frame.pack(fill="x", pady=10)

    # Tableau des produits disponibles
    dashboard_treeview = ttk.Treeview(sales_summary_frame, columns=(
        "Ventes du jour", "Ventes du mois", "Bénéfice Journalier", "Bénéfice mensuel", "Stock disponible", "Produits en rupture de stocks"), 
        show="headings", height=2
    )

    # Titre des colonnes
    for i, col in enumerate(["Ventes du jour", "Ventes du mois", "Bénéfice Journalier", "Bénéfice mensuel", "Stock disponible", "Produits en rupture de stocks"]):
        dashboard_treeview.heading(f"#{i+1}", text=col, anchor="w")

    # Redéfinition de la largeur de la dernière colonne
    dashboard_treeview.column("#6", width=300, anchor="w")

    # Style de police et de couleur pour améliorer la lisibilité
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 14), rowheight=30)  
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="#000000", background="#64b5f6")  
    style.configure("Treeview", background="#ffffff", fieldbackground="#f8f9fa", foreground="#333333")  

    dashboard_treeview.pack(fill="both", expand=True)
    
    utils.update_dashboard_treeview(dashboard_treeview)

    # Bouton "Produits en rupture de stock"
    stock_button = ctk.CTkButton(
        sales_summary_frame,
        text="Produits en rupture de stock",
        font=("Helvetica", 14),
        fg_color="red",
        text_color="white",
        command=lambda: view_out_of_stock(main_frame)
    )
    stock_button.pack(pady=5)

    # Section des alertes de stock faible
    stock_alert_frame = tk.Frame(dashboard_frame)
    stock_alert_frame.pack(fill="both", expand=True, pady=20)  # Remplir toute la place disponible

    # Appeler la fonction pour charger les alertes de stock faible
    utils.load_low_stock_alerts(stock_alert_frame)

    return dashboard_frame, dashboard_treeview, stock_alert_frame


# Fonction pour afficher les produits en rupture de stock
def view_out_of_stock(main_frame):
    db_path = utils.get_db_path()
    if not os.path.exists(db_path):
      original_db_path = os.path.join(os.path.dirname(__file__), "DataBase", "GESTOCK.db")
      shutil.copy2(original_db_path, db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT nom FROM stocks WHERE quantite = 0")
    result = cursor.fetchall()

    list_window = ctk.CTkToplevel(main_frame)
    list_window.title("Produits en Rupture de Stock")
    list_window.geometry("400x300")
    list_window.configure(fg_color="#f4f6f9")

    title_label = ctk.CTkLabel(
        list_window,
        text="Produits en Rupture de Stock",
        font=("Helvetica", 16, "bold"),
        text_color="#e74c3c"
    )
    title_label.pack(pady=10)

    if not result:
        empty_label = ctk.CTkLabel(
            list_window,
            text="Aucun produit en rupture de stock.",
            font=("Helvetica", 14),
            text_color="#34495e"
        )
        empty_label.pack(pady=20)
    else:
        container_frame = ctk.CTkFrame(list_window, fg_color="#ffffff", corner_radius=10)
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for row in result:
            nom = row[0]
            product_label = ctk.CTkLabel(
                container_frame,
                text=f"- {nom}",
                font=("Helvetica", 14),
                text_color="#2c3e50"
            )
            product_label.pack(anchor="w", pady=2)

    close_button = ctk.CTkButton(
        list_window,
        text="Fermer",
        font=("Helvetica", 14, "bold"),
        fg_color="#e74c3c",
        text_color="#ffffff",
        command=list_window.destroy
    )
    close_button.pack(pady=10)

    conn.close()
