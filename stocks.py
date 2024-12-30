import tkinter as tk
from tkinter import ttk, messagebox
import utils  #Importer les fonctions nécessaires

def create_stocks_frame(main_frame, conn, sales_frame, products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame):
    stocks_frame = tk.Frame(main_frame, bg="#f8f9fa")  # Fond de l'interface
    tk.Label(stocks_frame, text="Gestion des Stocks", font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#333").pack(pady=20)

    # Zone de recherche pour rechercher un produit
    search_frame = tk.Frame(stocks_frame, bg="#f8f9fa")
    search_frame.pack(pady=10)

    # Label et champ de recherche
    tk.Label(search_frame, text="Rechercher un produit", font=("Helvetica", 12), bg="#f8f9fa", fg="#333").pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, font=("Helvetica", 12))
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#2196F3", fg="white", command=lambda: utils.search_product(stock_treeview, conn, search_entry))
    search_button.pack(side=tk.LEFT, padx=5)
    
    # Ajouter un bouton pour réinitialiser le tableau
    reset_button = tk.Button(search_frame, text="Rafraichir", font=("Helvetica", 12), bg="#FF9800", fg="white", 
                              command=lambda: utils.reset_table(stock_treeview, conn))
    reset_button.pack(side=tk.LEFT, padx=10)

    # Tri et filtres des produits
    filter_frame = tk.Frame(stocks_frame, bg="#f8f9fa")
    filter_frame.pack(pady=10)

    # Menu déroulant pour filtrer par catégorie
    tk.Label(filter_frame, text="Filtrer par Catégorie", font=("Helvetica", 12), bg="#f8f9fa", fg="#333").pack(side=tk.LEFT, padx=10)

    # Combobox pour les catégories, mais elle est initialisée vide.
    category_filter = ttk.Combobox(filter_frame, values=[], font=("Helvetica", 12))
    category_filter.pack(side=tk.LEFT, padx=10)

    # Fonction pour appliquer les filtres
    tk.Button(filter_frame, text="Appliquer les filtres", font=("Helvetica", 12), bg="#64b5f6", fg="white", 
              command=lambda: utils.filter_product(stock_treeview, conn, category_filter)).pack(side=tk.LEFT, padx=10)

    # Frame pour contenir le Treeview et les scrollbars
    treeview_frame = tk.Frame(stocks_frame)
    treeview_frame.pack(pady=20, padx=20)

    # Barre de défilement verticale
    vertical_scrollbar = tk.Scrollbar(treeview_frame, orient="vertical")
    vertical_scrollbar.pack(side=tk.RIGHT, fill="y")

    # Barre de défilement horizontale
    horizontal_scrollbar = tk.Scrollbar(treeview_frame, orient="horizontal")
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill="x")

    # Tableau des produits disponibles
    stock_treeview = ttk.Treeview(treeview_frame, columns=("Nom", "Quantité", "Prix", "Fournisseur", "Date d'ajout", "Catégorie", "Prix d'achat de l'unité"), 
                                  show="headings", height=8, yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    # Titre des colonnes
    stock_treeview.heading("#1", text="Nom", anchor="w")
    stock_treeview.heading("#2", text="Quantité", anchor="w")
    stock_treeview.heading("#3", text="Prix de vente (FCFA)", anchor="w")
    stock_treeview.heading("#4", text="Fournisseur", anchor="w")
    stock_treeview.heading("#5", text="Date d'ajout", anchor="w")
    stock_treeview.heading("#6", text="Catégorie", anchor="w")
    stock_treeview.heading("#7", text="Prix d'achat de l'unité", anchor="w")

    # Style de police et de couleur pour améliorer la lisibilité
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30)  # Taille de la police et hauteur de ligne
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="#000000", background="#64b5f6")  # Couleur du texte des en-têtes en noir
    style.configure("Treeview", background="#ffffff", fieldbackground="#f8f9fa", foreground="#333333")  # Couleurs des lignes

    stock_treeview.pack(fill="both", expand=True)

    # Configurer les scrollbars
    vertical_scrollbar.config(command=stock_treeview.yview)
    horizontal_scrollbar.config(command=stock_treeview.xview)

    # Charger les produits depuis la base de données
    utils.load_products(stock_treeview, conn)

    # Options d'ajout, suppression et modification des stocks
    button_frame = tk.Frame(stocks_frame, bg="#f8f9fa")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Ajouter un Produit", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=lambda: utils.add_product(stock_treeview, conn, products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Supprimer un Produit", font=("Helvetica", 12), bg="#FF5722", fg="white", command=lambda: utils.delete_product(stock_treeview, conn, products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Modifier un Produit", font=("Helvetica", 12), bg="#FF9800", fg="white", command=lambda: utils.modify_product(stock_treeview, conn, products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame)).pack(side=tk.LEFT, padx=10)
    
    return stocks_frame
