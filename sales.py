import tkinter as tk 
from tkinter import ttk, messagebox


class Sales:
    def __init__(self, app):
        self.app = app
        

    def show_sales(self):
        self.app.clear_main_frame()
        self.app.content_label.config(text="Effectuer une vente")
        self.show_sales_input_form()

    def show_sales_input_form(self):
        form_frame = tk.Frame(self.app.main_frame)
        tk.Label(form_frame, text="Produit").grid(row=0, column=0, padx=10, pady=10)

        #  remplir les produits depuis la base de données ici
        self.product_dropdown = ttk.Combobox(form_frame, values=self.get_products_from_db()) 
        self.product_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Quantité").grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        self.sell_button = tk.Button(form_frame, text="Vendre", command=self.sell_product, font=("Arial", 12), bg="#2ecc71", fg="white")
        self.sell_button.grid(row=2, columnspan=2, pady=20)
        form_frame.pack(fill=tk.X)

    def sell_product(self):
        product_name = self.product_dropdown.get()
        quantity = self.quantity_entry.get().strip()
        
        # Interaction avec la base de données pour vendre un produit et mettre à jour la quantité
        pass

    def get_products_from_db(self):
        #  interagir avec la base de données pour récupérer la liste des produits
        pass
