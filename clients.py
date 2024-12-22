import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Ajout du messagebox

# Fonction d'affichage de la section Clients
def create_clients_frame(main_frame):
    clients_frame = tk.Frame(main_frame, bg="#f4f4f9")  # Couleur de fond douce
    tk.Label(clients_frame, text="Gestion des Clients", font=("Helvetica", 18, "bold"), bg="#f4f4f9", fg="#333333").pack(pady=20)

    # **Barre de Recherche**
    search_frame = tk.Frame(clients_frame, bg="#f4f4f9")
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Rechercher un client:", font=("Helvetica", 12), bg="#f4f4f9", fg="#333333").pack(side=tk.LEFT, padx=10)

    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=25, bd=2, relief="solid", highlightthickness=1)
    search_entry.pack(side=tk.LEFT, padx=10)

    def search_clients():
        search_term = search_entry.get().lower()
        # Parcourir tous les clients et masquer ceux qui ne correspondent pas
        for row in clients_treeview.get_children():
            values = clients_treeview.item(row, "values")
            if any(search_term in value.lower() for value in values):
                clients_treeview.item(row, open=True)
            else:
                clients_treeview.item(row, open=False)

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#2196F3", fg="white", command=search_clients)
    search_button.pack(side=tk.LEFT, padx=5)

    # **Tableau des Clients**
    clients_treeview = ttk.Treeview(clients_frame, columns=("Nom", "Téléphone", "Email", "Adresse", "Statut", "Date d'enregistrement"), show="headings")
    clients_treeview.heading("#1", text="Nom")
    clients_treeview.heading("#2", text="Téléphone")
    clients_treeview.heading("#3", text="Email")
    clients_treeview.heading("#4", text="Adresse")
    clients_treeview.heading("#5", text="Statut")
    clients_treeview.heading("#6", text="Date d'enregistrement")

    # Configurer les couleurs alternées pour les lignes du Treeview
    clients_treeview.tag_configure('even', background='#e9e9e9')  # Ligne paire
    clients_treeview.tag_configure('odd', background='#ffffff')  # Ligne impaire

    def insert_client(name, phone, email, address, status, date_registered):
        row_index = len(clients_treeview.get_children())  # Index de la ligne actuelle
        tag = 'even' if row_index % 2 == 0 else 'odd'  # Déterminer si la ligne est paire ou impaire
        clients_treeview.insert("", "end", values=(name, phone, email, address, status, date_registered), tags=(tag,))

    clients_treeview.pack(pady=20, padx=20)

    # Exemple d'insertion de clients
    insert_client("Client A", "01 23 45 67", "clientA@mail.com", "123 Rue Exemple", "Actif", "01/01/2024")
    insert_client("Client B", "01 23 45 68", "clientB@mail.com", "456 Rue Exemple", "Inactif", "15/02/2024")

    # **Ajouter un Client**
    def add_client():
        def save_client():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            address = address_entry.get()
            status = status_var.get()
            date_registered = date_entry.get()

            if name and phone and email and address and date_registered:
                insert_client(name, phone, email, address, status, date_registered)
                add_window.destroy()
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

        add_window = tk.Toplevel(clients_frame)
        add_window.title("Ajouter un Client")

        tk.Label(add_window, text="Nom", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(add_window, text="Téléphone", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(add_window, text="Email", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
        tk.Label(add_window, text="Adresse", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5)
        tk.Label(add_window, text="Statut", font=("Helvetica", 12)).grid(row=4, column=0, padx=10, pady=5)
        tk.Label(add_window, text="Date d'enregistrement", font=("Helvetica", 12)).grid(row=5, column=0, padx=10, pady=5)

        name_entry = tk.Entry(add_window, font=("Helvetica", 12))
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        phone_entry = tk.Entry(add_window, font=("Helvetica", 12))
        phone_entry.grid(row=1, column=1, padx=10, pady=5)
        email_entry = tk.Entry(add_window, font=("Helvetica", 12))
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        address_entry = tk.Entry(add_window, font=("Helvetica", 12))
        address_entry.grid(row=3, column=1, padx=10, pady=5)
        status_var = tk.StringVar(value="Actif")
        status_menu = ttk.Combobox(add_window, values=["Actif", "Inactif"], textvariable=status_var, font=("Helvetica", 12), state="readonly")
        status_menu.grid(row=4, column=1, padx=10, pady=5)
        date_entry = tk.Entry(add_window, font=("Helvetica", 12))
        date_entry.grid(row=5, column=1, padx=10, pady=5)

        save_button = tk.Button(add_window, text="Enregistrer", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=save_client)
        save_button.grid(row=6, column=1, padx=10, pady=20)

    # **Modifier un Client** (fonction modifiée, doit être définie avant le bouton)
    def modify_client():
        selected_item = clients_treeview.selection()
        if selected_item:
            values = clients_treeview.item(selected_item[0])["values"]
            def update_client():
                new_name = name_entry.get()
                new_phone = phone_entry.get()
                new_email = email_entry.get()
                new_address = address_entry.get()
                new_status = status_var.get()
                new_date = date_entry.get()

                clients_treeview.item(selected_item[0], values=(new_name, new_phone, new_email, new_address, new_status, new_date))
                modify_window.destroy()

            modify_window = tk.Toplevel(clients_frame)
            modify_window.title("Modifier Client")

            tk.Label(modify_window, text="Nom", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
            tk.Label(modify_window, text="Téléphone", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
            tk.Label(modify_window, text="Email", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
            tk.Label(modify_window, text="Adresse", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5)
            tk.Label(modify_window, text="Statut", font=("Helvetica", 12)).grid(row=4, column=0, padx=10, pady=5)
            tk.Label(modify_window, text="Date d'enregistrement", font=("Helvetica", 12)).grid(row=5, column=0, padx=10, pady=5)

            name_entry = tk.Entry(modify_window, font=("Helvetica", 12))
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            phone_entry = tk.Entry(modify_window, font=("Helvetica", 12))
            phone_entry.grid(row=1, column=1, padx=10, pady=5)
            email_entry = tk.Entry(modify_window, font=("Helvetica", 12))
            email_entry.grid(row=2, column=1, padx=10, pady=5)
            address_entry = tk.Entry(modify_window, font=("Helvetica", 12))
            address_entry.grid(row=3, column=1, padx=10, pady=5)
            status_var = tk.StringVar(value="Actif")
            status_menu = ttk.Combobox(modify_window, values=["Actif", "Inactif"], textvariable=status_var, font=("Helvetica", 12), state="readonly")
            status_menu.grid(row=4, column=1, padx=10, pady=5)
            date_entry = tk.Entry(modify_window, font=("Helvetica", 12))
            date_entry.grid(row=5, column=1, padx=10, pady=5)

            update_button = tk.Button(modify_window, text="Mettre à jour", font=("Helvetica", 12), bg="#FF9800", fg="white", command=update_client)
            update_button.grid(row=6, column=1, padx=10, pady=20)

        else:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client à modifier.")

    # **Supprimer un Client**
    def delete_client():
        selected_item = clients_treeview.selection()
        if selected_item:
            confirm = messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer ce client ?")
            if confirm:
                clients_treeview.delete(selected_item[0])
        else:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un client à supprimer.")

    # Créer un frame pour aligner les boutons sur la même ligne
    buttons_frame = tk.Frame(clients_frame, bg="#f4f4f9")
    buttons_frame.pack(pady=10)

    add_button = tk.Button(buttons_frame, text="Ajouter un Client", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_client)
    modify_button = tk.Button(buttons_frame, text="Modifier le Client", font=("Helvetica", 12), bg="#FF9800", fg="white", command=modify_client)
    delete_button = tk.Button(buttons_frame, text="Supprimer le Client", font=("Helvetica", 12), bg="#FF5722", fg="white", command=delete_client)

    add_button.pack(side=tk.LEFT, padx=10)
    modify_button.pack(side=tk.LEFT, padx=10)
    delete_button.pack(side=tk.LEFT, padx=10)

    return clients_frame
