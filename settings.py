import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import utils
import reports


def show_stock_settings(content_frame,stock_alert_frame,stock_report_frame):
    # Effacer les widgets existants dans le content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Titre et champ de seuil de réapprovisionnement
    tk.Label(content_frame, text="Paramètres de Gestion des Stocks", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)
    tk.Label(content_frame, text="Seuil de réapprovisionnement", font=("Helvetica", 12), bg="#f7f7f7", fg="#444").pack(pady=5)
    stock_threshold_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
    stock_threshold_entry.pack(pady=5)
    
    # Fonction pour enregistrer le seuil dans la table reorder_threshold
    def save_stock_settings():
        threshold = stock_threshold_entry.get()
        if not threshold.isdigit():
            messagebox.showwarning("Entrée invalide", "Veuillez entrer un seuil de réapprovisionnement valide.")
        else:
            # Connexion à la base de données
            db_path = os.path.join(os.path.dirname(__file__),'DataBase','GESTOCK.db')  # Modifie le chemin selon ton environnement
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Supprimer l'ancien seuil
            cursor.execute("DELETE FROM reorder_threshold")
            
            # Insertion du nouveau seuil dans la table reorder_threshold
            cursor.execute("INSERT INTO reorder_threshold (reorder_point) VALUES (?)", (threshold,))
            conn.commit()
            
            # Fermer la connexion
            conn.close()
            
            # Message de confirmation
            messagebox.showinfo("Paramètres enregistrés", f"Seuil enregistré : {threshold}")
            utils.load_low_stock_alerts(stock_alert_frame)
            utils.update_stocks_report_frame(stock_report_frame)
    
    # Bouton Enregistrer
    tk.Button(content_frame, text="Enregistrer", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=save_stock_settings).pack(pady=10)


def show_user_settings(content_frame):
    # Effacer les widgets existants dans le content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Titre et champs de gestion des utilisateurs
    tk.Label(content_frame, text="Gestion des Utilisateurs", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)
    tk.Label(content_frame, text="Nom d'utilisateur", font=("Helvetica", 12), bg="#f7f7f7", fg="#444").pack(pady=5)
    username_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
    username_entry.pack(pady=5)
    
    # Rôle
    tk.Label(content_frame, text="Rôle", font=("Helvetica", 12), bg="#f7f7f7", fg="#444").pack(pady=5)
    role_var = tk.StringVar(value="Administrateur")
    tk.OptionMenu(content_frame, role_var, "Administrateur", "Vendeur", "Responsable des stocks").pack(pady=5)
    
    # Bouton Enregistrer
    def save_user_settings():
        username = username_entry.get()
        role = role_var.get()
        if not username:
            messagebox.showwarning("Entrée invalide", "Veuillez entrer un nom d'utilisateur.")
        else:
            messagebox.showinfo("Paramètres enregistrés", f"Utilisateur: {username} | Rôle: {role}")
    
    tk.Button(content_frame, text="Enregistrer", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=save_user_settings).pack(pady=10)

def show_update_settings(content_frame):
    # Effacer les widgets existants dans le content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Titre et champs pour la mise à jour de l'application
    tk.Label(content_frame, text="Mise à jour de l'application", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)
    tk.Label(content_frame, text="Vérifier les mises à jour automatiques", font=("Helvetica", 12), bg="#f7f7f7", fg="#444").pack(pady=5)
    
    # Bouton de vérification des mises à jour
    def check_updates():
        messagebox.showinfo("Mise à jour", "Aucune mise à jour disponible.")
    
    tk.Button(content_frame, text="Vérifier maintenant", font=("Helvetica", 12), bg="#FF5722", fg="white", command=check_updates).pack(pady=10)

# Créer la fonction de la section des paramètres
def create_settings_frame(main_frame,stock_alert_frame,stock_report_frame):
    settings_frame = tk.Frame(main_frame, bg="#f7f7f7", padx=20, pady=20)
    settings_frame.pack(expand=True, fill="both", padx=30, pady=30)  # Centrage de la frame principale

    # Titre principal
    tk.Label(settings_frame, text="Paramètres de l'application", font=("Helvetica", 20, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)

    # Cadre de gauche pour les boutons
    left_frame = tk.Frame(settings_frame, bg="#f7f7f7", width=200, padx=10)
    left_frame.pack(side="left", padx=20, pady=20)

    # **Boutons pour naviguer entre les sections**
    stock_management_button = tk.Button(left_frame, text="Gestion des Stocks", font=("Helvetica", 12), bg="#FF5722", fg="white", relief="raised", bd=3, padx=10, pady=5, command=lambda: show_stock_settings(content_frame,stock_alert_frame,stock_report_frame))
    stock_management_button.pack(pady=5, fill="x")

    user_management_button = tk.Button(left_frame, text="Gestion des Utilisateurs", font=("Helvetica", 12), bg="#FF5722", fg="white", relief="raised", bd=3, padx=10, pady=5, command=lambda: show_user_settings(content_frame))
    user_management_button.pack(pady=5, fill="x")

    update_settings_button = tk.Button(left_frame, text="Mise à jour de l'Application", font=("Helvetica", 12), bg="#FF5722", fg="white", relief="raised", bd=3, padx=10, pady=5, command=lambda: show_update_settings(content_frame))
    update_settings_button.pack(pady=5, fill="x")

    # Cadre pour afficher le contenu selon la section sélectionnée
    content_frame = tk.Frame(settings_frame, bg="#f7f7f7", padx=20, pady=20)
    content_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

    return settings_frame
