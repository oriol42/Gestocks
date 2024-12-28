import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fonction d'affichage de la section Clients
def create_clients_frame(main_frame):
    clients_frame = tk.Frame(main_frame, bg="#f4f4f9")  # Couleur de fond douce
    tk.Label(clients_frame, text="Gestion des Clients", font=("Helvetica", 18, "bold"), bg="#f4f4f9", fg="#333333").pack(pady=20)

    # **Zone de Recherche**
    search_frame = tk.Frame(clients_frame, bg="#f4f4f9")
    search_frame.pack(pady=10, padx=10, fill=tk.X)

    search_label = tk.Label(search_frame, text="Rechercher un Client:", font=("Helvetica", 12), bg="#f4f4f9", fg="#333333")
    search_label.pack(side=tk.LEFT, padx=5)

    # Limiter la largeur du champ de recherche pour éviter qu'il prenne trop d'espace
    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bg="#ffffff", width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    def search_client():
        """
        Cette fonction doit être utilisée par le backend pour filtrer les résultats
        dans le tableau en fonction du texte de recherche saisi. Une fois que l'utilisateur
        clique sur le bouton de recherche, le backend doit filtrer les clients par nom,
        email, ou autre critère, et afficher les résultats dans le Treeview.
        """
        pass

    search_button = tk.Button(search_frame, text="Rechercher", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=search_client)
    search_button.pack(side=tk.LEFT, padx=10)

    # **Tableau des Clients avec Scrollbars**
    treeview_frame = tk.Frame(clients_frame)
    treeview_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    clients_treeview = ttk.Treeview(treeview_frame, columns=("Nom", "Téléphone", "Email", "Adresse", "Statut", "Date d'enregistrement"), show="headings")
    clients_treeview.heading("#1", text="Nom")
    clients_treeview.heading("#2", text="Téléphone")
    clients_treeview.heading("#3", text="Email")
    clients_treeview.heading("#4", text="Adresse")
    clients_treeview.heading("#5", text="Statut")
    clients_treeview.heading("#6", text="Date d'enregistrement")

    # Configurer les couleurs alternées pour les lignes du Treeview
    clients_treeview.tag_configure('even', background='#e9e9e9')  # Ligne paire
    clients_treeview.tag_configure('odd', background='#ffffff')  # Ligne impaire

    # Fonction d'insertion d'un client dans le Treeview
    def insert_client(name, phone, email, address, status, date_registered):
        """
        Insère un nouveau client dans le tableau des clients (Treeview).
        Cette fonction est appelée par le backend pour ajouter un client
        dans l'interface.
        """
        row_index = len(clients_treeview.get_children())  # Index de la ligne actuelle
        tag = 'even' if row_index % 2 == 0 else 'odd'  # Déterminer si la ligne est paire ou impaire
        clients_treeview.insert("", "end", values=(name, phone, email, address, status, date_registered), tags=(tag,))

    # Exemple d'insertion de clients (cette partie doit être remplacée par l'insertion dynamique via backend)
    insert_client("Client A", "01 23 45 67", "clientA@mail.com", "123 Rue Exemple", "Actif", "01/01/2024")
    insert_client("Client B", "01 23 45 68", "clientB@mail.com", "456 Rue Exemple", "Inactif", "15/02/2024")

    # Scrollbar verticale
    y_scrollbar = tk.Scrollbar(treeview_frame, orient="vertical", command=clients_treeview.yview)
    clients_treeview.configure(yscrollcommand=y_scrollbar.set)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Scrollbar horizontale
    x_scrollbar = tk.Scrollbar(treeview_frame, orient="horizontal", command=clients_treeview.xview)
    clients_treeview.configure(xscrollcommand=x_scrollbar.set)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    clients_treeview.pack(fill=tk.BOTH, expand=True)

    # **Ajouter un Client**
    def add_client():
        """
        Cette fonction doit être utilisée pour ouvrir un formulaire permettant à
        l'utilisateur d'ajouter un nouveau client. Une fois le formulaire rempli, 
        le backend doit appeler insert_client() pour ajouter le client à l'interface.
        """
        pass

    # **Modifier un Client**
    def modify_client():
        """
        Cette fonction permet de modifier les données d'un client sélectionné dans le Treeview.
        Une fois les modifications effectuées, il faut appeler insert_client() pour mettre à jour
        l'affichage du client dans le Treeview.
        """
        pass

    # **Supprimer un Client**
    def delete_client():
        """
        Cette fonction permet de supprimer un client sélectionné dans le Treeview.
        Le backend doit gérer la suppression et mettre à jour l'interface en conséquence.
        """
        pass

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
