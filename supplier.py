import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import utils

def create_suppliers_frame(main_frame, conn):
    suppliers_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#f8f9fa")
    ctk.CTkLabel(suppliers_frame, text="Gestion des Fournisseurs", font=("Helvetica", 18, "bold"), text_color="#333").pack(pady=20)

    # **Barre de recherche**
    search_frame = ctk.CTkFrame(suppliers_frame, corner_radius=10, fg_color="#f8f9fa")
    search_frame.pack(pady=10)

    ctk.CTkLabel(search_frame, text="Rechercher un fournisseur par :", font=("Helvetica", 14), text_color="#333").pack(side=ctk.LEFT, padx=10)

    # Option pour choisir le critère de recherche (Nom ou Produit livré)
    search_criteria = tk.StringVar(value="Nom")
    criteria_menu = ctk.CTkOptionMenu(search_frame, variable=search_criteria, values=["Nom", "Produit livré"], font=("Helvetica", 14),)
    criteria_menu.pack(side=ctk.LEFT, padx=10)

    search_entry = ctk.CTkEntry(search_frame, font=("Helvetica", 14), width=80)
    search_entry.pack(side=ctk.LEFT, padx=10)

    # Fonction de recherche qui sera appelée lors du clic sur le bouton
    def search_suppliers():
        search_value = search_entry.get().strip()  # Récupérer la valeur de recherche
        if search_value:
            criteria = search_criteria.get()  # Récupérer le critère choisi (Nom ou Produit livré)
            # Appeler la fonction search_supplier pour rechercher par le critère sélectionné
            utils.search_supplier(suppliers_treeview, conn, search_value, criteria)
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un critère de recherche.", parent=suppliers_frame)

    search_button = ctk.CTkButton(search_frame, text="Rechercher", font=("Helvetica", 14), fg_color="#2196F3", text_color="white", command=search_suppliers)
    search_button.pack(side=ctk.LEFT, padx=5)

    reset_button = ctk.CTkButton(search_frame, text="Rafraichir", font=("Helvetica", 14), fg_color="#2196F3", text_color="white", command=lambda: utils.load_suppliers_from_db(suppliers_treeview, conn))
    reset_button.pack(side=ctk.LEFT, padx=5)

    # **Tableau des fournisseurs avec barre de défilement**
    suppliers_treeview_frame = ctk.CTkFrame(suppliers_frame)
    suppliers_treeview_frame.pack(pady=20, padx=20, fill=ctk.X)

    suppliers_treeview = ttk.Treeview(
        suppliers_treeview_frame,
        columns=("Nom", "Contact", "Adresse", "Email", "Produit livré"),
        show="headings"
    )
    suppliers_treeview.heading("#1", text="Nom")
    suppliers_treeview.heading("#2", text="Contact")
    suppliers_treeview.heading("#3", text="Adresse")
    suppliers_treeview.heading("#4", text="Email")
    suppliers_treeview.heading("#5", text="Produit livré")

    # **Barres de défilement classiques**
    vsb = tk.Scrollbar(suppliers_treeview_frame, orient="vertical", command=suppliers_treeview.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    hsb = tk.Scrollbar(suppliers_treeview_frame, orient="horizontal", command=suppliers_treeview.xview)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)

    suppliers_treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    suppliers_treeview.pack(fill=ctk.BOTH, expand=True)

    # Charger les fournisseurs depuis la base de données
    utils.load_suppliers_from_db(suppliers_treeview, conn)

    # Boutons pour ajouter, modifier et supprimer
    button_frame = ctk.CTkFrame(suppliers_frame, corner_radius=10, fg_color="#f4f4f9")
    button_frame.pack(pady=20)

    add_button = ctk.CTkButton(button_frame, text="Ajouter", font=("Helvetica", 14), fg_color="#4CAF50", text_color="white", command=lambda: utils.add_supplier(suppliers_treeview, conn))
    add_button.pack(side=ctk.LEFT, padx=10)

    edit_button = ctk.CTkButton(button_frame, text="Modifier", font=("Helvetica", 14), fg_color="#FFC107", text_color="white", command=lambda: utils.edit_supplier(suppliers_treeview, conn))
    edit_button.pack(side=ctk.LEFT, padx=10)

    delete_button = ctk.CTkButton(button_frame, text="Supprimer", font=("Helvetica", 14), fg_color="#F44336", text_color="white", command=lambda: utils.delete_supplier(suppliers_treeview, conn))
    delete_button.pack(side=ctk.LEFT, padx=10)

    return suppliers_frame
