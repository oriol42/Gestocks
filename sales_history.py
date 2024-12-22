import tkinter as tk
from tkinter import ttk

# Fonction d'affichage de la section Historique des Ventes
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
    columns = ("Date", "Client", "Produit", "Quantité", "Prix (FCFA)", "Total (FCFA)")
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

    # Ajouter quelques lignes simulées pour l'exemple
    sales_history_treeview.insert("", "end", values=("01/12/2024", "Jean Dupont", "Produit A", 3, "20", "60"))
    sales_history_treeview.insert("", "end", values=("02/12/2024", "Marie Dubois", "Produit B", 2, "15", "30"))
    sales_history_treeview.insert("", "end", values=("03/12/2024", "Paul Martin", "Produit A", 1, "20", "20"))

    # Calcul du total des ventes
    total_sales = 0
    for child in sales_history_treeview.get_children():
        total_sales += int(sales_history_treeview.item(child, 'values')[5])  # Récupérer la colonne "Total (FCFA)"

    # Affichage du total des ventes
    total_sales_label = tk.Label(sales_history_frame, text=f"Total des ventes de la journée : {total_sales} FCFA", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#333")
    total_sales_label.pack(pady=(10, 0))

    # Alternance de couleurs de lignes (optionnel pour lisibilité)
    for idx in range(len(sales_history_treeview.get_children())):
        if idx % 2 == 0:
            sales_history_treeview.item(sales_history_treeview.get_children()[idx], tags=('even',))
        else:
            sales_history_treeview.item(sales_history_treeview.get_children()[idx], tags=('odd',))

    sales_history_treeview.tag_configure('even', background="#f9f9f9")  # Couleur de ligne paire
    sales_history_treeview.tag_configure('odd', background="#ffffff")   # Couleur de ligne impaire

    return sales_history_frame
