import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def create_stocks_frame(main_frame):
    stocks_frame = tk.Frame(main_frame, bg="#f8f9fa")  # Fond de l'interface
    tk.Label(stocks_frame, text="Gestion des Stocks", font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#333").pack(pady=20)

    # Zone de recherche pour rechercher un produit
    search_frame = tk.Frame(stocks_frame, bg="#f8f9fa")
    search_frame.pack(pady=10)

    # Label et champ de recherche
    tk.Label(search_frame, text="Rechercher un produit", font=("Helvetica", 12), bg="#f8f9fa", fg="#333").pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, font=("Helvetica", 12))
    search_entry.pack(side=tk.LEFT, padx=5)

    # Fonction de recherche
    def search_product():
        search_term = search_entry.get()
        if search_term:
            messagebox.showinfo("Recherche", f"Recherche pour: {search_term}")
        else:
            messagebox.showwarning("Recherche", "Veuillez entrer un terme de recherche")

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#2196F3", fg="white", command=search_product)
    search_button.pack(side=tk.LEFT, padx=5)

    # Tri et filtres des produits
    filter_frame = tk.Frame(stocks_frame, bg="#f8f9fa")
    filter_frame.pack(pady=10)

    # Menu déroulant pour filtrer par catégorie
    categories = ["Toutes", "Électronique", "Vêtements", "Meubles", "Accessoires"]
    tk.Label(filter_frame, text="Filtrer par Catégorie", font=("Helvetica", 12), bg="#f8f9fa", fg="#333").pack(side=tk.LEFT, padx=10)
    category_filter = ttk.Combobox(filter_frame, values=categories, font=("Helvetica", 12))
    category_filter.set("Toutes")  # Valeur par défaut
    category_filter.pack(side=tk.LEFT, padx=10)

    # Fonction pour appliquer les filtres
    def filter_products():
        selected_category = category_filter.get()
        messagebox.showinfo("Filtrer", f"Filtrer par catégorie : {selected_category}")

    tk.Button(filter_frame, text="Appliquer les filtres", font=("Helvetica", 12), bg="#64b5f6", fg="white", command=filter_products).pack(side=tk.LEFT, padx=10)

    # Tableau des produits disponibles
    stock_treeview = ttk.Treeview(stocks_frame, columns=("Nom", "Quantité", "Prix", "Fournisseur", "Date d'ajout", "Catégorie"), show="headings", height=8)

    # Titre des colonnes
    stock_treeview.heading("#1", text="Nom", anchor="w")
    stock_treeview.heading("#2", text="Quantité", anchor="w")
    stock_treeview.heading("#3", text="Prix (FCFA)", anchor="w")
    stock_treeview.heading("#4", text="Fournisseur", anchor="w")
    stock_treeview.heading("#5", text="Date d'ajout", anchor="w")
    stock_treeview.heading("#6", text="Catégorie", anchor="w")

    # Style de police et de couleur pour améliorer la lisibilité
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30)  # Taille de la police et hauteur de ligne
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="#000000", background="#64b5f6")  # Couleur du texte des en-têtes en noir
    style.configure("Treeview", background="#ffffff", fieldbackground="#f8f9fa", foreground="#333333")  # Couleurs des lignes

    # Définir explicitement la couleur du fond pour l'en-tête
    stock_treeview.tag_configure("even", background="#f5f5f5")
    stock_treeview.tag_configure("odd", background="#ffffff")

    stock_treeview.pack(pady=20, padx=20)

    # Simuler l'ajout de produits avec les informations complètes
    produits = [
        ("Produit A", 120, 12000, "Fournisseur A", "01/12/2024", "Électronique"),
        ("Produit B", 80, 8500, "Fournisseur B", "03/12/2024", "Vêtements"),
        ("Produit C", 150, 10000, "Fournisseur C", "05/12/2024", "Électronique")
    ]

    for produit in produits:
        nom, quantite, prix, fournisseur, date_ajout, categorie = produit
        stock_treeview.insert("", "end", values=(nom, quantite, f"{prix} FCFA", fournisseur, date_ajout, categorie))

    # Appliquer une couleur d'arrière-plan alternée
    for i, child in enumerate(stock_treeview.get_children()):
        if i % 2 == 0:
            stock_treeview.item(child, tags=("even",))  # Lignes paires
        else:
            stock_treeview.item(child, tags=("odd",))   # Lignes impaires

    # Options d'ajout, suppression et modification des stocks
    button_frame = tk.Frame(stocks_frame, bg="#f8f9fa")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Ajouter un Produit", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=lambda: messagebox.showinfo("Ajouter", "Produit ajouté")).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Supprimer un Produit", font=("Helvetica", 12), bg="#FF5722", fg="white", command=lambda: messagebox.showinfo("Supprimer", "Produit supprimé")).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Modifier un Produit", font=("Helvetica", 12), bg="#FF9800", fg="white", command=lambda: messagebox.showinfo("Modifier", "Produit modifié")).pack(side=tk.LEFT, padx=10)

    return stocks_frame
