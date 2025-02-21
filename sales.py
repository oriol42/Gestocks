import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from tkinter import ttk
import utils

def create_sales_frame(main_frame, conn, sales_history_treeview, totals_treeview, dashboard_treeview, stock_alert_frame, sales_report_frame, stock_report_frame):
    # Créer le cadre principal pour les ventes
    sales_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#f0f0f0")
    ctk.CTkLabel(sales_frame, text="GESTION DES VENTES", font=("Helvetica", 14, "bold"), text_color="#333").pack(pady=10)

    # **Recherche et réinitialisation**
    search_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    search_frame.pack(pady=10)

    search_entry = ctk.CTkEntry(search_frame, font=("Helvetica", 14), width=300)
    search_entry.pack(side=ctk.LEFT, padx=5)

    search_button = ctk.CTkButton(search_frame, text="RECHERCHER", font=("Helvetica", 14), fg_color="#2196F3", text_color="white", command=lambda: utils.search_sales(products_treeview, conn, search_entry))
    search_button.pack(side=ctk.LEFT, padx=5)

    reset_button = ctk.CTkButton(search_frame, text="RÉINITIALISER", font=("Helvetica", 14), fg_color="#FF9800", text_color="white", command=lambda: utils.load_products_sales(products_treeview, conn))
    reset_button.pack(side=ctk.LEFT, padx=5)

    # **Liste des produits disponibles**
    products_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    products_frame.pack(pady=10)

    columns = ("Nom", "Quantité en stock", "Prix de vente", "Prix d'achat")
    products_treeview = ttk.Treeview(products_frame, columns=columns, show="headings", height=6)

    products_treeview.heading("Nom", text="Nom")
    products_treeview.heading("Quantité en stock", text="Quantité en stock")
    products_treeview.heading("Prix de vente", text="Prix de vente")
    products_treeview.heading("Prix d'achat", text="Prix d'achat")

    products_treeview.column("Nom", width=200, anchor="center")
    products_treeview.column("Quantité en stock", width=200, anchor="center")
    products_treeview.column("Prix de vente", width=200, anchor="center")
    products_treeview.column("Prix d'achat", width=200, anchor="center")

    products_treeview.pack(fill=ctk.BOTH, expand=True)
    utils.load_products_sales(products_treeview, conn)

    # **Champ pour la quantité**
    quantity_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    quantity_frame.pack(pady=10)

    ctk.CTkLabel(quantity_frame, text="Quantité :", font=("Helvetica", 14), text_color="#333").pack(side=ctk.LEFT, padx=5)
    quantity_entry = ctk.CTkEntry(quantity_frame, font=("Helvetica", 14), width=40)
    quantity_entry.pack(side=ctk.LEFT, padx=5)
    
    ctk.CTkLabel(quantity_frame, text="Nom du client :", font=("Helvetica", 14), text_color="#333").pack(side=ctk.LEFT, padx=5)
    customer_name_entry = ctk.CTkEntry(quantity_frame, font=("Helvetica", 14), width=200)
    customer_name_entry.pack(side=ctk.LEFT, padx=5)

    # **Boutons d'action : Ajouter et annuler**
    action_buttons_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    action_buttons_frame.pack(pady=10)

    add_button = ctk.CTkButton(action_buttons_frame, text="AJOUTER AU PANIER", font=("Helvetica", 14), fg_color="#4CAF50", text_color="white", command=lambda: [utils.add_to_cart(products_treeview, cart_treeview, quantity_entry, conn), utils.calculate_total(cart_treeview, total_label)])
    add_button.pack(side=ctk.LEFT, padx=10)

    cancel_button = ctk.CTkButton(action_buttons_frame, text="ANNULER LA VENTE", font=("Helvetica", 14), fg_color="#FF5722", text_color="white", command=lambda: utils.cancel_the_sales(cart_treeview, products_treeview, conn, total_label))
    cancel_button.pack(side=ctk.LEFT, padx=10)

    # **Panier**
    cart_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    cart_frame.pack(pady=20)

    ctk.CTkLabel(cart_frame, text="Panier", font=("Helvetica", 16, "bold"), text_color="#333").pack(pady=5)

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

    cart_treeview.pack(fill=ctk.BOTH, expand=True)

    # **Boutons d'action pour le panier**
    cart_actions_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    cart_actions_frame.pack(pady=10)

    generate_invoice_button = ctk.CTkButton(cart_actions_frame, text="GÉNÉRER LA FACTURE", font=("Helvetica", 14), fg_color="#2196F3", text_color="white", command=lambda: [utils.generate_simple_invoice(cart_treeview, conn, sales_history_treeview, dashboard_treeview, stock_alert_frame, sales_report_frame, stock_report_frame,customer_name_entry), utils.update_totals_treeview(totals_treeview), utils.update_dashboard_treeview(dashboard_treeview)])
    generate_invoice_button.pack(side=ctk.LEFT, padx=10)

    empty_button = ctk.CTkButton(cart_actions_frame, text="VIDER LE PANIER", font=("Helvetica", 14), fg_color="#FF5722", text_color="white", command=lambda: utils.cancel_the_cart(cart_treeview, products_treeview, conn, total_label))
    empty_button.pack(side=ctk.LEFT, padx=10)

    # Total
    total_frame = ctk.CTkFrame(sales_frame, corner_radius=10, fg_color="#f0f0f0")
    total_frame.pack(pady=10)

    ctk.CTkLabel(total_frame, text="Total :", font=("Helvetica", 16, "bold"), text_color="#333").pack(side=ctk.LEFT, padx=5)
    total_label = ctk.CTkLabel(total_frame, text="0 FCFA", font=("Helvetica", 16), text_color="#333")
    total_label.pack(side=ctk.LEFT, padx=5)

    # Correction : utilisation de configure() au lieu de config()    
    # Mise à jour du total
    def update_total_label(total):
        total_label.configure(text=f"{total} FCFA")

    return sales_frame, products_treeview
