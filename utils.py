import tkinter as tk
from tkinter import ttk, messagebox,simpledialog
import os
import sqlite3
from datetime import datetime,timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser



def show_frame(frame_name, frames, expand=True, fill="both"):
    """
    Affiche le cadre correspondant au nom donné.

    Paramètres :
    frame_name (str) : Le nom de la frame à afficher.
    frames (dict) : Un dictionnaire contenant les frames, avec leurs noms comme clés.
    expand (bool) : Si True, le cadre occupe tout l'espace disponible. Par défaut, True.
    fill (str) : Direction dans laquelle la frame doit être étendue. Par défaut, "both".
    """
    # Vérifier si le nom de la frame existe dans le dictionnaire des frames
    if frame_name not in frames:
        raise ValueError(f"Le cadre '{frame_name}' n'existe pas dans les frames.")
    
    # Masquer toutes les autres frames
    for frame in frames.values():
        frame.pack_forget()
    
    # Afficher la frame sélectionnée
    frames[frame_name].pack(fill=fill, expand=expand)

# Fonction pour établir la connexion à la base de données
def connect_database():
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)
    return conn


# Fonction pour vérifier et mettre à jour la structure de la table
def update_table_structure(conn):
    cursor = conn.cursor()
    # Créer la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            prix REAL NOT NULL,
            fournisseur TEXT  NULL,
            DateAjout TEXT NOT NULL,
            categorie TEXT DEFAULT 'Non spécifiée',
            PrixAchatUnite REAL NOT NULL
        )
    """)
    conn.commit()


# Fonction pour charger les produits dans le Treeview
def load_products(stock_treeview, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT nom, quantite, prix, fournisseur, DateAjout, categorie, PrixAchatUnite FROM stocks")
    produits = cursor.fetchall()

    for produit in produits:
        nom, quantite, prix, fournisseur, date_ajout, categorie, PrixAchatUnite = produit
        stock_treeview.insert("", "end", values=(nom, quantite, f"{prix:.2f}", fournisseur, date_ajout, categorie, PrixAchatUnite))


# Fonction pour ajouter un produit
def add_product(stock_treeview, conn,products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame):
    def submit_product():
        nom = entry_nom.get()
        quantite = entry_quantite.get()
        prix = entry_prix.get()
        fournisseur = entry_fournisseur.get() or "Non spécifié"  # Fournisseur par défaut
        categorie = category_combobox.get()
        date_ajout = datetime.now().strftime("%d/%m/%Y")
        PrixAchatUnite = entry_PrixAchatUnite.get()

        if not (nom and quantite and prix and categorie and PrixAchatUnite):
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            quantite = int(quantite)
            prix = float(prix)
            PrixAchatUnite = float(PrixAchatUnite)
        except ValueError:
            messagebox.showerror("Erreur de saisie", "Quantité, Prix et Prix d'achat de l'unité doivent être des nombres.")
            return

        # Vérifier si le produit existe déjà (basé sur le nom)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM stocks WHERE LOWER(nom) = LOWER(?)", (nom,))
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Redondance", f"Le produit '{nom}' existe déjà dans le tableau des stocks.")
            return

        # Insérer dans la base de données
        cursor.execute("""
            INSERT INTO stocks (nom, quantite, prix, fournisseur, DateAjout, categorie, PrixAchatUnite)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nom, quantite, prix, fournisseur, date_ajout, categorie, PrixAchatUnite))
        conn.commit()

        # Ajouter dans le Treeview
        stock_treeview.insert("", "end", values=(nom, quantite, f"{prix:.2f}", fournisseur, date_ajout, categorie, f"{PrixAchatUnite:.2f}"))
        load_products_sales(products_treeview,conn)
        messagebox.showinfo("Succès", "Produit ajouté avec succès.")
        load_low_stock_alerts(stock_alert_frame)
        update_dashboard_treeview(dashboard_treeview)
        update_stocks_report_frame(stock_report_frame)
        add_window.destroy()

    # Fenêtre pour ajouter un produit
    add_window = tk.Toplevel()
    add_window.title("Ajouter un Produit")
    add_window.geometry("400x400")

    tk.Label(add_window, text="Nom :", font=("arial", 9)).grid(row=0, column=0, sticky="w", padx=12, pady=12)
    entry_nom = tk.Entry(add_window, font=("arial", 9))
    entry_nom.grid(row=0, column=1, padx=12, pady=12)

    tk.Label(add_window, text="Quantité :", font=("arial", 9)).grid(row=1, column=0, sticky="w", padx=12, pady=12)
    entry_quantite = tk.Entry(add_window, font=("arial", 9))
    entry_quantite.grid(row=1, column=1, padx=12, pady=12)

    tk.Label(add_window, text="Prix de vente :", font=("arial", 9)).grid(row=2, column=0, sticky="w", padx=12, pady=12)
    entry_prix = tk.Entry(add_window, font=("arial", 9))
    entry_prix.grid(row=2, column=1, padx=12, pady=12)

    tk.Label(add_window, text="Fournisseur :", font=("arial", 9)).grid(row=3, column=0, sticky="w", padx=12, pady=12)
    entry_fournisseur = tk.Entry(add_window, font=("arial", 9))
    entry_fournisseur.grid(row=3, column=1, padx=12, pady=12)

    tk.Label(add_window, text="Catégorie :", font=("arial", 9)).grid(row=4, column=0, sticky="w", padx=12, pady=12)
    categories = [] #vide pour l'instant
    category_combobox = ttk.Combobox(add_window, values=categories, font=("arial", 9))
    category_combobox.grid(row=4, column=1, padx=12, pady=12)
    
    tk.Label(add_window, text="Prix d'achat de l'unité :", font=("arial", 9)).grid(row=5, column=0, sticky="w", padx=12, pady=12)
    entry_PrixAchatUnite = tk.Entry(add_window, font=("arial", 9))
    entry_PrixAchatUnite.grid(row=5, column=1, padx=12, pady=12)

    tk.Button(add_window, text="Ajouter", font=("arial", 9), bg="#4CAF50", fg="white", command=submit_product).grid(row=6, column=1, sticky="w", padx=12, pady=12)
    
def delete_product(stock_treeview, conn,products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame):
    # Récupérer l'élément sélectionné dans le Treeview
    selected_item = stock_treeview.selection()
    if not selected_item:
        messagebox.showwarning("Sélection requise", "Veuillez sélectionner un produit à supprimer.")
        return

    # Récupérer les valeurs de l'élément sélectionné
    item_values = stock_treeview.item(selected_item[0], "values")
    nom = item_values[0]

    # Confirmer la suppression
    confirm = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le produit '{nom}' ?")
    if confirm:
        # Supprimer du Treeview
        stock_treeview.delete(selected_item)
       

        # Supprimer du produit de la base de données
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stocks WHERE nom = ?", (nom,))
        load_products_sales(products_treeview,conn)
        conn.commit()

        messagebox.showinfo("Succès", f"Produit '{nom}' supprimé avec succès.")
        load_low_stock_alerts(stock_alert_frame)
        update_dashboard_treeview(dashboard_treeview)
        update_stocks_report_frame(stock_report_frame)
    else:
        messagebox.showinfo("Annulé", "Suppression annulée.")
      
        
    
