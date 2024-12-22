import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fonction d'affichage de la section Ventes
def create_sales_frame(main_frame):
    sales_frame = tk.Frame(main_frame, bg="#f0f0f0")
    tk.Label(sales_frame, text="Gestion des Ventes", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=20)

    # **Filtre et tri**
    filter_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    filter_frame.pack(pady=10)

    tk.Label(filter_frame, text="Filtrer par", font=("Helvetica", 12), bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=5)
    filter_options = ["Date", "Statut", "Montant", "Produit"]
    filter_combobox = ttk.Combobox(filter_frame, values=filter_options, font=("Helvetica", 12), state="readonly")
    filter_combobox.pack(side=tk.LEFT, padx=5)

    filter_entry = tk.Entry(filter_frame, font=("Helvetica", 12))
    filter_entry.pack(side=tk.LEFT, padx=5)

    def apply_filter():
        filter_value = filter_entry.get()
        filter_type = filter_combobox.get()
        if filter_value:
            messagebox.showinfo("Filtre appliqué", f"Filtre par {filter_type} avec la valeur : {filter_value}")
        else:
            messagebox.showwarning("Filtre", "Veuillez entrer un terme de recherche.")

    filter_button = tk.Button(filter_frame, text="Appliquer", font=("Helvetica", 12), bg="#2196F3", fg="white", command=apply_filter)
    filter_button.pack(side=tk.LEFT, padx=5)

    # **Liste des ventes récentes**
    sales_history_frame = tk.Frame(sales_frame, bg="#f0f0f0", pady=20)
    sales_history_frame.pack(fill=tk.BOTH, expand=True)

    # Créer un Treeview pour afficher l'historique des ventes
    columns = ("Numéro", "Date", "Client", "Montant", "Statut", "Méthode de paiement")
    sales_history_treeview = ttk.Treeview(sales_history_frame, columns=columns, show="headings")
    
    sales_history_treeview.heading("Numéro", text="Numéro de vente")
    sales_history_treeview.heading("Date", text="Date")
    sales_history_treeview.heading("Client", text="Client")
    sales_history_treeview.heading("Montant", text="Montant")
    sales_history_treeview.heading("Statut", text="Statut")
    sales_history_treeview.heading("Méthode de paiement", text="Méthode de paiement")

    sales_history_treeview.column("Numéro", width=100, anchor="center")
    sales_history_treeview.column("Date", width=100, anchor="center")
    sales_history_treeview.column("Client", width=150, anchor="w")
    sales_history_treeview.column("Montant", width=100, anchor="center")
    sales_history_treeview.column("Statut", width=100, anchor="center")
    sales_history_treeview.column("Méthode de paiement", width=150, anchor="w")

    # Appliquer un style personnalisé avec des couleurs alternées
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30, background="#ffffff", fieldbackground="#f0f0f0", foreground="#333")
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#2196F3", foreground="white")
    
    sales_history_treeview.tag_configure("even", background="#f9f9f9")
    sales_history_treeview.tag_configure("odd", background="#ffffff")

    sales_history_treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Exemples de ventes ajoutées
    sales_history_treeview.insert("", "end", values=("001", "01/12/2024", "Client A", "60,000 FCFA", "Complétée", "Carte bancaire"), tags=("even",))
    sales_history_treeview.insert("", "end", values=("002", "02/12/2024", "Client B", "30,000 FCFA", "En attente", "Virement"), tags=("odd",))
    sales_history_treeview.insert("", "end", values=("003", "03/12/2024", "Client C", "20,000 FCFA", "Annulée", "Cash"), tags=("even",))

    # **Actions rapides**
    actions_frame = tk.Frame(sales_frame, bg="#f0f0f0")
    actions_frame.pack(pady=20)

    def add_sale():
        messagebox.showinfo("Ajout de vente", "Ajout d'une nouvelle vente.")
        # Code pour ajouter une vente à l'historique ici

    def modify_sale():
        selected_item = sales_history_treeview.selection()
        if selected_item:
            messagebox.showinfo("Modifier la vente", "Modification de la vente sélectionnée.")
        else:
            messagebox.showwarning("Sélectionner une vente", "Veuillez sélectionner une vente à modifier.")

    def cancel_sale():
        selected_item = sales_history_treeview.selection()
        if selected_item:
            messagebox.showinfo("Annuler la vente", "La vente a été annulée.")
        else:
            messagebox.showwarning("Sélectionner une vente", "Veuillez sélectionner une vente à annuler.")

    add_button = tk.Button(actions_frame, text="Ajouter une Vente", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_sale, relief="raised", bd=2)
    modify_button = tk.Button(actions_frame, text="Modifier la Vente", font=("Helvetica", 12), bg="#FF9800", fg="white", command=modify_sale, relief="raised", bd=2)
    cancel_button = tk.Button(actions_frame, text="Annuler la Vente", font=("Helvetica", 12), bg="#FF5722", fg="white", command=cancel_sale, relief="raised", bd=2)

    add_button.pack(side=tk.LEFT, padx=10)
    modify_button.pack(side=tk.LEFT, padx=10)
    cancel_button.pack(side=tk.LEFT, padx=10)

    # **Détails de chaque vente**
    def show_sale_details():
        selected_item = sales_history_treeview.selection()
        if selected_item:
            values = sales_history_treeview.item(selected_item[0])["values"]
            messagebox.showinfo("Détails de la Vente", f"Numéro de vente: {values[0]}\nDate: {values[1]}\nClient: {values[2]}\nMontant: {values[3]}\nStatut: {values[4]}\nMéthode de paiement: {values[5]}")
        else:
            messagebox.showwarning("Sélectionner une vente", "Veuillez sélectionner une vente pour voir les détails.")

    details_button = tk.Button(actions_frame, text="Voir Détails", font=("Helvetica", 12), bg="#2196F3", fg="white", command=show_sale_details, relief="raised", bd=2)
    details_button.pack(side=tk.LEFT, padx=10)

    # **Génération de la facture**
    def generate_invoice():
        selected_item = sales_history_treeview.selection()
        if selected_item:
            values = sales_history_treeview.item(selected_item[0])["values"]
            sale_details = f"""
Facture pour la vente N° {values[0]}:

Client: {values[2]}
Date: {values[1]}
Montant: {values[3]}
Statut: {values[4]}
Méthode de paiement: {values[5]}

Merci pour votre achat !"""
            messagebox.showinfo("Générer la Facture", sale_details)
        else:
            messagebox.showwarning("Sélectionner une vente", "Veuillez sélectionner une vente pour générer la facture.")

    invoice_button = tk.Button(actions_frame, text="Générer la Facture", font=("Helvetica", 12), bg="#2196F3", fg="white", command=generate_invoice, relief="raised", bd=2)
    invoice_button.pack(side=tk.LEFT, padx=10)

    return sales_frame
