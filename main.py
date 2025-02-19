import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dashboard import create_dashboard_frame
from sales import create_sales_frame
from sales_history import create_sales_history_frame
from stocks import create_stocks_frame
from supplier import create_suppliers_frame
from reports import create_reports_frame
from settings import create_settings_frame
from utils import connect_database, update_table_structure, show_frame,get_db_path
import time,shutil,sqlite3
import customtkinter as ctk

# Créer la fenêtre principale
root = ctk.CTk()
root.title("Gestocks")
icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
root.iconbitmap(icon_path)

# Taille de la fenêtre principale
window_width = 1024
window_height = 800
root.geometry(f"{window_width}x{window_height}")
root.resizable(True, True)  # Permettre le redimensionnement de la fenêtre

# Couleurs améliorées
app_bg_color = "#D5DBDB"  # Gris clair pour l'application
menu_bg_color = "#34495E"  # Couleur plus sombre pour le menu
loading_bg_color = "#2C3E50"  # Couleur d'arrière-plan plus sombre pour l'écran de chargement

# Appliquer la couleur de fond à toute l'application
root.configure(fg_color=app_bg_color)

# Fonction pour afficher l'écran de chargement
def show_loading_screen():
    # Créer une frame pour l'écran de chargement qui occupe toute la fenêtre
    loading_frame = ctk.CTkFrame(root, width=window_width, height=window_height, corner_radius=0, fg_color=loading_bg_color)  # Utilisation de CTkFrame avec couleur de fond
    loading_frame.place(relwidth=1, relheight=1)  # Utilisation de relwidth et relheight pour occuper toute la fenêtre

    # Animation pour le texte "Gestocks"
    label = ctk.CTkLabel(loading_frame, text="Gestocks", font=("Arial", 60, "bold"), text_color="#ECF0F1", fg_color=loading_bg_color)
    label.pack(pady=100)
    
    # Liste de couleurs professionnelles à utiliser
    colors = ["#ECF0F1", "#F39C12", "#27AE60", "#2980B9", "#8E44AD", "#E74C3C"] 
    # Animation du texte : G -> Ge -> Gest -> Gesto -> Gestoc -> Gestocks
    def animate_label():
        text = "Gestocks"
        index = 1  # Commencer à afficher la lettre "G"
        
        def update_text():
            nonlocal index
            label.configure(text=text[:index], text_color=colors[index % len(colors)])  # Change la couleur à chaque lettre
            index += 1
            if index <= len(text):
                label.after(300, update_text)  # Ajouter une lettre toutes les 300ms

        update_text()

    animate_label()  # Lancer l'animation du texte "Gestocks"
    
    # Ajouter les étapes de chargement en bas
    steps_label = ctk.CTkLabel(loading_frame, text="Chargement...", font=("Arial", 16), text_color="#ECF0F1", fg_color=loading_bg_color)
    steps_label.pack(side="bottom", pady=30)

    # Animation des étapes de chargement
    steps = ["Chargement de l'application...", "Connexion à la base de données...", "Initialisation des modules..."]
    current_step = 0

    def update_loading_step():
        nonlocal current_step
        # Vérifier si le loading_frame existe toujours avant d'essayer de mettre à jour l'étiquette
        if loading_frame.winfo_exists():
            if current_step < len(steps):
                steps_label.configure(text=steps[current_step])  # Utilisation de configure() au lieu de config()
                current_step += 1
                root.after(2500, update_loading_step)  # Changer le message toutes les 2,5 secondes
        else:
            print("L'écran de chargement a été détruit, arrêt de la mise à jour.")

    update_loading_step()

    # Créer la barre de progression circulaire tout en bas
    def create_circular_loader(canvas, width, height):
        arc = canvas.create_arc(10, 10, width - 10, height - 10, start=0, extent=90, outline="#F39C12", width=6, style='arc')
        canvas.after(50, rotate_arc, arc, canvas)

    def rotate_arc(arc, canvas):
        # Faire tourner l'arc de manière fluide
        current_extent = float(canvas.itemcget(arc, 'extent'))
        new_extent = (current_extent + 5) % 360
        canvas.itemconfig(arc, extent=new_extent)
        canvas.after(50, rotate_arc, arc, canvas)

    canvas = ctk.CTkCanvas(loading_frame, width=200, height=200, bg=loading_bg_color, bd=0, highlightthickness=0)  # Enlever le bord
    canvas.pack(side="bottom", pady=30)
    create_circular_loader(canvas, 200, 200)

    # Fonction pour fermer l'écran de chargement et démarrer l'application
    def start_main_app():
        loading_frame.destroy()  # Supprimer l'écran de chargement
        start_time = time.time()  # Début du chargement

        try:
            # Initialiser la connexion à la base de données
            db_path = get_db_path()
            if not os.path.exists(db_path):
               original_db_path = os.path.join(os.path.dirname(__file__), "DataBase", "GESTOCK.db")
               shutil.copy2(original_db_path, db_path)
            conn = sqlite3.connect(db_path)
            update_table_structure(conn)

            # Dictionnaire pour gérer les différentes frames
            frames = {}

            # Création des frames
            dashboard_frame, dashboard_treeview, stock_alert_frame = create_dashboard_frame(root)
            report_frame, sales_report_frame, stock_report_frame,expense_frame = create_reports_frame(root)
            sales_history_frame, sale_history_treeview, totals_frame, totals_treeview = create_sales_history_frame(root, dashboard_treeview, sales_report_frame)
            sales_frame, sales_treeview = create_sales_frame(
                root, conn, sale_history_treeview, totals_treeview,
                dashboard_treeview, stock_alert_frame, sales_report_frame, stock_report_frame
            )
            products_treeview = sales_treeview

            # Menu principal (remplacé par des boutons)
            frame_menu = ctk.CTkFrame(root, fg_color=menu_bg_color, height=40)  # Utilisation de CTkFrame
            frame_menu.pack(fill="x", side="top")  # Remplir la largeur du haut de la fenêtre

            # Fonction pour afficher le bon cadre
            def change_frame(frame_name):
                show_frame(frame_name, frames)

            # Créer des boutons pour chaque section
            button_dashboard = ctk.CTkButton(frame_menu, text="Tableau de Bord", command=lambda: change_frame("dashboard"), fg_color="#2980B9", text_color="white", width=20)
            button_dashboard.pack(side="left", padx=10, pady=5)

            button_sales = ctk.CTkButton(frame_menu, text="Ventes", command=lambda: change_frame("sales"), fg_color="#2980B9", text_color="white", width=20)
            button_sales.pack(side="left", padx=10, pady=5)

            button_sales_history = ctk.CTkButton(frame_menu, text="Historique des Ventes", command=lambda: change_frame("sales_history"), fg_color="#2980B9", text_color="white", width=20)
            button_sales_history.pack(side="left", padx=10, pady=5)

            button_stocks = ctk.CTkButton(frame_menu, text="Stocks", command=lambda: change_frame("stocks"), fg_color="#2980B9", text_color="white", width=20)
            button_stocks.pack(side="left", padx=10, pady=5)

            button_suppliers = ctk.CTkButton(frame_menu, text="Fournisseurs", command=lambda: change_frame("suppliers"), fg_color="#2980B9", text_color="white", width=20)
            button_suppliers.pack(side="left", padx=10, pady=5)

            button_reports = ctk.CTkButton(frame_menu, text="Rapports", command=lambda: change_frame("reports"), fg_color="#2980B9", text_color="white", width=20)
            button_reports.pack(side="left", padx=10, pady=5)

            button_settings = ctk.CTkButton(frame_menu, text="Paramètres", command=lambda: change_frame("settings"), fg_color="#2980B9", text_color="white", width=20)
            button_settings.pack(side="left", padx=10, pady=5)

            # Création des frames
            frames["dashboard"] = dashboard_frame
            frames["sales"] = sales_frame
            frames["sales_history"] = sales_history_frame
            frames["stocks"] = create_stocks_frame(root, conn, sales_treeview, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame,expense_frame)
            frames["suppliers"] = create_suppliers_frame(root, conn)
            frames["reports"] = report_frame
            frames["settings"] = create_settings_frame(root, stock_alert_frame, stock_report_frame)

            # Affichage du tableau de bord par défaut
            show_frame("dashboard", frames)

            # Lancer l'application
            root.mainloop()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
            root.quit()

        end_time = time.time()  # Fin du chargement
        loading_time = end_time - start_time  # Temps de chargement
        print(f"Temps de chargement: {loading_time:.2f} secondes")

    # Lancer l'application après 6 secondes
    root.after(6000, start_main_app)

# Appeler la fonction pour afficher l'écran de chargement
show_loading_screen()

# Lancer l'application principale après le délai
root.mainloop()