# Fonction pour modifier un produit
def modify_product(stock_treeview, conn,products_treeview,dashboard_treeview,stock_alert_frame,stock_report_frame):
    selected_item = stock_treeview.selection()
    if not selected_item:
        messagebox.showwarning("Sélection requise", "Veuillez sélectionner un produit à modifier.")
        return

    # Récupérer les informations du produit sélectionné
    item = stock_treeview.item(selected_item)
    values = item["values"]
    nom, quantite, prix, fournisseur, date_ajout, categorie, PrixAchatUnite = values

    # Fenêtre pour modifier le produit
    modify_window = tk.Toplevel()
    modify_window.title("Modifier un Produit")
    modify_window.geometry("400x400")

    # Créer les champs de saisie pour les informations du produit
    tk.Label(modify_window, text="Nom :", font=("arial", 9)).grid(padx=12, pady=12, row=0, column=0, sticky="w")
    entry_nom = tk.Entry(modify_window, font=("arial", 9))
    entry_nom.insert(0, nom)
    entry_nom.grid(row=0, column=1, padx=12, pady=12)

    tk.Label(modify_window, text="Quantité :", font=("arial", 9)).grid(row=1, column=0, sticky="w", padx=12, pady=12)
    entry_quantite = tk.Entry(modify_window, font=("arial", 9))
    entry_quantite.insert(0, quantite)
    entry_quantite.grid(row=1, column=1, padx=12, pady=12)

    tk.Label(modify_window, text="Prix de vente :", font=("arial", 9)).grid(row=2, column=0, sticky="w", padx=12, pady=12)
    entry_prix = tk.Entry(modify_window, font=("arial", 9))
    entry_prix.insert(0, prix)
    entry_prix.grid(row=2, column=1, padx=12, pady=12)

    tk.Label(modify_window, text="Fournisseur :", font=("arial", 9)).grid(row=3, column=0, sticky="w", padx=12, pady=12)
    entry_fournisseur = tk.Entry(modify_window, font=("arial", 9))
    entry_fournisseur.insert(0, fournisseur)
    entry_fournisseur.grid(row=3, column=1, padx=12, pady=12)

    tk.Label(modify_window, text="Catégorie :", font=("arial", 9)).grid(row=4, column=0, sticky="w", padx=12, pady=12)
    categories = ["Électronique", "Vêtements", "Meubles", "Accessoires", "Autre"]
    category_combobox = ttk.Combobox(modify_window, values=categories, font=("arial", 9))
    category_combobox.set(categorie)
    category_combobox.grid(row=4, column=1, padx=12, pady=12)
    
    
    tk.Label(modify_window, text="Prix d'achat de l'unité  :", font=("arial", 9)).grid(row=5, column=0, sticky="w", padx=12, pady=12)
    entry_PrixAchatUnite = tk.Entry(modify_window, font=("arial", 9))
    entry_PrixAchatUnite.insert(0, PrixAchatUnite)
    entry_PrixAchatUnite.grid(row=5, column=1, padx=12, pady=12)
    
    
    

    def submit_changes():
        new_nom = entry_nom.get()
        new_quantite = entry_quantite.get()
        new_prix = entry_prix.get()
        new_fournisseur = entry_fournisseur.get() or "Non spécifié"  # Fournisseur par défaut si vide
        new_categorie = category_combobox.get()
        new_PrixAchatUnite = entry_PrixAchatUnite.get()

        if not (new_nom and new_quantite and new_prix and new_categorie and new_PrixAchatUnite):
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            new_quantite = int(new_quantite)
            new_prix = float(new_prix)
            new_PrixAchatUnite = float(new_PrixAchatUnite)
        except ValueError:
            messagebox.showerror("Erreur de saisie", "Quantité, Prix et Prix d'achat de l'unité doivent être des nombres.")
            return

        # Mettre à jour le produit dans la base de données
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stocks
            SET nom = ?, quantite = ?, prix = ?, fournisseur = ?, categorie = ?, PrixAchatUnite = ?
            WHERE nom = ? AND fournisseur = ? AND DateAjout = ?
        """, (new_nom, new_quantite, new_prix, new_fournisseur, new_categorie, new_PrixAchatUnite, nom, fournisseur, date_ajout))
        load_products_sales(products_treeview,conn)
        conn.commit()

        # Mettre à jour le produit dans le Treeview
        stock_treeview.item(selected_item, values=(new_nom, new_quantite, f"{new_prix:.2f}", new_fournisseur, date_ajout, new_categorie, f"{new_PrixAchatUnite}"))

        messagebox.showinfo("Succès", "Produit modifié avec succès.")
        update_dashboard_treeview(dashboard_treeview)
        load_low_stock_alerts(stock_alert_frame)
        update_stocks_report_frame(stock_report_frame)
        
        modify_window.destroy()

    # Bouton pour valider les modifications
    tk.Button(modify_window, text="Modifier", font=("arial", 9), bg="#4CAF50", fg="white", command=submit_changes).grid(row=6, column=1, padx=15, pady=15)
# Fonction pour rechercher un produit
def search_product(stock_treeview, conn, search_entry):
    """
    Recherche un produit dans la base de données et met à jour le Treeview.

    :param stock_treeview: Treeview à mettre à jour
    :param conn: Connexion à la base de données
    :param search_entry: Champ de recherche contenant le terme à chercher
    """
    search_term = search_entry.get().strip().lower()

    if not search_term:
        messagebox.showwarning("Recherche", "Veuillez entrer un terme de recherche.")
        return

    # Effacer les résultats actuels dans le Treeview
    for item in stock_treeview.get_children():
        stock_treeview.delete(item)

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nom, quantite, prix, fournisseur, DateAjout, categorie, PrixAchatUnite
            FROM stocks
            WHERE LOWER(nom) LIKE ? 
            ORDER BY nom ASC
        """, (f"%{search_term}%",))

        produits = cursor.fetchall()

        if not produits:
            messagebox.showinfo("Recherche", f"Aucun produit trouvé pour '{search_term}'.")
            return

        # Afficher les produits trouvés dans le Treeview
        for produit in produits:
            nom, quantite, prix, fournisseur, date_ajout, categorie, PrixAchatUnite = produit
            stock_treeview.insert(
                "",
                "end",
                values=(nom, quantite, f"{prix:.2f} FCFA", fournisseur, date_ajout, categorie, f"{PrixAchatUnite:.2f}")
            )
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la recherche : {e}") 
        
