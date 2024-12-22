import tkinter as tk
from tkinter import messagebox

# Fonction d'affichage de la section Rapports
def create_reports_frame(main_frame):
    # Création du cadre principal pour les rapports
    reports_frame = tk.Frame(main_frame, bg="#f4f4f9", bd=5, relief="groove")
    reports_frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Titre principal
    tk.Label(reports_frame, text="Rapports de Ventes et Stocks", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white", pady=10).pack(fill="x")
    
    # Cadre pour les rapports de ventes
    sales_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    sales_frame.pack(pady=10, fill="x")
    
    # Utilisation de grid pour l'alignement compact
    tk.Label(sales_frame, text="Chiffre d'Affaires : 6,000,000 FCFA", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    tk.Label(sales_frame, text="Ventes Totales : 9,000,000 FCFA (Mois)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=1, column=0, sticky="w", pady=4)
    tk.Label(sales_frame, text="Ventes par Produit : Produit A (200 unités, 2,000,000 FCFA)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=2, column=0, sticky="w", pady=4)
    tk.Label(sales_frame, text="Ventes par Client : Client X (2,500,000 FCFA)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=3, column=0, sticky="w", pady=4)
    tk.Label(sales_frame, text="Comparaison des Ventes : +10% Mois Précédent", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=4, column=0, sticky="w", pady=4)
    
    # Cadre pour les rapports de stocks
    stock_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    stock_frame.pack(pady=10, fill="x")
    
    # Utilisation de grid pour l'alignement compact
    tk.Label(stock_frame, text="Stock Obsolète : Produit B (5 unités)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    tk.Label(stock_frame, text="Mouvement de Stock par Catégorie : Catégorie X (20 entrées, 10 sorties)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=1, column=0, sticky="w", pady=4)
    tk.Label(stock_frame, text="Rentabilité par Produit : Produit A (40% de marge)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=2, column=0, sticky="w", pady=4)
    
    # Indicateur de Stock Optimal : produit à réapprovisionner
    stock_levels = {'Produit A': 10, 'Produit B': 3, 'Produit C': 20}  # Exemple de stocks pour chaque produit
    low_stock_threshold = 5  # Seuil de réapprovisionnement
    
    low_stock_products = [product for product, stock in stock_levels.items() if stock < low_stock_threshold]
    
    if low_stock_products:
        tk.Label(stock_frame, text=f"Réapprovisionnement requis : {', '.join(low_stock_products)}", font=("Helvetica", 12), bg="#ffffff", fg="#D32F2F").grid(row=3, column=0, sticky="w", pady=4)
    else:
        tk.Label(stock_frame, text="Aucun réapprovisionnement requis", font=("Helvetica", 12), bg="#ffffff", fg="#388E3C").grid(row=3, column=0, sticky="w", pady=4)

    # Cadre pour les dépenses liées au stock
    expense_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    expense_frame.pack(pady=10, fill="x")
    
    tk.Label(expense_frame, text="Dépenses liées au Stock : 1,500,000 FCFA pour réapprovisionnement", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    
    # Bouton pour exporter le rapport
    export_button = tk.Button(reports_frame, text="Exporter Rapport", font=("Helvetica", 12), bg="#FF9800", fg="white", relief="raised", command=lambda: export_report())
    export_button.pack(pady=15, ipadx=10, ipady=5)

    return reports_frame


def export_report():
    """
    Fonction pour l'exportation du rapport.
    Actuellement, un message est affiché. À étendre pour exporter un fichier.
    """
    # Code pour exporter le rapport (par exemple en CSV, Excel, ou PDF)
    # Ceci est un exemple d'extension. Vous pouvez ajouter une fonctionnalité pour créer un fichier CSV ou autre.
    messagebox.showinfo("Exporter", "Rapport exporté avec succès !")
