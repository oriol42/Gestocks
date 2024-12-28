import tkinter as tk
from tkinter import messagebox, ttk

def create_suppliers_frame(main_frame):
    suppliers_frame = tk.Frame(main_frame, bg="#f4f4f9")  # Couleur de fond plus douce
    tk.Label(suppliers_frame, text="Gestion des Fournisseurs", font=("Helvetica", 18, "bold"), bg="#f4f4f9", fg="#333333").pack(pady=20)

    # **Barre de recherche**
    search_frame = tk.Frame(suppliers_frame, bg="#f4f4f9")
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Rechercher un fournisseur:", font=("Helvetica", 12), bg="#f4f4f9", fg="#333333").pack(side=tk.LEFT, padx=10)

    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=25, bd=2, relief="solid", highlightthickness=1)
    search_entry.pack(side=tk.LEFT, padx=10)

    def search_suppliers():
        #fonction pour rechercher un fournisseur
        pass

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#2196F3", fg="white", command=search_suppliers)
    search_button.pack(side=tk.LEFT, padx=5)

    # **Tableau des fournisseurs avec barre de défilement**
    suppliers_treeview_frame = tk.Frame(suppliers_frame)
    suppliers_treeview_frame.pack(pady=20, padx=20, fill=tk.X)

    suppliers_treeview = ttk.Treeview(suppliers_treeview_frame, columns=("Nom", "Contact", "Adresse", "Téléphone", "Email", "Statut", "Historique Commandes"), show="headings")
    suppliers_treeview.heading("#1", text="Nom")
    suppliers_treeview.heading("#2", text="Contact")
    suppliers_treeview.heading("#3", text="Adresse")
    suppliers_treeview.heading("#4", text="Téléphone")
    suppliers_treeview.heading("#5", text="Email")
    suppliers_treeview.heading("#6", text="Statut")
    suppliers_treeview.heading("#7", text="Historique Commandes")

    # **Barres de défilement**
    vsb = tk.Scrollbar(suppliers_treeview_frame, orient="vertical", command=suppliers_treeview.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    hsb = tk.Scrollbar(suppliers_treeview_frame, orient="horizontal", command=suppliers_treeview.xview)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)

    suppliers_treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    suppliers_treeview.pack(fill=tk.BOTH, expand=True)

    # Insérer des lignes d'exemple
    suppliers_treeview.insert("", "end", values=("Fournisseur A", "contact@fournisseurA.com", "123 Rue Exemple", "01 23 45 67", "contact@fournisseurA.com", "Actif", "Commande #1, #2"))
    suppliers_treeview.insert("", "end", values=("Fournisseur B", "contact@fournisseurB.com", "456 Rue Exemple", "01 23 45 68", "contact@fournisseurB.com", "Inactif", "Commande #3"))

    # **Appliquer les couleurs des lignes**
    def apply_row_colors():
        suppliers_treeview.tag_configure("even_row", background="#f9f9f9")  # Ligne paire
        suppliers_treeview.tag_configure("odd_row", background="#ffffff")  # Ligne impaire
        
        for i, row in enumerate(suppliers_treeview.get_children()):
            if i % 2 == 0:  # Ligne paire
                suppliers_treeview.item(row, tags="even_row")
            else:  # Ligne impaire
                suppliers_treeview.item(row, tags="odd_row")

    apply_row_colors()

    # **Ajouter un fournisseur**
    def add_supplier():
        #ajouter un fournisseur
        pass

    # Bouton pour ajouter un fournisseur
    add_button = tk.Button(suppliers_frame, text="Ajouter un fournisseur", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_supplier)
    add_button.pack(pady=20)

    return suppliers_frame