def filter_product(stock_treeview, conn, combobox_entry):
    """
    Recherche un produit dans la base de données et met à jour le Treeview.

    :param stock_treeview: Treeview à mettre à jour
    :param conn: Connexion à la base de données
    :param search_entry: Champ de recherche contenant le terme à chercher
    """
    filter_term = combobox_entry.get().strip().lower()

    if not filter_term:
        messagebox.showwarning("Recherche", "Veuillez entrer un terme de recherche.")
        return

    # Effacer les résultats actuels dans le Treeview
    for item in stock_treeview.get_children():
        stock_treeview.delete(item)

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nom, quantite, prix, fournisseur, DateAjout, categorie, PrixAchatUnite
            FROM stocks
            WHERE LOWER(categorie) LIKE ? 
            ORDER BY nom ASC
        """, (f"%{filter_term}%",))

        produits = cursor.fetchall()

        if not produits:
            messagebox.showinfo("Recherche", f"Aucun produit trouvé pour '{filter_term}'.")
            return

        # Afficher les produits trouvés dans le Treeview
        for produit in produits:
            nom, quantite, prix, fournisseur, date_ajout, categorie, PrixAchatUnite = produit
            stock_treeview.insert(
                "",
                "end",
                values=(nom, quantite, f"{prix:.2f} FCFA", fournisseur, date_ajout, categorie, f"{PrixAchatUnite:.2f}")
            )
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors du filtrage : {e}") 
#Fonction pour reinitialiser le tableau
def reset_table(stock_treeview, conn):
    # Effacer les éléments existants dans le Treeview
    for item in stock_treeview.get_children():
        stock_treeview.delete(item)

    # Recharger tous les produits depuis la base de données
    load_products(stock_treeview, conn)
#fonction pour charger dans le sale treeview
def load_products_sales(products_treeview, conn):
    
    # Vider le Treeview avant de le remplir
    for item in products_treeview.get_children():
        products_treeview.delete(item)

    # Requête SQL pour récupérer les produits (nom, quantité, prix)
    cursor = conn.cursor()
    cursor.execute("SELECT nom, quantite, prix,PrixAchatUnite FROM stocks")
    products = cursor.fetchall()

    # Ajouter les produits au Treeview
    for product in products:
        products_treeview.insert("", "end", values=product)
      
       
def search_sales(sales_treeview, conn, search_entry):
    search_text = search_entry.get().strip()  # Récupérer le texte de recherche

    if not search_text:
        return  # Si aucun texte n'est saisi, on ne fait rien

    # Préparer la requête pour rechercher par nom, quantité ou prix
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nom, quantite, prix FROM stocks
        WHERE nom LIKE ? OR quantite LIKE ? OR prix LIKE ?
    """, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))

    # Effacer les anciennes données dans le Treeview
    for row in sales_treeview.get_children():
        sales_treeview.delete(row)

    # Insérer les résultats de la recherche dans le Treeview
    rows = cursor.fetchall()
    for row in rows:
        sales_treeview.insert("", "end", values=row)

    cursor.close()


def add_to_cart(products_treeview, cart_treeview, quantity_entry, conn):
    selected_item = products_treeview.selection()  # Récupérer l'élément sélectionné
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner un produit.")
        return

    # Récupérer les données du produit sélectionné
    product_name = products_treeview.item(selected_item)["values"][0]
    available_quantity = int(products_treeview.item(selected_item)["values"][1])
    price = float(products_treeview.item(selected_item)["values"][2])

    # Récupérer la quantité saisie
    try:
        quantity_to_sell = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une quantité valide.")
        return

    if quantity_to_sell <= 0:
        messagebox.showerror("Erreur", "La quantité doit être supérieure à zéro.")
        return

    if quantity_to_sell > available_quantity:
        messagebox.showerror("Erreur", "La quantité demandée dépasse la quantité en stock.")
        return

    # Ajouter l'article au panier
    total_price = price * quantity_to_sell
    cart_treeview.insert("", "end", values=(product_name, quantity_to_sell, price, total_price))

    # Mettre à jour la quantité en stock dans le Treeview de vente
    new_available_quantity = available_quantity - quantity_to_sell
    products_treeview.item(selected_item, values=(product_name, new_available_quantity, price))
   

    # Réinitialiser le champ de quantité
    quantity_entry.delete(0, tk.END)
    
def cancel_the_sales(cart_treeview, products_treeview, conn,total_label):
    # Afficher un message de confirmation avant d'annuler
    confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir annuler la vente ?")
    
    if confirm:  # Si l'utilisateur confirme
        # Effacer les éléments existants dans le Treeview du panier
        for item in cart_treeview.get_children():
            cart_treeview.delete(item)
        total_label.config(text="0 FCFA")

        # Recharger tous les produits depuis la base de données
        load_products_sales(products_treeview, conn)
        messagebox.showinfo("Annulation", "La vente a été annulée avec succès.")
    else:
        messagebox.showinfo("Annulation", "L'annulation de la vente a été annulée.")
        
def calculate_total(cart_treeview, total_label):
    total = 0.0
    # Parcourir chaque élément du panier
    for item in cart_treeview.get_children():
        # Récupérer les valeurs de la ligne
        product_name = cart_treeview.item(item, 'values')[0]
        quantity = int(cart_treeview.item(item, 'values')[1])
        price = float(cart_treeview.item(item, 'values')[2])
        
        # Calculer le prix total pour ce produit
        total += quantity * price

    # Mettre à jour l'étiquette du total avec la nouvelle valeur
    total_label.config(text=f"{total} FCFA")
    

