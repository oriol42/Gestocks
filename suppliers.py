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
        search_term = search_entry.get().lower()
        for row in suppliers_treeview.get_children():
            values = suppliers_treeview.item(row, "values")
            if any(search_term in value.lower() for value in values):
                suppliers_treeview.item(row, tags="show")
            else:
                suppliers_treeview.item(row, tags="hide")
        
        # Appliquer visibilité selon les tags "show" ou "hide"
        for row in suppliers_treeview.get_children():
            if suppliers_treeview.item(row, "tags") == "show":
                suppliers_treeview.item(row, open=True)
            else:
                suppliers_treeview.item(row, open=False)

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#2196F3", fg="white", command=search_suppliers)
    search_button.pack(side=tk.LEFT, padx=5)

    # **Tableau des fournisseurs**
    suppliers_treeview = ttk.Treeview(suppliers_frame, columns=("Nom", "Contact", "Adresse", "Téléphone", "Email"), show="headings")
    suppliers_treeview.heading("#1", text="Nom")
    suppliers_treeview.heading("#2", text="Contact")
    suppliers_treeview.heading("#3", text="Adresse")
    suppliers_treeview.heading("#4", text="Téléphone")
    suppliers_treeview.heading("#5", text="Email")

    def apply_row_colors():
        for i, row in enumerate(suppliers_treeview.get_children()):
            if i % 2 == 0:  # Ligne paire
                suppliers_treeview.tag_configure(f"even_row", background="#f9f9f9")
                suppliers_treeview.item(row, tags="even_row")
            else:  # Ligne impaire
                suppliers_treeview.tag_configure(f"odd_row", background="#ffffff")
                suppliers_treeview.item(row, tags="odd_row")

    suppliers_treeview.pack(pady=20, padx=20, fill=tk.X)
    suppliers_treeview.insert("", "end", values=("Fournisseur A", "contact@fournisseurA.com", "123 Rue Exemple", "01 23 45 67", "contact@fournisseurA.com"))
    suppliers_treeview.insert("", "end", values=("Fournisseur B", "contact@fournisseurB.com", "456 Rue Exemple", "01 23 45 68", "contact@fournisseurB.com"))
    apply_row_colors()

    # **Ajouter un fournisseur**
    def add_supplier():
        def save_supplier():
            name = name_entry.get()
            contact = contact_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()

            if name and contact and address and phone and email:
                suppliers_treeview.insert("", "end", values=(name, contact, address, phone, email))
                apply_row_colors()
                add_window.destroy()
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

        add_window = tk.Toplevel(suppliers_frame)
        add_window.title("Ajouter un Fournisseur")

        tk.Label(add_window, text="Nom", font=("Helvetica", 12)).pack(padx=10, pady=5)
        tk.Label(add_window, text="Contact", font=("Helvetica", 12)).pack(padx=10, pady=5)
        tk.Label(add_window, text="Adresse", font=("Helvetica", 12)).pack(padx=10, pady=5)
        tk.Label(add_window, text="Téléphone", font=("Helvetica", 12)).pack(padx=10, pady=5)
        tk.Label(add_window, text="Email", font=("Helvetica", 12)).pack(padx=10, pady=5)

        name_entry = tk.Entry(add_window, font=("Helvetica", 12))
        name_entry.pack(padx=10, pady=5)
        contact_entry = tk.Entry(add_window, font=("Helvetica", 12))
        contact_entry.pack(padx=10, pady=5)
        address_entry = tk.Entry(add_window, font=("Helvetica", 12))
        address_entry.pack(padx=10, pady=5)
        phone_entry = tk.Entry(add_window, font=("Helvetica", 12))
        phone_entry.pack(padx=10, pady=5)
        email_entry = tk.Entry(add_window, font=("Helvetica", 12))
        email_entry.pack(padx=10, pady=5)

        tk.Button(add_window, text="Enregistrer", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=save_supplier).pack(pady=10)

    # Bouton pour ajouter un fournisseur
    add_button = tk.Button(suppliers_frame, text="Ajouter un fournisseur", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_supplier)
    add_button.pack(pady=20)

    return suppliers_frame
