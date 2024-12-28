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
    
    # Calculs dynamiques des informations de ventes
    # Exemple : Récupération du chiffre d'affaires et des ventes totales
    chiffre_affaires = get_chiffre_affaires()  # Remplacer par le calcul dynamique
    ventes_totales = get_ventes_totales()  # Remplacer par le calcul dynamique
    
    # Utilisation de grid pour l'alignement compact
    tk.Label(sales_frame, text=f"Chiffre d'Affaires : {chiffre_affaires} FCFA", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    tk.Label(sales_frame, text=f"Ventes Totales : {ventes_totales} FCFA (Mois)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=1, column=0, sticky="w", pady=4)
    
    # Calculs des ventes par produit (dynamique)
    produits_ventes = get_ventes_par_produit()  # Remplacer par la récupération dynamique des ventes par produit
    for i, (produit, details) in enumerate(produits_ventes.items()):
        tk.Label(sales_frame, text=f"Ventes par Produit : {produit} ({details['unités']} unités, {details['chiffre']} FCFA)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=i + 2, column=0, sticky="w", pady=4)
    
    # Calcul des ventes par client (dynamique)
    clients_ventes = get_ventes_par_client()  # Remplacer par la récupération dynamique des ventes par client
    for i, (client, montant) in enumerate(clients_ventes.items()):
        tk.Label(sales_frame, text=f"Ventes par Client : {client} ({montant} FCFA)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=len(produits_ventes) + 2 + i, column=0, sticky="w", pady=4)
    
    # Comparaison des ventes avec le mois précédent (dynamique)
    comparaison_ventes = get_comparaison_ventes()  # Remplacer par le calcul dynamique
    tk.Label(sales_frame, text=f"Comparaison des Ventes : {comparaison_ventes}", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=len(produits_ventes) + len(clients_ventes) + 2, column=0, sticky="w", pady=4)
    
    # Cadre pour les rapports de stocks
    stock_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    stock_frame.pack(pady=10, fill="x")
    
    # Calculs dynamiques des informations de stock
    stock_obsolete = get_stock_obsolete()  # Remplacer par la récupération dynamique du stock obsolète
    for produit, quantite in stock_obsolete.items():
        tk.Label(stock_frame, text=f"Stock Obsolète : {produit} ({quantite} unités)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    
    # Mouvement de stock par catégorie (dynamique)
    mouvement_stock = get_mouvement_stock()  # Remplacer par la récupération dynamique du mouvement de stock
    for categorie, details in mouvement_stock.items():
        tk.Label(stock_frame, text=f"Mouvement de Stock par Catégorie : {categorie} ({details['entrées']} entrées, {details['sorties']} sorties)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=1, column=0, sticky="w", pady=4)
    
    # Rentabilité par produit (dynamique)
    rentabilite_par_produit = get_rentabilite_par_produit()  # Remplacer par la récupération dynamique des rentabilités
    for produit, marge in rentabilite_par_produit.items():
        tk.Label(stock_frame, text=f"Rentabilité par Produit : {produit} ({marge}% de marge)", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=2, column=0, sticky="w", pady=4)
    
    # Indicateur de Stock Optimal : produit à réapprovisionner
    stock_levels = get_niveaux_stock()  # Remplacer par la récupération dynamique des niveaux de stock
    low_stock_threshold = 5  # Seuil de réapprovisionnement
    
    low_stock_products = [product for product, stock in stock_levels.items() if stock < low_stock_threshold]
    if low_stock_products:
        tk.Label(stock_frame, text=f"Réapprovisionnement requis : {', '.join(low_stock_products)}", font=("Helvetica", 12), bg="#ffffff", fg="#D32F2F").grid(row=3, column=0, sticky="w", pady=4)
    else:
        tk.Label(stock_frame, text="Aucun réapprovisionnement requis", font=("Helvetica", 12), bg="#ffffff", fg="#388E3C").grid(row=3, column=0, sticky="w", pady=4)

    # Cadre pour les dépenses liées au stock
    expense_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    expense_frame.pack(pady=10, fill="x")
    
    # Calcul dynamique des dépenses liées au stock
    depenses_stock = get_depenses_stock()  # Remplacer par la récupération dynamique des dépenses liées au stock
    tk.Label(expense_frame, text=f"Dépenses liées au Stock : {depenses_stock} FCFA pour réapprovisionnement", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    
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

# Définition des fonctions de calcul dynamique (exemples)

def get_chiffre_affaires():
    # Remplacer par le calcul réel du chiffre d'affaires
    return 6000000  # Exemple statique, à remplacer par une logique dynamique

def get_ventes_totales():
    # Remplacer par le calcul des ventes totales
    return 9000000  # Exemple statique, à remplacer par une logique dynamique

def get_ventes_par_produit():
    # Remplacer par le calcul des ventes par produit
    return {
        "Produit A": {"unités": 200, "chiffre": 2000000},
        "Produit B": {"unités": 150, "chiffre": 1500000}
    }

def get_ventes_par_client():
    # Remplacer par le calcul des ventes par client
    return {
        "Client X": 2500000,
        "Client Y": 3000000
    }

def get_comparaison_ventes():
    # Remplacer par le calcul de la comparaison des ventes avec le mois précédent
    return "+10%"  # Exemple statique, à remplacer par une logique dynamique

def get_stock_obsolete():
    # Remplacer par le calcul du stock obsolète
    return {"Produit B": 5}

def get_mouvement_stock():
    # Remplacer par le calcul du mouvement de stock par catégorie
    return {"Catégorie X": {"entrées": 20, "sorties": 10}}

def get_rentabilite_par_produit():
    # Remplacer par le calcul de la rentabilité par produit
    return {"Produit A": 40}  # Marge en %

def get_niveaux_stock():
    # Remplacer par le calcul des niveaux de stock
    return {"Produit A": 10, "Produit B": 3, "Produit C": 20}

def get_depenses_stock():
    # Remplacer par le calcul des dépenses liées au stock
    return 1500000  # Exemple statique, à remplacer par une logique dynamique

    return reports_frame


def export_report():
    """
    Fonction pour l'exportation du rapport.
    Actuellement, un message est affiché. À étendre pour exporter un fichier.
    """
    # Code pour exporter le rapport (par exemple en CSV, Excel, ou PDF)
    # Ceci est un exemple d'extension. Vous pouvez ajouter une fonctionnalité pour créer un fichier CSV ou autre.
    messagebox.showinfo("Exporter", "Rapport exporté avec succès !")