def get_product_stock_by_name(product_name, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT quantite FROM stocks WHERE nom = ?", (product_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0



def create_facture_folder():
    """
    Crée le dossier 'factures' dans le dossier 'GESTOCK' pour y stocker toutes les factures.
    """
    # Chemin du dossier GESTOCK
    gestock_folder = os.path.join(os.path.expanduser("~"), "Documents", "GESTOCK")
    
    # Créer le dossier GESTOCK s'il n'existe pas
    if not os.path.exists(gestock_folder):
        os.makedirs(gestock_folder)

    # Créer le sous-dossier 'factures' dans GESTOCK
    facture_folder = os.path.join(gestock_folder, "factures")
    if not os.path.exists(facture_folder):
        os.makedirs(facture_folder)

    return facture_folder

def generate_simple_invoice(cart_treeview, conn, sales_history_treeview, dashboard_treeview, stock_alert_frame, sales_report_frame, stock_report_frame):
    if not cart_treeview.get_children():
        messagebox.showwarning("Panier vide", "Aucun produit dans le panier. Veuillez ajouter des produits avant de générer la facture.")
        return

    # Créer le dossier 'factures' dans 'GESTOCK' si nécessaire
    facture_folder = create_facture_folder()

    # Générer un nom unique pour la facture
    invoice_name = f"Facture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    invoice_path = os.path.join(facture_folder, invoice_name)  # Enregistrer dans le dossier 'factures'

    # Créer un canevas pour la facture
    c = canvas.Canvas(invoice_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "FACTURE")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Date : {datetime.now().strftime('%d/%m/%Y')}")
    c.drawString(50, 700, f"Heure : {datetime.now().strftime('%H:%M:%S')}")

    # Entêtes des colonnes
    c.drawString(50, 650, "Nom du produit")
    c.drawString(200, 650, "Quantité")
    c.drawString(300, 650, "Prix unitaire")
    c.drawString(400, 650, "Prix total")
    c.line(50, 645, 500, 645)

    # Variables pour le total général
    total_general = 0
    y_position = 620

    # Mettre à jour les stocks et écrire les produits dans la facture
    for item in cart_treeview.get_children():
        values = cart_treeview.item(item, "values")
        product_name = values[0]
        quantity_sold = int(values[1])
        unit_price = float(values[2])
        total_price = float(values[3])

        # Ajouter les données dans le PDF
        c.drawString(50, y_position, product_name)
        c.drawString(200, y_position, str(quantity_sold))
        c.drawString(300, y_position, f"{unit_price:.2f}")
        c.drawString(400, y_position, f"{total_price:.2f}")
        y_position -= 20
        total_general += total_price

        # Mettre à jour la quantité dans la base de données
        cursor = conn.cursor()
        cursor.execute("SELECT quantite, PrixAchatUnite FROM stocks WHERE nom = ?", (product_name,))
        result = cursor.fetchone()
        if result:
            current_stock, unit_purchase_price = result
            if current_stock >= quantity_sold:
                new_stock = current_stock - quantity_sold
                cursor.execute("UPDATE stocks SET quantite = ? WHERE nom = ?", (new_stock, product_name))
                
                # Vérifier si une vente existe déjà pour ce produit et cette date
                cursor.execute("SELECT id, quantity FROM sales_history WHERE product_name = ? AND date = ?", 
                               (product_name, datetime.now().strftime('%Y-%m-%d')))
                existing_sale = cursor.fetchone()

                if existing_sale:
                    # Si une vente existe, mettre à jour la quantité, le total, et le prix d'achat unitaire
                    new_quantity = existing_sale[1] + quantity_sold
                    new_total = new_quantity * unit_price
                    cursor.execute(
                        "UPDATE sales_history SET quantity = ?, total_price = ?, unit_purchase_price = ? WHERE id = ?",
                        (new_quantity, new_total, unit_purchase_price, existing_sale[0])
                    )
                else:
                    # Sinon, insérer une nouvelle vente
                    cursor.execute(
                        "INSERT INTO sales_history (date, product_name, quantity, unit_price, total_price, unit_purchase_price) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (datetime.now().strftime('%Y-%m-%d'), product_name, quantity_sold, unit_price, total_price, unit_purchase_price)
                    )
            else:
                messagebox.showerror("Erreur de stock", f"Stock insuffisant pour le produit : {product_name}")
                conn.rollback()
                return
        else:
            messagebox.showerror("Erreur de produit", f"Produit introuvable dans la base de données : {product_name}")
            conn.rollback()
            return

    conn.commit()  # Enregistrer les modifications dans la base de données

    # Ajouter le total général
    c.drawString(50, y_position - 20, f"Total général : {total_general:.2f} FCFA")

    # Sauvegarder et fermer le PDF
    c.save()

    # Vérifier si le fichier existe avant d'essayer de l'ouvrir
    if os.path.exists(invoice_path):
        webbrowser.open(invoice_path)
    else:
        messagebox.showerror("Erreur", f"Le fichier n'a pas été trouvé : {invoice_path}")

    # Afficher un message de confirmation
    messagebox.showinfo("Facture générée", f"Facture générée avec succès : {invoice_path}")
    update_sales_history_treeview(sales_history_treeview, conn)
    update_dashboard_treeview(dashboard_treeview)
    load_low_stock_alerts(stock_alert_frame)
    update_sales_report_frame(sales_report_frame)
    update_stocks_report_frame(stock_report_frame)

   
  
  
def cancel_the_cart(cart_treeview, products_treeview, conn,total_label):
    # Afficher un message de confirmation avant d'annuler
    confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir vider le panier  ?")
    
    if confirm:  # Si l'utilisateur confirme
        # Effacer les éléments existants dans le Treeview du panier
        for item in cart_treeview.get_children():
            cart_treeview.delete(item)
        total_label.config(text="0 FCFA")

        # Recharger tous les produits depuis la base de données
        load_products_sales(products_treeview, conn)
        messagebox.showinfo("Succès", "Panier vidé avec succès.")
    else:
        messagebox.showinfo("Annulation", "Panier non vidé")
        
def update_sales_history_treeview(treeview, conn):
    # Effacer les éléments existants
    for item in treeview.get_children():
        treeview.delete(item)

    # Récupérer les données de l'historique des ventes
    cursor = conn.cursor()
    cursor.execute("SELECT date, product_name, quantity, unit_price, total_price FROM sales_history")
    sales_data = cursor.fetchall()

    # Insérer les nouvelles données dans le Treeview
    for sale in sales_data:
        treeview.insert("", "end", values=sale)

def add_or_update_sale_in_history(conn, product_name, quantity_sold, unit_price, total_price):
    cursor = conn.cursor()

    # Vérifier si le produit est déjà dans l'historique pour la même date
    cursor.execute("SELECT * FROM sales_history WHERE product_name = ? AND date = ?", (product_name, datetime.now().strftime('%Y-%m-%d')))
    existing_sale = cursor.fetchone()

    if existing_sale:
        # Si une entrée existe, vérifier et mettre à jour la quantité et le prix total
        try:
            existing_quantity = int(existing_sale[3])  # La quantité est à l'index 3
            new_quantity = existing_quantity + quantity_sold  # Additionner la quantité
        except ValueError:
            messagebox.showerror("Erreur de données", f"Valeur invalide pour la quantité du produit {product_name}.")
            return  # Retourner si la valeur n'est pas valide

        try:
            existing_total_price = float(existing_sale[5])  # Le prix total est à l'index 5
            new_total_price = existing_total_price + total_price  # Additionner le prix total
        except ValueError:
            messagebox.showerror("Erreur de données", f"Valeur invalide pour le prix du produit {product_name}.")
            return  # Retourner si la valeur n'est pas valide

        # Mise à jour de la quantité et du prix total dans sales_history
        cursor.execute("UPDATE sales_history SET quantity = ?, total_price = ? WHERE product_name = ? AND date = ?",
                       (new_quantity, new_total_price, product_name, datetime.now().strftime('%Y-%m-%d')))
    else:
        # Si aucune vente n'existe, on insère une nouvelle ligne
        cursor.execute("INSERT INTO sales_history (date, product_name, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)",
                       (datetime.now().strftime('%Y-%m-%d'), product_name, quantity_sold, unit_price, total_price))

    conn.commit()  # Sauvegarder les changements dans la base de données
   
  
def update_totals_treeview(totals_treeview):
    # Connexion à la base de données et récupération des données de l'historique des ventes
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer la somme des ventes du jour et du mois
    cursor.execute("SELECT SUM(total_price) AS total_sales FROM sales_history WHERE date = ?", (datetime.today().strftime('%Y-%m-%d'),))
    total_sales_day = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0
    
    cursor.execute("SELECT SUM(total_price) AS total_sales FROM sales_history WHERE strftime('%Y-%m', date) = ?", (datetime.today().strftime('%Y-%m'),))
    total_sales_month = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0

    # Mettre à jour le Treeview des totaux
    # Effacer les anciennes entrées
    for item in totals_treeview.get_children():
        totals_treeview.delete(item)
    
    # Insérer les nouveaux totaux
    totals_treeview.insert("", "end", values=(f"{total_sales_day} FCFA", f"{total_sales_month} FCFA"))
    
def update_dashboard_treeview(dashboard_treeview):
    # Connexion à la base de données et récupération des données de l'historique des ventes
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer la somme des ventes du jour et du mois
    cursor.execute("SELECT SUM(total_price) AS total_sales FROM sales_history WHERE date = ?", (datetime.today().strftime('%Y-%m-%d'),))
    total_sales_day = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0
    
    cursor.execute("SELECT SUM(total_price) AS total_sales FROM sales_history WHERE strftime('%Y-%m', date) = ?", (datetime.today().strftime('%Y-%m'),))
    total_sales_month = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0
    
    #Calculer les depenses
    cursor.execute("SELECT SUM(quantity * unit_purchase_price) AS daily_total_purchase_cost FROM sales_history WHERE date = ?", (datetime.today().strftime('%Y-%m-%d'),))
    daily_total_purchase_cost = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0   
    
    cursor.execute("SELECT SUM(quantity * unit_purchase_price) AS monthly_total_purchase_cost FROM sales_history WHERE strftime('%Y-%m', date) = ?", (datetime.today().strftime('%Y-%m'),))
    monthly_total_purchase_cost = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0
    
    #Calculer les bénéfices
    daily_benefits = total_sales_day - daily_total_purchase_cost
    
    monthly_benefits = total_sales_month - monthly_total_purchase_cost
   
    #Compter la quantité totales de produits en stocks
    cursor.execute("SELECT SUM(quantite) AS in_stocks_quantity FROM stocks ")
    in_stocks_quantity = cursor.fetchone()[0] or 0  # Si aucune vente n'est trouvée, mettre 0
    
    cursor.execute("SELECT COUNT(nom) AS out_of_stock FROM stocks WHERE quantite = 0 ")
    out_of_stock = cursor.fetchone()[0] or 0 # Si aucune vente n'est trouvée, mettre 0

    # Mettre à jour le Treeview des totaux
    # Effacer les anciennes entrées
    for item in dashboard_treeview.get_children():
        dashboard_treeview.delete(item)
    
    # Insérer les nouveaux totaux
    dashboard_treeview.insert("", "end", values=(f"{total_sales_day} FCFA", f"{total_sales_month} FCFA",f"{daily_benefits} FCFA",f"{monthly_benefits} FCFA",f"{in_stocks_quantity} unités",f"{out_of_stock} produits"))
    conn.close()
    
def get_low_stock_items():

    try:
        # Chemin vers la base de données
        db_path = os.path.join(os.path.dirname(__file__), 'DataBase', 'GESTOCK.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Requête pour récupérer le seuil de réapprovisionnement
        cursor.execute("SELECT reorder_point FROM reorder_threshold")
        result = cursor.fetchone()
        
        if result is None:
            print("Aucun seuil de réapprovisionnement trouvé.")
            return []  # Retourne une liste vide si aucune donnée n'est trouvée

        reorder_point = result[0]
        
        # Requête pour récupérer les produits en rupture de stock
        cursor.execute("SELECT nom, quantite FROM stocks WHERE quantite <= ?", (reorder_point,))
        low_stock_items = cursor.fetchall()

        return low_stock_items if low_stock_items else []  # Retourne une liste vide si aucun produit en rupture

    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []  # Retourne une liste vide en cas d'erreur

    finally:
        # Assurez-vous de fermer la connexion à la base de données
        if conn:
            conn.close()
            
def load_low_stock_alerts(stock_alert_frame):
    # Effacer les anciennes alertes (si présentes)
    for widget in stock_alert_frame.winfo_children():
        widget.destroy()

    # Récupérer les produits en rupture de stock ou proches du seuil
    low_stock_items = get_low_stock_items()  # Récupère les produits à faible stock
    
    # Titre de la section
    stock_alert_title = tk.Label(stock_alert_frame, text="Alertes de Stock Faible", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#e74c3c")
    stock_alert_title.pack(pady=10)

    if not low_stock_items:
        # Si aucun produit en rupture de stock
        empty_label = tk.Label(stock_alert_frame, text="Aucune alerte de stock faible", font=("Helvetica", 12), bg="#ffffff", fg="#34495e")
        empty_label.pack(pady=5)
    else:
        # Si des produits en rupture de stock sont trouvés
        canvas = tk.Canvas(stock_alert_frame)
        scrollbar = tk.Scrollbar(stock_alert_frame, orient="vertical", command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        alert_container = tk.Frame(canvas, bg="#ffffff")
        row, col, num_columns = 0, 0, 4  # 4 alertes par ligne

        # Ajouter chaque produit en rupture de stock
        for product, stock in low_stock_items:
            alert_card = tk.Frame(alert_container, bg="#ecf0f1", bd=1, relief="solid", padx=15, pady=10, width=230)
            alert_card.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            alert_label = tk.Label(alert_card, text=f"{product}: {stock}", font=("Helvetica", 12), bg="#ecf0f1", fg="#e74c3c")
            alert_label.pack()
            col += 1
            if col >= num_columns:
                col, row = 0, row + 1

        canvas.create_window((0, 0), window=alert_container, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        alert_container.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
def add_supplier(suppliers_treeview, conn):
    def is_supplier_name_duplicate(name):
        """
        Vérifie si un nom de fournisseur existe déjà dans le Treeview, sans tenir compte de la casse.

        Args:
            name (str): Le nom du fournisseur à vérifier.

        Returns:
            bool: True si le nom existe déjà (indépendamment de la casse), False sinon.
        """
        name = name.lower()  # Convertir le nom à minuscules pour la comparaison
        for row in suppliers_treeview.get_children():
            values = suppliers_treeview.item(row, "values")
            if values and values[0].lower() == name:  # Comparer sans tenir compte de la casse
                return True
        return False

    def save_supplier():
        nom = nom_entry.get().strip()
        contact = contact_entry.get().strip()
        adresse = adresse_entry.get().strip()
        telephone = telephone_entry.get().strip()
        email = email_entry.get().strip()
        produit_livre = produit_livre_entry.get().strip()
        historique_commandes = historique_entry.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire.", parent=add_window)
            return

        # Vérification de duplication
        if is_supplier_name_duplicate(nom):
            messagebox.showwarning("Duplication détectée", f"Le fournisseur '{nom}' existe déjà.", parent=add_window)
            return

        # Ajouter dans la base de données
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fournisseurs (nom, contact, adresse, telephone, email, produit_livre, historique_commandes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nom, contact, adresse, telephone, email, produit_livre, historique_commandes))
        conn.commit()

        # Ajouter dans le Treeview
        suppliers_treeview.insert("", "end", values=(nom, contact, adresse, telephone, email, produit_livre, historique_commandes))
        messagebox.showinfo("Succès", "Fournisseur ajouté avec succès.", parent=add_window)
        add_window.destroy()

    # Fenêtre Toplevel pour ajouter un fournisseur
    add_window = tk.Toplevel()
    add_window.title("Ajouter un fournisseur")
    add_window.geometry("400x400")
    add_window.grab_set()

    # Champs d'entrée
    tk.Label(add_window, text="Nom :").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    nom_entry = tk.Entry(add_window, width=30)
    nom_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)

    tk.Label(add_window, text="Contact :").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    contact_entry = tk.Entry(add_window, width=30)
    contact_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)

    tk.Label(add_window, text="Adresse :").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    adresse_entry = tk.Entry(add_window, width=30)
    adresse_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)

    tk.Label(add_window, text="Téléphone :").grid(row=3, column=0, sticky="w", padx=10, pady=10)
    telephone_entry = tk.Entry(add_window, width=30)
    telephone_entry.grid(row=3, column=1, sticky="w", padx=10, pady=10)

    tk.Label(add_window, text="Email :").grid(row=4, column=0, sticky="w", padx=10, pady=10)
    email_entry = tk.Entry(add_window, width=30)
    email_entry.grid(row=4, column=1, sticky="w", padx=10, pady=10)

    tk.Label(add_window, text="Produit livré :").grid(row=5, column=0, sticky="w", padx=10, pady=10)
    produit_livre_entry = tk.Entry(add_window, width=30)
    produit_livre_entry.grid(row=5, column=1, sticky="w", padx=10, pady=10)

    tk.Label(add_window, text="Historique Commandes :").grid(row=6, column=0, sticky="w", padx=10, pady=10)
    historique_entry = tk.Entry(add_window, width=30)
    historique_entry.grid(row=6, column=1, sticky="w", padx=10, pady=10)

    # Bouton de sauvegarde
    tk.Button(add_window, text="Enregistrer", command=save_supplier).grid(row=7, column=1, padx=10, pady=10)

def delete_supplier(suppliers_treeview, conn):
    selected_item = suppliers_treeview.selection()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner un fournisseur à supprimer.")
        return

    confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce fournisseur ?")
    if confirm:
        # Supprimer de la base de données
        cursor = conn.cursor()
        values = suppliers_treeview.item(selected_item, "values")
        cursor.execute("DELETE FROM fournisseurs WHERE nom = ? AND contact = ?", (values[0], values[1]))
        conn.commit()

        # Supprimer du Treeview
        suppliers_treeview.delete(selected_item)
        messagebox.showinfo("Succès", "Fournisseur supprimé avec succès.")

def edit_supplier(suppliers_treeview, conn):
    selected_item = suppliers_treeview.selection()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner un fournisseur à modifier.")
        return

    current_values = suppliers_treeview.item(selected_item, "values")

    def is_supplier_name_duplicate(name):
        """
        Vérifie si un nom de fournisseur existe déjà dans le Treeview, sans tenir compte de la casse.
        Args:
            name (str): Le nom du fournisseur à vérifier.
        Returns:
            bool: True si le nom existe déjà (indépendamment de la casse), False sinon.
        """
        name = name.lower()  # Convertir le nom à minuscules pour la comparaison
        for row in suppliers_treeview.get_children():
            values = suppliers_treeview.item(row, "values")
            if values and values[0].lower() == name and values[0] != current_values[0]:  # Vérifier sans tenir compte de la casse
                return True
        return False

    def save_changes():
        nom = nom_entry.get().strip()
        contact = contact_entry.get().strip()
        adresse = adresse_entry.get().strip()
        telephone = telephone_entry.get().strip()
        email = email_entry.get().strip()
        produit_livre = produit_livre_entry.get().strip()
        historique_commandes = historique_entry.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire.", parent=edit_window)
            return

        # Vérification de duplication
        if is_supplier_name_duplicate(nom):
            messagebox.showwarning("Duplication détectée", f"Le fournisseur '{nom}' existe déjà.", parent=edit_window)
            return

        # Mettre à jour la base de données
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fournisseurs
            SET nom = ?, contact = ?, adresse = ?, telephone = ?, email = ?, produit_livre = ?, historique_commandes = ?
            WHERE nom = ? AND contact = ?
        """, (nom, contact, adresse, telephone, email, produit_livre, historique_commandes, current_values[0], current_values[1]))
        conn.commit()

        # Mettre à jour le Treeview
        suppliers_treeview.item(selected_item, values=(nom, contact, adresse, telephone, email, produit_livre, historique_commandes))
        messagebox.showinfo("Succès", "Fournisseur modifié avec succès.", parent=edit_window)
        edit_window.destroy()

    # Fenêtre Toplevel pour modifier un fournisseur
    edit_window = tk.Toplevel()
    edit_window.title("Modifier un fournisseur")
    edit_window.geometry("400x400")
    edit_window.grab_set()

    # Champs d'entrée avec valeurs actuelles
    tk.Label(edit_window, text="Nom :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    nom_entry = tk.Entry(edit_window, width=30)
    nom_entry.insert(0, current_values[0])
    nom_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(edit_window, text="Contact :").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    contact_entry = tk.Entry(edit_window, width=30)
    contact_entry.insert(0, current_values[1])
    contact_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    tk.Label(edit_window, text="Adresse :").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    adresse_entry = tk.Entry(edit_window, width=30)
    adresse_entry.insert(0, current_values[2])
    adresse_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    tk.Label(edit_window, text="Téléphone :").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    telephone_entry = tk.Entry(edit_window, width=30)
    telephone_entry.insert(0, current_values[3])
    telephone_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    tk.Label(edit_window, text="Email :").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    email_entry = tk.Entry(edit_window, width=30)
    email_entry.insert(0, current_values[4])
    email_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    tk.Label(edit_window, text="Produit livré :").grid(row=5, column=0, padx=10, pady=10, sticky="w")
    produit_livre_entry = tk.Entry(edit_window, width=30)
    produit_livre_entry.insert(0, current_values[5])
    produit_livre_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    tk.Label(edit_window, text="Historique Commandes :").grid(row=6, column=0, padx=10, pady=10, sticky="w")
    historique_entry = tk.Entry(edit_window, width=30)
    historique_entry.insert(0, current_values[6])
    historique_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    # Bouton de sauvegarde
    tk.Button(edit_window, text="Enregistrer", command=save_changes).grid(row=7, column=1, padx=10, pady=10)

def load_suppliers_from_db(treeview, conn):
    

    """
    Charge les fournisseurs depuis la base de données et les insère dans le Treeview.
    
    Args:
        treeview (ttk.Treeview): Le Treeview où afficher les données.
        conn (sqlite3.Connection): Connexion à la base de données SQLite.
    """
    # Effacer les anciennes données du Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Requête SQL pour récupérer les fournisseurs
    query = "SELECT nom,contact,adresse,telephone,email,produit_livre,historique_commandes FROM fournisseurs"
    cursor = conn.cursor()
    cursor.execute(query)

    # Insérer les données dans le Treeview
    for supplier in cursor.fetchall():
        treeview.insert("", "end", values=supplier)

    cursor.close()
    
def search_supplier(suppliers_treeview, conn, search_value, criteria):
    # Convertir la valeur de recherche en minuscules pour une comparaison insensible à la casse
    search_value = search_value.lower()

    # Vider le Treeview avant d'afficher les résultats
    for row in suppliers_treeview.get_children():
        suppliers_treeview.delete(row)

    # Définir la colonne à rechercher en fonction du critère sélectionné
    if criteria == "Nom":
        column = "nom"
    elif criteria == "Produit livré":
        column = "produit_livre"

    # Requête SQL pour rechercher par le critère choisi
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT nom, contact, adresse, telephone, email, produit_livre, historique_commandes
        FROM fournisseurs
        WHERE LOWER({column}) LIKE ?
    """, (f"%{search_value}%",))

    results = cursor.fetchall()

    # Insérer les résultats dans le Treeview
    for result in results:
        suppliers_treeview.insert("", "end", values=result)
        
