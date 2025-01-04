import tkinter as tk
from tkinter import messagebox
import os


# Fonction pour afficher la fenêtre d'inscription
def afficher_inscription(frame_login, frame_signup):
    frame_login.pack_forget()
    frame_signup.pack(pady=20)

# Fonction pour afficher la fenêtre de connexion
def afficher_connexion(frame_login, frame_signup):
    frame_signup.pack_forget()
    frame_login.pack(pady=20)

# Fonction pour démarrer l'application principale après une connexion réussie
def start_main_app(root):
    root.destroy()  # Utiliser destroy pour fermer la fenêtre Tkinter proprement
    os.system('python main.py')  # Lance l'application principale (main.py)

# Fonction pour afficher la fenêtre de connexion
def show_authentication_window():
    root = tk.Tk()
    root.title("Formulaire d'inscription - Gestion des Stocks et Ventes")
    root.geometry("1000x780")
    root.config(bg="#e6f7ff")  # Couleur de fond de la fenêtre principale

    # Fenêtre de connexion
    frame_login = tk.Frame(root, bg="#e6f7ff")
    label_username_login = tk.Label(frame_login, text="Nom d'utilisateur", bg="#e6f7ff", font=("Arial", 12))
    label_username_login.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_username_login = tk.Entry(frame_login, font=("Arial", 12), bd=2, relief="solid", width=35)
    entry_username_login.grid(row=0, column=1, padx=10, pady=10)

    label_password_login = tk.Label(frame_login, text="Mot de passe", bg="#e6f7ff", font=("Arial", 12))
    label_password_login.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_password_login = tk.Entry(frame_login, font=("Arial", 12), bd=2, relief="solid", show="*", width=35)
    entry_password_login.grid(row=1, column=1, padx=10, pady=10)

    # Bouton de connexion
    button_login = tk.Button(frame_login, text="Se connecter", font=("Arial", 12), command=lambda: start_main_app(root), bg="#4CAF50", fg="white", relief="flat", width=25)
    button_login.grid(row=2, columnspan=2, pady=10)

    # Lien vers l'inscription
    button_signup_link = tk.Button(frame_login, text="Créer un compte", font=("Arial", 10), command=lambda: afficher_inscription(frame_login, frame_signup), bg="#3498db", fg="white", relief="flat")
    button_signup_link.grid(row=3, columnspan=2, pady=5)

    # Fenêtre d'inscription
    frame_signup = tk.Frame(root, bg="#e6f7ff")

    label_username_signup = tk.Label(frame_signup, text="Nom d'utilisateur", bg="#e6f7ff", font=("Arial", 12))
    label_username_signup.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_username_signup = tk.Entry(frame_signup, font=("Arial", 12), bd=2, relief="solid", width=35)
    entry_username_signup.grid(row=0, column=1, padx=10, pady=10)

    label_password_signup = tk.Label(frame_signup, text="Mot de passe", bg="#e6f7ff", font=("Arial", 12))
    label_password_signup.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_password_signup = tk.Entry(frame_signup, font=("Arial", 12), bd=2, relief="solid", show="*", width=35)
    entry_password_signup.grid(row=1, column=1, padx=10, pady=10)

    label_email_signup = tk.Label(frame_signup, text="Adresse e-mail", bg="#e6f7ff", font=("Arial", 12))
    label_email_signup.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_email_signup = tk.Entry(frame_signup, font=("Arial", 12), bd=2, relief="solid", width=35)
    entry_email_signup.grid(row=2, column=1, padx=10, pady=10)

    label_phone_signup = tk.Label(frame_signup, text="Numéro de téléphone", bg="#e6f7ff", font=("Arial", 12))
    label_phone_signup.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_phone_signup = tk.Entry(frame_signup, font=("Arial", 12), bd=2, relief="solid", width=35)
    entry_phone_signup.grid(row=3, column=1, padx=10, pady=10)

    label_company_signup = tk.Label(frame_signup, text="Nom de l'entreprise", bg="#e6f7ff", font=("Arial", 12))
    label_company_signup.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_company_signup = tk.Entry(frame_signup, font=("Arial", 12), bd=2, relief="solid", width=35)
    entry_company_signup.grid(row=4, column=1, padx=10, pady=10)

    label_address_signup = tk.Label(frame_signup, text="Adresse de l'entreprise", bg="#e6f7ff", font=("Arial", 12))
    label_address_signup.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_address_signup = tk.Entry(frame_signup, font=("Arial", 12), bd=2, relief="solid", width=35)
    entry_address_signup.grid(row=5, column=1, padx=10, pady=10)

    # Bouton d'inscription
    button_signup = tk.Button(frame_signup, text="S'inscrire", font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat", width=25)
    button_signup.grid(row=6, columnspan=2, pady=20)

    # Lien vers la connexion
    button_login_link = tk.Button(frame_signup, text="Déjà un compte ? Se connecter", font=("Arial", 10), command=lambda: afficher_connexion(frame_login, frame_signup), bg="#3498db", fg="white", relief="flat")
    button_login_link.grid(row=7, columnspan=2, pady=10)

    # Affichage de la fenêtre de connexion par défaut
    afficher_connexion(frame_login, frame_signup)

    # Lancer la boucle Tkinter
    root.mainloop()
