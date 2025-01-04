import os
import tkinter as tk
from tkinter import messagebox
from dashboard import create_dashboard_frame
from sales import create_sales_frame
from sales_history import create_sales_history_frame
from stocks import create_stocks_frame
from supplier import create_suppliers_frame
from reports import create_reports_frame
from settings import create_settings_frame
from utils import connect_database, update_table_structure, show_frame
from auth import show_authentication_window
from loading_screen import show_loading_screen 


# Lancer la fenêtre d'authentification
show_authentication_window()

# Créer la fenêtre principale mais la cacher
root = tk.Tk()
root.title("Gestion de l'Application")

# Taille de la fenêtre principale 
window_width = 1024
window_height = 800

root.geometry(f"{window_width}x{window_height}")
root.resizable(True, True)  # permettre le redimensionnement de la fenêtre

# Cacher la fenêtre principale pour ne pas qu'elle s'affiche pendant le chargement
root.withdraw()

# Créer la fenêtre de chargement
loading_window = show_loading_screen()

# Fonction pour fermer la fenêtre de chargement et lancer l'application principale
def start_main_app():
    loading_window.destroy()  # Fermer la fenêtre de chargement

    root.deiconify()  # Afficher la fenêtre principale (enlever le hide)

    # Initialiser la connexion à la base de données
    conn = connect_database()
    update_table_structure(conn)

    # Dictionnaire pour gérer les différentes frames
    frames = {}

    # Création de la frame des ventes pour récupérer le sales_treeview
    sales_history_frame, sale_history_treeview, totals_frame, totals_treeview = create_sales_history_frame(root)
    dashboard_frame, dashboard_treeview, stock_alert_frame = create_dashboard_frame(root)
    report_frame, sales_report_frame, stock_report_frame = create_reports_frame(root)
    sales_frame, sales_treeview = create_sales_frame(root, conn, sale_history_treeview, totals_treeview, dashboard_treeview, stock_alert_frame, sales_report_frame, stock_report_frame)
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

    # Création des frames, y compris celle des stocks avec sales_treeview
    frames["dashboard"] = dashboard_frame
    frames["sales"] = sales_frame
    frames["sales_history"] = sales_history_frame
    frames["stocks"] = create_stocks_frame(root, conn, sales_treeview, products_treeview, dashboard_treeview, stock_alert_frame, stock_report_frame)  # Passer directement sales_treeview
    frames["suppliers"] = create_suppliers_frame(root, conn)
    frames["reports"] = report_frame
    frames["settings"] = create_settings_frame(root, stock_alert_frame, stock_report_frame)

    # Affichage du tableau de bord par défaut
    show_frame("dashboard", frames)

    # Lancer l'application
    root.mainloop()

# Lancer le loader pendant 5 secondes, puis appeler la fonction de démarrage de l'application
loading_window.after(5000, start_main_app)  # Après 5000 ms (5 secondes), démarrer l'application principale

# Lancer la fenêtre de chargement
loading_window.mainloop()