def get_chiffre_affaires_mensuel():
    # Connexion à la base de données
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)  # Remplace par ton chemin de base de données
    cursor = conn.cursor()
    
    # Récupération du mois et de l'année actuels
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Requête SQL pour obtenir le total des ventes du mois actuel
    query = """
    SELECT total_price FROM sales_history
    WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
    """
    cursor.execute(query, (str(current_month).zfill(2), str(current_year)))
    
    # Récupération des résultats et calcul du chiffre d'affaires
    total_sales = cursor.fetchall()
    chiffre_affaires = sum([sale[0] for sale in total_sales])  # Additionne toutes les valeurs de total_price
    
    # Fermeture de la connexion à la base de données
    conn.close()
    
    return chiffre_affaires

def get_ventes_par_produit():
    # Connexion à la base de données
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)  # Remplace par ton chemin de base de données
    cursor = conn.cursor()

    # Récupérer la date actuelle et la date du mois en cours
    today = datetime.today().date()
    first_day_of_month = today.replace(day=1)

    # Sélectionner les ventes par produit, quantités et dates
    cursor.execute("""
        SELECT product_name, quantity, date 
        FROM sales_history
        WHERE date BETWEEN ? AND ?
    """, (first_day_of_month, today))

    ventes_par_produit = {}
    for row in cursor.fetchall():
        product_name = row[0]
        quantity = row[1]
        date = row[2]

        # Vérification si le produit existe déjà dans le dictionnaire
        if product_name not in ventes_par_produit:
            ventes_par_produit[product_name] = {"aujourd'hui": 0, "mois": 0}

        # Calcul des ventes par produit (aujourd'hui et ce mois-ci)
        if date == str(today):  # Ventes du jour
            ventes_par_produit[product_name]["aujourd'hui"] += quantity
        ventes_par_produit[product_name]["mois"] += quantity

    conn.close()
    
    return ventes_par_produit

