import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import utils

def create_sales_frame(main_frame, conn, sales_history_treeview, totals_treeview,dashboard_treeview,stock_alert_frame,sales_report_frame,stock_report_frame):
    # Créer le cadre principal pour les ventes
    sales_frame = tk.Frame(main_frame, bg="#f0f0f0")
    tk.Label(sales_frame, text="GESTION DES VENTES", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

    # **Sélection du client** : Ajouter un menu déroulant pour choisir le client
    client_selection_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    client_selection_frame.pack(pady=10)

    # Label pour le menu déroulant
    tk.Label(client_selection_frame, text="Sélectionner le client :", font=("Helvetica", 12), bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=5)

    # **Menu déroulant pour la sélection du client**  
    # La liste des clients sera récupérée depuis le backend (fonction à coder côté backend)
    client_combobox = ttk.Combobox(client_selection_frame, font=("Helvetica", 12), width=30)
    client_combobox.pack(side=tk.LEFT, padx=5)

    # La fonction backend qui récupère les noms de clients de la base de données


    # **Recherche et réinitialisation**
    search_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    search_frame.pack(pady=10)

    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="RECHERCHER", font=("Helvetica", 12), bg="#2196F3", fg="white", command=lambda: utils.search_sales(products_treeview, conn, search_entry))
    search_button.pack(side=tk.LEFT, padx=5)

    reset_button = tk.Button(search_frame, text="RÉINITIALISER", font=("Helvetica", 12), bg="#FF9800", fg="white", command=lambda: utils.load_products_sales(products_treeview, conn))
    reset_button.pack(side=tk.LEFT, padx=5)

    # **Liste des produits disponibles**
    products_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    products_frame.pack(pady=10)

    columns = ("Nom", "Quantité en stock", "Prix de vente","Prix d'achat")
    products_treeview = ttk.Treeview(products_frame, columns=columns, show="headings", height=6)

    products_treeview.heading("Nom", text="Nom")
    products_treeview.heading("Quantité en stock", text="Quantité en stock")
    products_treeview.heading("Prix de vente", text="Prix de vente")
    products_treeview.heading("Prix d'achat", text="Prix d'achat")

    products_treeview.column("Nom", width=200, anchor="center")
    products_treeview.column("Quantité en stock", width=200, anchor="center")
    products_treeview.column("Prix de vente", width=200, anchor="center")
    products_treeview.column("Prix d'achat", width=200, anchor="center")

    products_treeview.pack(fill=tk.BOTH, expand=True)
    utils.load_products_sales(products_treeview, conn)

    # **Champ pour la quantité**
    quantity_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    quantity_frame.pack(pady=10)

    tk.Label(quantity_frame, text="Quantité :", font=("Helvetica", 12), bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=5)
    quantity_entry = tk.Entry(quantity_frame, font=("Helvetica", 12), width=10)
    quantity_entry.pack(side=tk.LEFT, padx=5)

    # **Boutons d'action : Ajouter et annuler**
    action_buttons_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    action_buttons_frame.pack(pady=10)

    add_button = tk.Button(action_buttons_frame, text="AJOUTER AU PANIER", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=lambda: [utils.add_to_cart(products_treeview, cart_treeview, quantity_entry, conn), utils.calculate_total(cart_treeview, total_label)])
    add_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(action_buttons_frame, text="ANNULER LA VENTE", font=("Helvetica", 12), bg="#FF5722", fg="white", command=lambda: utils.cancel_the_sales(cart_treeview, products_treeview, conn, total_label))
    cancel_button.pack(side=tk.LEFT, padx=10)

    # **Panier**
    cart_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    cart_frame.pack(pady=20)

    tk.Label(cart_frame, text="Panier", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#333").pack(pady=5)

    cart_columns = ("Nom", "Quantité", "Prix", "Prix total")
    cart_treeview = ttk.Treeview(cart_frame, columns=cart_columns, show="headings", height=2)

    cart_treeview.heading("Nom", text="Nom")
    cart_treeview.heading("Quantité", text="Quantité")
    cart_treeview.heading("Prix", text="Prix")
    cart_treeview.heading("Prix total", text="Prix total")

    cart_treeview.column("Nom", width=200, anchor="center")
    cart_treeview.column("Quantité", width=100, anchor="center")
    cart_treeview.column("Prix", width=100, anchor="center")
    cart_treeview.column("Prix total", width=150, anchor="center")

    cart_treeview.pack(fill=tk.BOTH, expand=True)

    # **Boutons d'action pour le panier**
    cart_actions_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    cart_actions_frame.pack(pady=10)

    generate_invoice_button = tk.Button(cart_actions_frame, text="GÉNÉRER LA FACTURE", font=("Helvetica", 12), bg="#2196F3", fg="white", command=lambda: [utils.generate_simple_invoice(cart_treeview, conn, sales_history_treeview,dashboard_treeview,stock_alert_frame,sales_report_frame,stock_report_frame), utils.update_totals_treeview(totals_treeview),utils.update_dashboard_treeview(dashboard_treeview)])
    generate_invoice_button.pack(side=tk.LEFT, padx=10)

    empty_button = tk.Button(cart_actions_frame, text="VIDER LE PANIER", font=("Helvetica", 12), bg="#FF5722", fg="white", command=lambda: utils.cancel_the_cart(cart_treeview, products_treeview, conn, total_label))
    empty_button.pack(side=tk.LEFT, padx=10)

    # Total
    total_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    total_frame.pack(pady=10)

    tk.Label(total_frame, text="Total :", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=5)
    total_label = tk.Label(total_frame, text="0 FCFA", font=("Helvetica", 14), bg="#f0f0f0", fg="#333")
    total_label.pack(side=tk.LEFT, padx=5)

    return sales_frame, products_treeview
