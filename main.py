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
from utils import connect_database, update_table_structure, show_frame
import time


# Créer la fenêtre principale
root = tk.Tk()
root.title("Gestion de l'Application")
icon_path = os.path.join(os.path.dirname(__file__),'assets','icon.ico')
root.iconbitmap(icon_path)

# Taille de la fenêtre principale
window_width = 1024
window_height = 800
root.geometry(f"{window_width}x{window_height}")
root.resizable(True, True)  # Permettre le redimensionnement de la fenêtre

# Fonction pour afficher l'écran de chargement
def show_loading_screen():
    # Créer une frame pour l'écran de chargement qui occupe toute la fenêtre
    loading_frame = tk.Frame(root, width=window_width, height=window_height, bg="#2C3E50")  # Bleu Marine
    loading_frame.place(relwidth=1, relheight=1)  # Utilisation de relwidth et relheight pour occuper toute la fenêtre

    # Animation pour le texte "Gestocks"
    label = tk.Label(loading_frame, text="Gestocks", font=("Arial", 60, "bold"), fg="#ECF0F1", bg="#2C3E50")
    label.pack(pady=100)
    
    # Liste de couleurs professionnelles à utiliser
    colors = ["#ECF0F1", "#F39C12", "#27AE60", "#2980B9", "#8E44AD", "#E74C3C"] 
    # Animation du texte : G -> Ge -> Gest -> Gesto -> Gestoc -> Gestocks
    def animate_label():
        text = "Gestocks"
        index = 1  # Commencer à afficher la lettre "G"
        
        def update_text():
            nonlocal index
            label.config(text=text[:index], fg=colors[index % len(colors)])  # Change la couleur à chaque lettre
            index += 1
            if index <= len(text):
                label.after(300, update_text)  # Ajouter une lettre toutes les 300ms

        update_text()

    animate_label()  # Lancer l'animation du texte "Gestocks"
    
    # Ajouter les étapes de chargement en bas
    steps_label = tk.Label(loading_frame, text="Chargement...", font=("Arial", 16), fg="#ECF0F1", bg="#2C3E50")
    steps_label.pack(side="bottom", pady=30)

    # Animation des étapes de chargement
    steps = ["Chargement de l'application...", "Connexion à la base de données...", "Initialisation des modules..."]
    current_step = 0

    def update_loading_step():
        nonlocal current_step
        # Vérifier si le loading_frame existe toujours avant d'essayer de mettre à jour l'étiquette
        if loading_frame.winfo_exists():
            if current_step < len(steps):
                steps_label.config(text=steps[current_step])
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

    canvas = tk.Canvas(loading_frame, width=200, height=200, bg="#2C3E50", bd=0, highlightthickness=0)  # Enlever le bord
    canvas.pack(side="bottom", pady=30)
    create_circular_loader(canvas, 200, 200)

    # Fonction pour fermer l'écran de chargement et démarrer l'application
    def start_main_app():
        loading_frame.destroy()  # Supprimer l'écran de chargement
        start_time = time.time()  # Début du chargement

        try:
            # Initialiser la connexion à la base de données
            conn = connect_database()
            update_table_structure(conn)

            # Dictionnaire pour gérer les différentes frames
            frames = {}

            # Création des frames
            
            dashboard_frame, dashboard_treeview, stock_alert_frame = create_dashboard_frame(root)
            
            report_frame, sales_report_frame, stock_report_frame = create_reports_frame(root)
            sales_history_frame, sale_history_treeview, totals_frame, totals_treeview = create_sales_history_frame(root,dashboard_treeview,sales_report_frame)
            sales_frame, sales_treeview = create_sales_frame(
                root, conn, sale_history_treeview, totals_treeview,
                dashboard_treeview, stock_alert_frame, sales_report_frame, stock_report_frame
            )
            products_treeview = sales_treeview

            # Menu principal
            menubar = tk.Menu(root)

            # Menu Tableau de Bord
            menu_dashboard = tk.Menu(menubar, tearoff=0)
            menu_dashboard.add_command(label="Tableau de Bord", command=lambda: show_frame("dashboard", frames))
            menubar.add_cascade(label="Tableau de Bord", menu=menu_dashboard)

            # Menu Ventes
            menu_sales = tk.Menu(menubar, tearoff=0)
            menu_sales.add_command(label="Ventes", command=lambda: show_frame("sales", frames))
            menubar.add_cascade(label="Ventes", menu=menu_sales)

            # Menu Historique des ventes
            menu_sales_history = tk.Menu(menubar, tearoff=0)
            menu_sales_history.add_command(label="Historique des Ventes", command=lambda: show_frame("sales_history", frames))
            menubar.add_cascade(label="Historique des Ventes", menu=menu_sales_history)

            # Menu Stocks
            menu_stocks = tk.Menu(menubar, tearoff=0)
            menu_stocks.add_command(label="Stocks", command=lambda: show_frame("stocks", frames))
            menubar.add_cascade(label="Stocks", menu=menu_stocks)

            # Menu Fournisseurs
            menu_suppliers = tk.Menu(menubar, tearoff=0)
            menu_suppliers.add_command(label="Fournisseurs", command=lambda: show_frame("suppliers", frames))
            menubar.add_cascade(label="Fournisseurs", menu=menu_suppliers)

            # Menu Rapports
            menu_reports = tk.Menu(menubar, tearoff=0)
            menu_reports.add_command(label="Rapports", command=lambda: show_frame("reports", frames))
            menubar.add_cascade(label="Rapports", menu=menu_reports)

            # Menu Paramètres
            menu_settings = tk.Menu(menubar, tearoff=0)
            menu_settings.add_command(label="Paramètres", command=lambda: show_frame("settings", frames))
            menubar.add_cascade(label="Paramètres", menu=menu_settings)

            # Configurer la barre de menu
            root.config(menu=menubar)

            # Création des frames
            frames["dashboard"] = dashboard_frame
            frames["sales"] = sales_frame
            frames["sales_history"] = sales_history_frame
            frames["stocks"] = create_stocks_frame(root, conn, sales_treeview, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame)
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
