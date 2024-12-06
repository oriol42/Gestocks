from tkinter import Toplevel, Label, Entry, Button, messagebox
import sqlite3
import os


class ManageProduct:
    def __init__(self, app):
        self.app = app

    def AddProduct(self):
        # Fenêtre d'ajout de produit
        addWindow = Toplevel(self.app.root)
        addWindow.title("Ajouter un produit")
        addWindow.geometry("400x300")

        # Entrée pour le nom du produit
        Label(addWindow, text="Nom du produit :").pack(pady=5)
        nameEntry = Entry(addWindow)
        nameEntry.pack(pady=5)

        # Entrée pour la quantité
        Label(addWindow, text="Quantité en stock :").pack(pady=5)
        quantityEntry = Entry(addWindow)
        quantityEntry.pack(pady=5)

        # Entrée pour le prix
        Label(addWindow, text="Prix du produit :").pack(pady=5)
        priceEntry = Entry(addWindow)
        priceEntry.pack(pady=5)

        # Entrée pour la description
        Label(addWindow, text="Description du produit :").pack(pady=5)
        descriptionEntry = Entry(addWindow)
        descriptionEntry.pack(pady=5)

        # Bouton pour enregistrer
        saveButton = Button(
            addWindow,
            text="Enregistrer",
            command=lambda: self.SaveProduct(addWindow, nameEntry, quantityEntry, priceEntry, descriptionEntry)
        )
        saveButton.pack(pady=10)

    def SaveProduct(self, addWindow, nameEntry, quantityEntry, priceEntry, descriptionEntry):
        # Récupération des données
        name = nameEntry.get().strip()
        quantity = quantityEntry.get().strip()
        price = priceEntry.get().strip()
        description = descriptionEntry.get().strip()

        # Validation des champs obligatoires
        if not name or not quantity or not price:
            messagebox.showwarning("Champs manquants", "Les champs Nom, Quantité et Prix sont obligatoires.")
            return

        # Conversion des champs numériques
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Erreur de saisie", "Quantité et Prix doivent être des valeurs numériques.")
            return

        try:
            # Chemin vers la base de données
            dbPath = os.path.join(os.path.dirname(__file__), 'database', 'GESTOCK.db')

            # Connexion à la base de données
            con = sqlite3.connect(dbPath)
            cursor = con.cursor()

            # Création de la table si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    description TEXT
                )
            """)
            con.commit()

            # Insertion des données dans la table
            cursor.execute("""
                INSERT INTO Stocks (name, quantity, price, description)
                VALUES (?, ?, ?, ?)
            """, (name, quantity, price, description))
            con.commit()

            self.app.stocks.populate_stock_table()
            # Message de succès et fermeture de la fenêtre
            messagebox.showinfo("Succès", "Produit ajouté avec succès.")
            addWindow.destroy()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        finally:
            if 'con' in locals():
                con.close()
                
    def updateProduct(self):
        
      # Vérifier si un produit est sélectionné dans le Treeview
      selected_item = self.app.stocks.table.selection()
      
      if not selected_item:
          messagebox.showwarning("Aucun produit sélectionné", "Veuillez sélectionner un produit à modifier.")
          return
      
      item = self.app.stocks.table.item(selected_item[0])
      product_data = item['values']#[id,name,quantity,price,descriptin]

      # Récupérer les données du produit sélectionné
      product_id = product_data[0]  # L'identifiant (iid) correspond à l'ID dans la base de données


      # Ouvrir une fenêtre pour modifier le produit
      editWindow = Toplevel(self.app.root)
      editWindow.title("Modifier un produit")
      editWindow.geometry("400x300")

      # Champs de saisie pour les modifications
      Label(editWindow, text="Nom du produit :").pack(pady=5)
      nameEntry = Entry(editWindow)
      nameEntry.insert(0, product_data[1])  # Pré-remplir avec le nom actuel
      nameEntry.pack(pady=5)

      Label(editWindow, text="Quantité en stock :").pack(pady=5)
      quantityEntry = Entry(editWindow)
      quantityEntry.insert(0, product_data[2])
      quantityEntry.pack(pady=5)

      Label(editWindow, text="Prix du produit :").pack(pady=5)
      priceEntry = Entry(editWindow)
      priceEntry.insert(0, product_data[3])
      priceEntry.pack(pady=5)

      Label(editWindow, text="Description du produit :").pack(pady=5)
      descriptionEntry = Entry(editWindow)
      descriptionEntry.insert(0, product_data[4])
      descriptionEntry.pack(pady=5)
      
      #Bouton pour sauvegarder les modifications
      
      saveButton = Button(
            editWindow,
            text="Modifier",
            command=lambda: SaveChanges()
        )
      saveButton.pack(pady=10)
      
      # Fonction pour enregistrer les modifications
      def SaveChanges():
        new_name = nameEntry.get().strip()
        new_quantity = quantityEntry.get().strip()
        new_price = priceEntry.get().strip()
        new_description = descriptionEntry.get().strip()

        if not new_name or not new_quantity or not new_price:
            messagebox.showwarning("Champs manquants", "Les champs Nom, Quantité et Prix sont obligatoires.")
            return

        try:
            # Conversion des valeurs numériques
            new_quantity = int(new_quantity)
            new_price = float(new_price)
        except ValueError:
             messagebox.showerror("Erreur de saisie", "Le prix et la quantité doivent etres des noombres valides")
             
             return

        try :
            # Connexion à la base de données
            dbPath = os.path.join(os.path.dirname(__file__), 'database', 'GESTOCK.db')
            conn = sqlite3.connect(dbPath)
            cursor = conn.cursor()

            # Mise à jour des données dans la base de données
            cursor.execute("""
                UPDATE Stocks
                SET name = ?, quantity = ?, Price = ?, description = ?
                WHERE id = ?
            """, (new_name, new_quantity, new_price, new_description, product_id))
            conn.commit()
            
            if cursor.rowcount == 0:
                messagebox.showerror("Erreur", "Le produit n'a pas été trouvé dans la base de données.")
                return

            # Mise à jour du Treeview
            
            self.app.stocks.populate_stock_table() 
            
            # Message de succès
            
            messagebox.showinfo("Succès","Produit modifié avec succès.")
            editWindow.destroy()
            
        except Exception as e:
            messagebox.showerror("Erreur",f"Une erreur est survenue : {e}") 
        finally:
            if 'conn' in locals():
                conn.close()




      
      
