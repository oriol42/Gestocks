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

            # Ajouter au tableau de l'application principale
            if hasattr(self.app.stocks, "table"):
                self.app.stocks.table.insert("", "end", values=(name, quantity, price, description))

            # Message de succès et fermeture de la fenêtre
            messagebox.showinfo("Succès", "Produit ajouté avec succès.")
            addWindow.destroy()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        finally:
            if 'con' in locals():
                con.close()