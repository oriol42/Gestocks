import tkinter as tk
from tkinter import ttk, messagebox
import utils

def create_suppliers_frame(main_frame, conn):
    suppliers_frame = tk.Frame(main_frame, bg="#f4f4f9")  # Couleur de fond plus douce
    tk.Label(suppliers_frame, text="Gestion des Fournisseurs", font=("Helvetica", 18, "bold"), bg="#f4f4f9", fg="#333333").pack(pady=20)

    # **Barre de recherche**
    search_frame = tk.Frame(suppliers_frame, bg="#f4f4f9")
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Rechercher un fournisseur par :", font=("Helvetica", 12), bg="#f4f4f9", fg="#333333").pack(side=tk.LEFT, padx=10)

    # Option pour choisir le critère de recherche (Nom ou Produit livré)
    search_criteria = tk.StringVar(value="Nom")
    criteria_menu = tk.OptionMenu(search_frame, search_criteria, "Nom", "Produit livré")
    criteria_menu.pack(side=tk.LEFT, padx=10)

    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=25, bd=2, relief="solid", highlightthickness=1)
    search_entry.pack(side=tk.LEFT, padx=10)

    # Fonction de recherche qui sera appelée lors du clic sur le bouton
    def search_suppliers():
        search_value = search_entry.get().strip()  # Récupérer la valeur de recherche
        if search_value:
            criteria = search_criteria.get()  # Récupérer le critère choisi (Nom ou Produit livré)
            # Appeler la fonction search_supplier pour rechercher par le critère sélectionné
            utils.search_supplier(suppliers_treeview, conn, search_value, criteria)
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un critère de recherche.", parent=suppliers_frame)

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#2196F3", fg="white", command=search_suppliers)
    search_button.pack(side=tk.LEFT, padx=5)
    reset_button = tk.Button(search_frame, text="Rafraichir", font=("Helvetica", 12), bg="#2196F3", fg="white", command = lambda: utils.load_suppliers_from_db(suppliers_treeview,conn))
    reset_button.pack(side=tk.LEFT, padx=5)

    # **Tableau des fournisseurs avec barre de défilement**
    suppliers_treeview_frame = tk.Frame(suppliers_frame)
    suppliers_treeview_frame.pack(pady=20, padx=20, fill=tk.X)

    suppliers_treeview = ttk.Treeview(
        suppliers_treeview_frame,
        columns=("Nom", "Contact", "Adresse", "Téléphone", "Email", "Produit livré", "Historique Commandes"),
        show="headings"
    )
    suppliers_treeview.heading("#1", text="Nom")
    suppliers_treeview.heading("#2", text="Contact")
    suppliers_treeview.heading("#3", text="Adresse")
    suppliers_treeview.heading("#4", text="Téléphone")
    suppliers_treeview.heading("#5", text="Email")
    suppliers_treeview.heading("#6", text="Produit livré")
    suppliers_treeview.heading("#7", text="Historique Commandes")

    # **Barres de défilement**
    vsb = tk.Scrollbar(suppliers_treeview_frame, orient="vertical", command=suppliers_treeview.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    hsb = tk.Scrollbar(suppliers_treeview_frame, orient="horizontal", command=suppliers_treeview.xview)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)

    suppliers_treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    suppliers_treeview.pack(fill=tk.BOTH, expand=True)

    # Charger les fournisseurs depuis la base de données
    utils.load_suppliers_from_db(suppliers_treeview, conn)

    # Boutons pour ajouter, modifier et supprimer
    button_frame = tk.Frame(suppliers_frame, bg="#f4f4f9")
    button_frame.pack(pady=20)

    add_button = tk.Button(button_frame, text="Ajouter", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=lambda: utils.add_supplier(suppliers_treeview, conn))
    add_button.pack(side=tk.LEFT, padx=10)

    edit_button = tk.Button(button_frame, text="Modifier", font=("Helvetica", 12), bg="#FFC107", fg="white", command=lambda: utils.edit_supplier(suppliers_treeview, conn))
    edit_button.pack(side=tk.LEFT, padx=10)

    delete_button = tk.Button(button_frame, text="Supprimer", font=("Helvetica", 12), bg="#F44336", fg="white", command=lambda: utils.delete_supplier(suppliers_treeview, conn))
    delete_button.pack(side=tk.LEFT, padx=10)

    return suppliers_frame