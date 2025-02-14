import customtkinter as ctk
from tkinter import ttk, messagebox
import utils  # Importer les fonctions nécessaires

def create_stocks_frame(main_frame, conn, sales_frame, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame):
    stocks_frame = ctk.CTkFrame(main_frame, fg_color="#f8f9fa")  
    ctk.CTkLabel(stocks_frame, text="Gestion des Stocks", font=("Helvetica", 18, "bold"), text_color="#333").pack(pady=20)

    # Zone de recherche 
    search_frame = ctk.CTkFrame(stocks_frame, fg_color="#f8f9fa")
    search_frame.pack(pady=10)

    ctk.CTkLabel(search_frame, text="Rechercher un produit", font=("Helvetica", 14), text_color="#333").pack(side="left", padx=8)
    search_entry = ctk.CTkEntry(search_frame, font=("Helvetica", 14), width=200)
    search_entry.pack(side="left", padx=8)

    search_button = ctk.CTkButton(search_frame, text="Rechercher", font=("Helvetica", 14), fg_color="#2196F3", command=lambda: utils.search_product(stock_treeview, conn, search_entry))
    search_button.pack(side="left", padx=8)
    
    reset_button = ctk.CTkButton(search_frame, text="Rafraîchir", font=("Helvetica", 14), fg_color="#FF9800", command=lambda: utils.reset_table(stock_treeview, conn))
    reset_button.pack(side="left", padx=10)

    # Tri et filtres des produits
    filter_frame = ctk.CTkFrame(stocks_frame, fg_color="#f8f9fa")
    filter_frame.pack(pady=10)

    ctk.CTkLabel(filter_frame, text="Filtrer par Catégorie", font=("Helvetica", 14), text_color="#333").pack(side="left", padx=10)

    categories = utils.get_categories(conn)  
    category_filter = ctk.CTkComboBox(filter_frame, values=categories, font=("Helvetica", 14), state="readonly", width=180)
    category_filter.pack(side="left", padx=10)

    ctk.CTkButton(filter_frame, text="Appliquer les filtres", font=("Helvetica", 14), fg_color="#64b5f6", command=lambda: utils.filter_product(stock_treeview, conn, category_filter)).pack(side="left", padx=10)

    # Conteneur du Treeview
    treeview_frame = ctk.CTkFrame(stocks_frame)
    treeview_frame.pack(pady=20, padx=20, fill="both", expand=True)

    vertical_scrollbar = ctk.CTkScrollbar(treeview_frame, orientation="vertical")
    vertical_scrollbar.pack(side="right", fill="y")

    horizontal_scrollbar = ctk.CTkScrollbar(treeview_frame, orientation="horizontal")
    horizontal_scrollbar.pack(side="bottom", fill="x")

    stock_treeview = ttk.Treeview(treeview_frame, columns=("Nom", "Quantité", "Prix", "Fournisseur", "Date d'ajout", "Catégorie", "Prix d'achat de l'unité"), 
                                  show="headings", height=10, yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    # Configuration des colonnes
    stock_treeview.heading("#1", text="Nom", anchor="w")
    stock_treeview.heading("#2", text="Quantité", anchor="w")
    stock_treeview.heading("#3", text="Prix de vente (FCFA)", anchor="w")
    stock_treeview.heading("#4", text="Fournisseur", anchor="w")
    stock_treeview.heading("#5", text="Date d'ajout", anchor="w")
    stock_treeview.heading("#6", text="Catégorie", anchor="w")
    stock_treeview.heading("#7", text="Prix d'achat de l'unité", anchor="w")
    
    stock_treeview.column("#7", width=220, anchor="w")

    # Style du Treeview avec alternance des couleurs
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 13), rowheight=30, background="#ffffff", fieldbackground="#f8f9fa", foreground="#333333")
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="#000000", background="#64b5f6")

    # Alternance des couleurs des lignes
    style.map("Treeview", background=[('selected', '#64b5f6')])  # Couleur de sélection si nécessaire
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    stock_treeview.pack(fill="both", expand=True)

    vertical_scrollbar.configure(command=stock_treeview.yview)
    horizontal_scrollbar.configure(command=stock_treeview.xview)

    utils.load_products(stock_treeview, conn)

    # Boutons d'actions
    button_frame = ctk.CTkFrame(stocks_frame, fg_color="#f8f9fa")
    button_frame.pack(pady=20)

    ctk.CTkButton(button_frame, text="Ajouter un Produit", font=("Helvetica", 14), fg_color="#4CAF50", height=40, width=200,
                  command=lambda: utils.add_product(stock_treeview, conn, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame, category_filter)).pack(side="left", padx=10)

    ctk.CTkButton(button_frame, text="Supprimer un Produit", font=("Helvetica", 14), fg_color="#FF5722", height=40, width=200,
                  command=lambda: utils.delete_product(stock_treeview, conn, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame, category_filter)).pack(side="left", padx=10)

    ctk.CTkButton(button_frame, text="Modifier un Produit", font=("Helvetica", 14), fg_color="#FF9800", height=40, width=200,
                  command=lambda: utils.modify_product(stock_treeview, conn, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame, category_filter)).pack(side="left", padx=10)

    return stocks_frame
