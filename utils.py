import tkinter as tk
from tkinter import ttk, messagebox
import os
import sqlite3
from datetime import datetime
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
def add_product(stock_treeview, conn,products_treeview):
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

    tk.Label(add_window, text="Prix :", font=("arial", 9)).grid(row=2, column=0, sticky="w", padx=12, pady=12)
    entry_prix = tk.Entry(add_window, font=("arial", 9))
    entry_prix.grid(row=2, column=1, padx=12, pady=12)

    tk.Label(add_window, text="Fournisseur :", font=("arial", 9)).grid(row=3, column=0, sticky="w", padx=12, pady=12)
    entry_fournisseur = tk.Entry(add_window, font=("arial", 9))
    entry_fournisseur.grid(row=3, column=1, padx=12, pady=12)

    tk.Label(add_window, text="Catégorie :", font=("arial", 9)).grid(row=4, column=0, sticky="w", padx=12, pady=12)
    categories = ["Électronique", "Vêtements", "Meubles", "Accessoires", "Autre"]
    category_combobox = ttk.Combobox(add_window, values=categories, font=("arial", 9))
    category_combobox.set("Électronique")
    category_combobox.grid(row=4, column=1, padx=12, pady=12)
    
    tk.Label(add_window, text="Prix d'achat de l'unité :", font=("arial", 9)).grid(row=5, column=0, sticky="w", padx=12, pady=12)
    entry_PrixAchatUnite = tk.Entry(add_window, font=("arial", 9))
    entry_PrixAchatUnite.grid(row=5, column=1, padx=12, pady=12)

    tk.Button(add_window, text="Ajouter", font=("arial", 9), bg="#4CAF50", fg="white", command=submit_product).grid(row=6, column=1, sticky="w", padx=12, pady=12)
    
def delete_product(stock_treeview, conn,products_treeview):
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
    else:
        messagebox.showinfo("Annulé", "Suppression annulée.")
      
        
    
# Fonction pour modifier un produit
def modify_product(stock_treeview, conn,products_treeview):
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

    tk.Label(modify_window, text="Prix :", font=("arial", 9)).grid(row=2, column=0, sticky="w", padx=12, pady=12)
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
    cursor.execute("SELECT nom, quantite, prix FROM stocks")
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

def generate_simple_invoice(cart_treeview, conn, sales_history_treeview):
    if not cart_treeview.get_children():
        messagebox.showwarning("Panier vide", "Aucun produit dans le panier. Veuillez ajouter des produits avant de générer la facture.")
        return

    # Générer un nom unique pour la facture
    invoice_name = f"Facture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    invoice_path = os.path.abspath(invoice_name)  # Chemin absolu pour enregistrer la facture

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
        cursor.execute("SELECT quantite FROM stocks WHERE nom = ?", (product_name,))
        result = cursor.fetchone()
        if result:
            current_stock = result[0]
            if current_stock >= quantity_sold:
                new_stock = current_stock - quantity_sold
                cursor.execute("UPDATE stocks SET quantite = ? WHERE nom = ?", (new_stock, product_name))
                
                # Vérifier si une vente existe déjà pour ce produit et cette date
                cursor.execute("SELECT id, quantity FROM sales_history WHERE product_name = ? AND date = ?", 
                               (product_name, datetime.now().strftime('%Y-%m-%d')))
                existing_sale = cursor.fetchone()

                if existing_sale:
                    # Si une vente existe, mettre à jour la quantité et le total
                    new_quantity = existing_sale[1] + quantity_sold
                    new_total = new_quantity * unit_price
                    cursor.execute("UPDATE sales_history SET quantity = ?, total_price = ? WHERE id = ?",
                                   (new_quantity, new_total, existing_sale[0]))
                else:
                    # Sinon, insérer une nouvelle vente
                    cursor.execute("INSERT INTO sales_history (date, product_name, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)",
                                   (datetime.now().strftime('%Y-%m-%d'), product_name, quantity_sold, unit_price, total_price))
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