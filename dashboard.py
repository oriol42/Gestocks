import tkinter as tk

# Fonction d'affichage du tableau de bord
def create_dashboard_frame(main_frame):
    # Frame principale du tableau de bord
    dashboard_frame = tk.Frame(main_frame, bg="#f4f6f9", padx=20, pady=20)
    
    # Titre du tableau de bord
    title_label = tk.Label(dashboard_frame, text="Tableau de Bord", font=("Helvetica", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
    title_label.pack(pady=20)

    # Résumé des ventes récentes
    sales_summary_frame = tk.Frame(dashboard_frame, bg="#ffffff", pady=10, padx=20, bd=2, relief="groove")
    sales_summary_frame.pack(fill=tk.X, pady=10)

    # Section des Ventes récentes
    sales_title = tk.Label(sales_summary_frame, text="Résumé des ventes récentes", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#3498db")
    sales_title.pack(pady=10)

    # Affichage des informations de vente
    sales_data = [
        ("Ventes du jour", "150,000 FCFA"),
        ("Ventes du mois", "1,200,000 FCFA"),
        ("Stock disponible", "120 articles"),
        ("Produits en rupture de stock", "5 produits"),
    ]
    
    for label, value in sales_data:
        sales_label = tk.Label(sales_summary_frame, text=f"{label}: {value}", font=("Helvetica", 12), bg="#ffffff", fg="#34495e")
        sales_label.pack(pady=5)

    # Section des alertes de stock faible
    stock_alert_frame = tk.Frame(dashboard_frame, bg="#ffffff", pady=10, padx=20, bd=2, relief="groove")
    stock_alert_frame.pack(fill=tk.X, pady=20)

    stock_alert_title = tk.Label(stock_alert_frame, text="Alertes de Stock Faible", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#e74c3c")
    stock_alert_title.pack(pady=10)

    # Produits en rupture de stock avec 20 produits
    low_stock_items = [
        ("Produit X", "10 unités restantes"),
        ("Produit Y", "5 unités restantes"),
        ("Produit Z", "2 unités restantes"),
        ("Produit A", "3 unités restantes"),
        ("Produit B", "4 unités restantes"),
        ("Produit C", "1 unité restante"),
        ("Produit D", "7 unités restantes"),
        ("Produit E", "8 unités restantes"),
        ("Produit F", "5 unités restantes"),
        ("Produit G", "9 unités restantes"),
        ("Produit H", "2 unités restantes"),
        ("Produit I", "3 unités restantes"),
        ("Produit J", "6 unités restantes"),
        ("Produit K", "4 unités restantes"),
        ("Produit L", "2 unités restantes"),
        ("Produit M", "10 unités restantes"),
        ("Produit N", "5 unités restantes"),
        ("Produit O", "1 unité restante"),
        ("Produit P", "8 unités restantes"),
        ("Produit Q", "9 unités restantes"),
    ]

    # Utilisation d'un canvas et barre de défilement pour gérer une longue liste
    canvas = tk.Canvas(stock_alert_frame)
    scrollbar = tk.Scrollbar(stock_alert_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)

    # Frame interne pour contenir les alertes avec une barre de défilement
    alert_container = tk.Frame(canvas, bg="#ffffff")

    # Utilisation de grid pour organiser les alertes en plusieurs colonnes
    num_columns = 3  # Nombre de colonnes
    row = 0
    col = 0

    for product, stock in low_stock_items:
        # Créer un cadre pour chaque produit avec des bordures et un fond coloré
        alert_card = tk.Frame(alert_container, bg="#ecf0f1", bd=1, relief="solid", padx=15, pady=10, width=250)
        alert_card.grid(row=row, column=col, padx=10, pady=5)

        # Label pour afficher le nom du produit et la quantité restante
        alert_label = tk.Label(alert_card, text=f"{product}: {stock}", font=("Helvetica", 12), bg="#ecf0f1", fg="#e74c3c")
        alert_label.pack()

        # Mettre une couleur de fond différente pour les alertes critiques
        if "1 unité restante" in stock:
            alert_card.config(bg="#f8d7da")  # Fond rouge clair pour alerte critique

        # Mettre à jour les indices de la grille
        col += 1
        if col >= num_columns:
            col = 0
            row += 1

    # Affichage de la barre de défilement
    canvas.create_window((0, 0), window=alert_container, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mettre à jour la région visible du canvas
    alert_container.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Section des mises à jour de stock
    stock_update_frame = tk.Frame(dashboard_frame, bg="#ffffff", pady=10, padx=20, bd=2, relief="groove")
    stock_update_frame.pack(fill=tk.X, pady=20)

    stock_update_title = tk.Label(stock_update_frame, text="Dernières mises à jour de stock", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#8e44ad")
    stock_update_title.pack(pady=10)

    stock_updates = [
        ("Produit A", "Ajouté", "50 unités"),
        ("Produit B", "Retiré", "10 unités"),
        ("Produit C", "Ajouté", "30 unités"),
    ]

    for product, action, quantity in stock_updates:
        update_label = tk.Label(stock_update_frame, text=f"{product} - {action}: {quantity}", font=("Helvetica", 12), bg="#ffffff", fg="#7f8c8d")
        update_label.pack(pady=5)

    return dashboard_frame