def get_ventes_totales():
    # Connexion à la base de données
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)  # Remplace par ton chemin de base de données
    cursor = conn.cursor()


    # Récupérer la date d'aujourd'hui et du mois actuel
    today = datetime.today().date()
    current_month = today.month
    current_year = today.year

    # Requête pour obtenir les ventes d'aujourd'hui
    cursor.execute("SELECT SUM(quantity) FROM sales_history WHERE date = ?", (today,))
    ventes_aujourdhui = cursor.fetchone()[0] or 0  # 0 si aucun résultat

    # Requête pour obtenir les ventes du mois en cours
    cursor.execute("SELECT SUM(quantity) FROM sales_history WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (str(current_month).zfill(2), str(current_year)))
    ventes_mois = cursor.fetchone()[0] or 0  # 0 si aucun résultat

    # Fermeture de la connexion
    conn.close()

    return ventes_aujourdhui, ventes_mois

def get_comparaison_ventes():
    # Connexion à la base de données
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)  # Remplace par ton chemin de base de données
    cursor = conn.cursor()

    # Dates actuelles et précédentes
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    current_month = today.month
    current_year = today.year

    # Calcul des ventes d'aujourd'hui
    cursor.execute("SELECT SUM(quantity) FROM sales_history WHERE date = ?", (today,))
    ventes_aujourdhui = cursor.fetchone()[0] or 0

    # Calcul des ventes d'hier
    cursor.execute("SELECT SUM(quantity) FROM sales_history WHERE date = ?", (yesterday,))
    ventes_hier = cursor.fetchone()[0] or 0

    # Calcul des ventes de ce mois
    cursor.execute("SELECT SUM(quantity) FROM sales_history WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (str(current_month).zfill(2), str(current_year)))
    ventes_mois = cursor.fetchone()[0] or 0

    # Calcul des ventes du mois précédent
    last_month = (today.replace(day=1) - timedelta(days=1)).month
    last_month_year = (today.replace(day=1) - timedelta(days=1)).year
    cursor.execute("SELECT SUM(quantity) FROM sales_history WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (str(last_month).zfill(2), str(last_month_year)))
    ventes_mois_dernier = cursor.fetchone()[0] or 0

    # Fermeture de la connexion
    conn.close()

    # Calcul des pourcentages
    pourcentage_hier = ((ventes_aujourdhui - ventes_hier) / ventes_hier * 100) if ventes_hier > 0 else 0
    pourcentage_mois = ((ventes_mois - ventes_mois_dernier) / ventes_mois_dernier * 100) if ventes_mois_dernier > 0 else 0

    return round(pourcentage_hier, 2), round(pourcentage_mois, 2)

def update_sales_report_frame(sales_report_frame):
    for widget in sales_report_frame.winfo_children():
        widget.destroy()
        # Calculs dynamiques des informations de ventes
    chiffre_affaire = get_chiffre_affaires_mensuel()  # Calcul du chiffre d'affaire mensuel
    ventes_par_produits = get_ventes_par_produit()  # Calcul des ventes par produit
    ventes_totales_aujourdhui, ventes_totales_mois = get_ventes_totales() #Calcul des ventes totales
    pourcentage_hier, pourcentage_mois = get_comparaison_ventes()
  
    
    # Utilisation de grid pour l'alignement compact
    tk.Label(sales_report_frame, text=f"Chiffre d'Affaires Mensuel : {chiffre_affaire} FCFA", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    
    # Calculs des ventes par produit (dynamique)
    ventes_text = "Ventes par Produits : "
    max_produits_par_ligne = 3  # Nombre maximum de produits par ligne
    produit_count = 0
    
    for produit, details in ventes_par_produits.items():
        ventes_today = details['aujourd\'hui']
        ventes_month = details['mois']
        texte = f"{produit} ({ventes_today} unités aujourd'hui, {ventes_month} unités ce mois)"
        
        if produit_count == max_produits_par_ligne:
            ventes_text += "\n"  # Ajout d'un retour à la ligne
            produit_count = 0  # Réinitialiser le compteur pour la nouvelle ligne
        
        ventes_text += texte + ", "  # Ajouter les informations du produit à la chaîne
        produit_count += 1
    
    # Supprimer la dernière virgule et espace de la chaîne
    ventes_text = ventes_text.rstrip(", ")
    
    # Affichage des ventes par produit
    tk.Label(sales_report_frame, text=ventes_text, font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=1, column=0, sticky="w", pady=4)
    tk.Label(sales_report_frame, text=f"Ventes Totales : {ventes_totales_aujourdhui} unités vendues aujourd'hui, {ventes_totales_mois} unités vendues ce mois ", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=2, column=0, sticky="w", pady=4)
    
    comparaison_text = f"Comparaison des ventes : +{pourcentage_hier}% par rapport a hier, +{pourcentage_mois}% par rapport au mois dernier"

    tk.Label(sales_report_frame, text=comparaison_text, font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=3, column=0, sticky="w", pady=4)
    
def get_rentabilite_par_produit():
    """
    Calcule la rentabilité par produit à partir de la table 'stocks'.
    Retourne un dictionnaire avec le nom du produit et sa rentabilité.
    """
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)  # Remplace par ton chemin de base de données
    cursor = conn.cursor()
    
    query = "SELECT nom, prix, PrixAchatUnite FROM stocks"
    cursor.execute(query)
    
    produits = cursor.fetchall()
    conn.close()
    
    rentabilite_par_produit = {}
    for produit in produits:
        nom, prix_vente, prix_achat = produit
        if prix_vente is not None and prix_achat is not None:
            rentabilite = prix_vente - prix_achat
            rentabilite_par_produit[nom] = rentabilite
    
    return rentabilite_par_produit

def get_reapprovisionnement_requis():
    # Connexion à la base de données
    db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')
    conn = sqlite3.connect(db_path)  # Remplace par ton chemin de base de données
    cursor = conn.cursor()

    # Sélectionner les produits avec leurs quantités
    cursor.execute("SELECT nom, quantite FROM stocks")
    stocks = cursor.fetchall()

    # Sélectionner le seuil de réapprovisionnement
    cursor.execute("SELECT reorder_point FROM reorder_threshold")
    reorder_point = cursor.fetchone()[0]  # Il n'y a qu'une seule valeur dans reorder_threshold

    # Trouver les produits nécessitant un réapprovisionnement
    reapprovisionnement = {}
    for produit, quantite in stocks:
        if quantite <= reorder_point:
            reapprovisionnement[produit] = reorder_point - quantite

    # Fermer la connexion
    conn.close()

    return reapprovisionnement

def update_stocks_report_frame(stock_report_frame):
    
    for widget in stock_report_frame.winfo_children():
       widget.destroy()
    rentabilite_par_produits = get_rentabilite_par_produit()
    # Formatage des résultats pour l'affichage
    texte_rentabilite = "Rentabilité par produit :"
    ligne_actuelle = texte_rentabilite
    for produit, rentabilite in rentabilite_par_produits.items():
        produit_info = f" {produit} ({rentabilite} FCFA),"
        if len(ligne_actuelle) + len(produit_info) > 60:  # Limite pour aller à la ligne
           tk.Label(stock_report_frame, text=ligne_actuelle.rstrip(','), font=("Helvetica", 12), bg="#ffffff", fg="#333").pack(anchor="w", pady=4)
           ligne_actuelle = produit_info
        else:
           ligne_actuelle += produit_info
    
    # Ajouter la dernière ligne si elle existe
    if ligne_actuelle.strip():
     tk.Label(stock_report_frame, text=ligne_actuelle.rstrip(','), font=("Helvetica", 12), bg="#ffffff", fg="#333").pack(anchor="w", pady=4) 
    
    # Récupérer les produits nécessitant un réapprovisionnement
    reapprovisionnement_requis = get_reapprovisionnement_requis()
    
    # Formatage du texte pour réapprovisionnement
    texte_reapprovisionnement = "Réapprovisionnement requis : "
    for produit, quantite_requise in reapprovisionnement_requis.items():
        texte_reapprovisionnement += f"{produit} ({quantite_requise} unités), "

    # Retirer la dernière virgule et l'espace
    texte_reapprovisionnement = texte_reapprovisionnement.rstrip(", ")

    # Affichage du texte dans le label
    tk.Label(stock_report_frame, text=texte_reapprovisionnement, font=("Helvetica", 12), bg="#ffffff", fg="#D32F2F").pack(anchor="w",pady=4)


def change_theme(main_window, theme="Clair"):
    """
    Change le thème de l'application entre clair et sombre.
    """
    if theme == "Sombre":
        bg_color = "#2E2E2E"  # Couleur de fond sombre
        fg_color = "#FFFFFF"  # Couleur du texte claire
        button_bg = "#555555"  # Couleur des boutons sombres
        button_fg = "#FFFFFF"  # Texte des boutons clairs
    else:
        bg_color = "#FFFFFF"  # Couleur de fond claire
        fg_color = "#000000"  # Couleur du texte sombre
        button_bg = "#DDDDDD"  # Couleur des boutons clairs
        button_fg = "#000000"  # Texte des boutons sombres

    # Appliquer les couleurs à la fenêtre principale
    main_window.config(bg=bg_color)

    # Appliquer les couleurs aux widgets (labels, boutons, etc.)
    for widget in main_window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Button):
            widget.config(bg=button_bg, fg=button_fg)
        elif isinstance(widget, tk.Frame):
            widget.config(bg=bg_color)