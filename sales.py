import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

class Sales:
    def __init__(self, app):
        self.app = app
        self.cart = []  # Panier vide
        self.products = ["Produit 1", "Produit 2", "Produit 3", "Produit 4"]  # Exemple de produits

    def show_sales(self):
        """Affiche la page de vente avec un design moderne utilisant CustomTkinter."""
        self.app.clear_main_frame()
        self.app.content_label.configure(text="Créer une vente", font=("Helvetica", 18, "bold"), text_color="#34495e")
        self.show_sales_input_form()

    def show_sales_input_form(self):
        """Affiche le formulaire d'entrée pour une vente avec des éléments stylisés et spacieux."""
        form_frame = ctk.CTkFrame(self.app.main_frame, fg_color="#f0f3f5", corner_radius=15, border_width=2, border_color="#BDC3C7")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Champ Produit
        ctk.CTkLabel(form_frame, text="Produit", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", padx=15, pady=10)
        self.product_dropdown = ctk.CTkComboBox(form_frame, values=self.products, font=("Helvetica", 12), state="normal")
        self.product_dropdown.grid(row=1, column=1, padx=15, pady=10, ipadx=10, ipady=5)

        # Champ Quantité
        ctk.CTkLabel(form_frame, text="Quantité", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", padx=15, pady=10)
        self.quantity_entry = ctk.CTkEntry(form_frame, font=("Helvetica", 12), justify="center", corner_radius=8, border_width=2, border_color="#BDC3C7")
        self.quantity_entry.grid(row=2, column=1, padx=15, pady=10, ipadx=10, ipady=5)

        # Bouton Ajouter au panier
        self.add_to_cart_button = ctk.CTkButton(form_frame, text="Ajouter au panier", command=self.add_to_cart, font=("Helvetica", 12, "bold"),
                                                 fg_color="#3498db", hover_color="#2980b9", corner_radius=10)
        self.add_to_cart_button.grid(row=3, column=0, pady=20, sticky="ew")  # Laisse de l'espace à droite pour le bouton suivant

        # Bouton Rafraîchir le panier (à droite du bouton "Ajouter au panier")
        self.refresh_cart_button = ctk.CTkButton(form_frame, text="Rafraîchir le panier", command=self.refresh_cart, font=("Helvetica", 12, "bold"),
                                                 fg_color="#f39c12", hover_color="#e67e22", corner_radius=10)
        self.refresh_cart_button.grid(row=3, column=1, padx=10, pady=20, sticky="ew")  # À droite du bouton "Ajouter au panier"

        # Zone de texte pour afficher les produits du panier
        self.cart_display = ctk.CTkTextbox(form_frame, width=400, height=150, font=("Helvetica", 12), state="disabled")
        self.cart_display.grid(row=4, columnspan=2, padx=15, pady=10)

        # Total de la vente
        self.total_label = ctk.CTkLabel(form_frame, text="Total: 0.00 FCFA", font=("Helvetica", 14, "bold"), text_color="#e74c3c")
        self.total_label.grid(row=5, columnspan=2, pady=10)

        # Bouton de facturation
        self.generate_invoice_button = ctk.CTkButton(form_frame, text="Générer Facture", command=self.generate_invoice, font=("Helvetica", 12, "bold"),
                                                     fg_color="#2ecc71", hover_color="#27ae60", corner_radius=10)
        self.generate_invoice_button.grid(row=6, columnspan=2, pady=20)

    def add_to_cart(self):
        """Ajoute un produit au panier et met à jour l'affichage."""
        product_name = self.product_dropdown.get()
        quantity = self.quantity_entry.get().strip()

        if not product_name or not quantity:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un nombre entier positif.")
            return

        # Recherche du produit et de son prix
        product_price = 5000  # Prix par défaut en FCFA, à remplacer par votre logique
        total_price = product_price * quantity

        # Ajout au panier
        self.cart.append((product_name, quantity, product_price, total_price))

        # Mise à jour de l'affichage du panier
        cart_content = "\n".join([f"{item[0]} - {item[1]} x {item[2]:.2f} FCFA = {item[3]:.2f} FCFA" for item in self.cart])
        self.cart_display.configure(state="normal")
        self.cart_display.delete(1.0, tk.END)  # Effacer le contenu précédent
        self.cart_display.insert(tk.END, cart_content)
        self.cart_display.configure(state="disabled")

        # Mise à jour du total de la vente
        total_amount = sum(item[3] for item in self.cart)
        self.total_label.configure(text=f"Total: {total_amount:.2f} FCFA")

        # Réinitialisation du champ quantité
        self.quantity_entry.delete(0, tk.END)

    def generate_invoice(self):
        """Génère une facture basée sur le panier actuel et l'affiche."""
        if not self.cart:
            messagebox.showwarning("Panier vide", "Ajoutez des produits au panier avant de générer une facture.")
            return

        # Récapitulatif de la facture
        invoice = "Facture de vente\n\n"
        invoice += "Produit\tQuantité\tPrix\tTotal\n"
        invoice += "-" * 50 + "\n"
        
        # Ajouter chaque ligne de produit au panier dans la facture
        for item in self.cart:
            invoice += f"{item[0]}\t{item[1]}\t{item[2]:.2f} FCFA\t{item[3]:.2f} FCFA\n"
        
        # Total de la facture
        total_amount = sum(item[3] for item in self.cart)
        invoice += "-" * 50 + "\n"
        invoice += f"Total: {total_amount:.2f} FCFA"

        # Affichage de la facture dans une fenêtre popup
        messagebox.showinfo("Facture", invoice)

        # Réinitialiser le panier après génération de la facture
        self.cart.clear()
        self.cart_display.configure(state="normal")
        self.cart_display.delete(1.0, tk.END)  # Effacer le contenu du panier
        self.cart_display.configure(state="disabled")
        self.total_label.configure(text="Total: 0.00 FCFA")

    def refresh_cart(self):
        """Réinitialise l'affichage du panier et réinitialise le total."""
        self.cart.clear()  # Vider le panier
        self.cart_display.configure(state="normal")
        self.cart_display.delete(1.0, tk.END)  # Effacer tout le contenu du panier affiché
        self.cart_display.configure(state="disabled")
        self.total_label.configure(text="Total: 0.00 FCFA")  # Réinitialiser le total
