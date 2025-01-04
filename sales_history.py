import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import os

def create_sales_history_frame(main_frame):
    # Créer un cadre pour l'historique des ventes dans le frame principal
    sales_history_frame = tk.Frame(main_frame, bg="#f0f0f0", padx=20, pady=20)
    
    # Titre de la section Historique des Ventes
    title_label = tk.Label(sales_history_frame, text="Historique des Ventes", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=(0, 20))  # Espacement sous le titre

    # Créer un cadre scrollable pour le Treeview
    treeview_frame = tk.Frame(sales_history_frame, bg="#f0f0f0")
    treeview_frame.pack(fill=tk.BOTH, expand=True)

    # Créer un Treeview pour afficher l'historique des ventes
    columns = ("Date", "Produit", "Quantité vendue", "Prix (FCFA)", "Total (FCFA)")
    sales_history_treeview = ttk.Treeview(treeview_frame, columns=columns, show="headings")
    
    # Définir les en-têtes des colonnes
    for col in columns:
        sales_history_treeview.heading(col, text=col)
        sales_history_treeview.column(col, anchor="center", width=120)
    
    # Ajouter une barre de défilement verticale
    treeview_scroll_y = tk.Scrollbar(treeview_frame, orient="vertical", command=sales_history_treeview.yview)
    sales_history_treeview.config(yscrollcommand=treeview_scroll_y.set)
    treeview_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    # Ajouter une barre de défilement horizontale
    treeview_scroll_x = tk.Scrollbar(treeview_frame, orient="horizontal", command=sales_history_treeview.xview)
    sales_history_treeview.config(xscrollcommand=treeview_scroll_x.set)
    treeview_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Placer le Treeview avec un espacement
    sales_history_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Connexion à la base de données et récupération des données de l'historique des ventes
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT date, product_name, quantity, unit_price, total_price, id FROM sales_history")  # Ajout de l'ID pour la suppression
    sales_data = cursor.fetchall()

    # Récupérer la date actuelle
    today = datetime.today()
    current_day = today.day
    current_month = today.month
    current_year = today.year

    # Variables pour les totaux
    total_sales_day = 0
    total_sales_month = 0

    # Ajouter les données dans le Treeview et calculer les totaux
    for sale in sales_data:
        sale_date = sale[0]  # Date de la vente
        sale_day = int(sale_date.split('-')[2])  # Récupérer le jour de la vente
        sale_month = int(sale_date.split('-')[1])  # Récupérer le mois de la vente
        sale_year = int(sale_date.split('-')[0])  # Récupérer l'année de la vente

        # Ajouter la vente au Treeview et calculer les totaux
        sales_history_treeview.insert("", "end", values=sale[:-1])  # Ne pas insérer l'ID
        if sale_day == current_day and sale_month == current_month and sale_year == current_year:
            total_sales_day += float(sale[4])
        if sale_month == current_month and sale_year == current_year:
            total_sales_month += float(sale[4])

    # Ajouter un bouton pour supprimer une vente sélectionnée sans aucune action
    delete_button = tk.Button(sales_history_frame, text="Supprimer la vente", command=lambda: None,
                              font=("Helvetica", 12, "bold"), bg="#ff4d4d", fg="white", relief="flat",
                              padx=20, pady=10, bd=0, activebackground="#ff3333", activeforeground="white")
    delete_button.pack(pady=10)

    # Ajouter un nouveau Treeview pour afficher les totaux
    totals_frame = tk.Frame(sales_history_frame, bg="#f0f0f0")
    totals_frame.pack(fill=tk.X, pady=10)

    totals_columns = ("Total des ventes de la journée", "Total des ventes du mois")
    totals_treeview = ttk.Treeview(totals_frame, columns=totals_columns, show="headings", height=1)

    for col in totals_columns:
        totals_treeview.heading(col, text=col)
        totals_treeview.column(col, anchor="center", width=200)

    # Ajouter les totaux calculés dans le Treeview
    totals_treeview.insert("", "end", values=(f"{total_sales_day} FCFA", f"{total_sales_month} FCFA"))
    totals_treeview.pack(fill=tk.X, padx=10)

    # Alternance de couleurs de lignes pour le Treeview des ventes
    for idx in range(len(sales_history_treeview.get_children())):
        if idx % 2 == 0:
            sales_history_treeview.item(sales_history_treeview.get_children()[idx], tags=('even',))
        else:
            sales_history_treeview.item(sales_history_treeview.get_children()[idx], tags=('odd',))

    sales_history_treeview.tag_configure('even', background="#f9f9f9")  # Couleur de ligne paire
    sales_history_treeview.tag_configure('odd', background="#ffffff")   # Couleur de ligne impaire

    return sales_history_frame, sales_history_treeview, totals_frame, totals_treeview
