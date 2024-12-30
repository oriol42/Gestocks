import tkinter as tk
from tkinter import messagebox
import utils
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import ImageGrab
from datetime import datetime


# Fonction d'affichage de la section Rapports
def create_reports_frame(main_frame):
    # Création du cadre principal pour les rapports
    reports_frame = tk.Frame(main_frame, bg="#f4f4f9", bd=5, relief="groove")
    reports_frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Titre principal
    tk.Label(reports_frame, text="Rapports de Ventes et Stocks", font=("Helvetica", 18, "bold"), bg="#4CAF50", fg="white", pady=10).pack(fill="x")
    
    # Cadre pour les rapports de ventes
    sales_report_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10,height=100000)
    sales_report_frame.pack(pady=10, fill="x")
    
    # Calculs dynamiques des informations de ventes
    chiffre_affaire = utils.get_chiffre_affaires_mensuel()  # Calcul du chiffre d'affaire mensuel
    ventes_par_produits = utils.get_ventes_par_produit()  # Calcul des ventes par produit
    ventes_totales_aujourdhui, ventes_totales_mois = utils.get_ventes_totales() #Calcul des ventes totales
    pourcentage_hier, pourcentage_mois = utils.get_comparaison_ventes()
  
    
    # Utilisation de grid pour l'alignement compact
    tk.Label(sales_report_frame, text=f"Chiffre d'Affaires Mensuel : {chiffre_affaire} FCFA", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    
    # Calculs des ventes par produit (dynamique)
    ventes_text = "Ventes par Produits : "
    max_produits_par_ligne = 3  # Nombre maximum de produits par ligne
    produit_count = 0
    
    for produit, details in ventes_par_produits.items():
        ventes_today = details['aujourd\'hui']
        ventes_month = details['mois']
        texte = f"{produit} ({ventes_today} unités aujourd'hui, {ventes_month} unités ce mois)"
        
        if produit_count == max_produits_par_ligne:
            ventes_text += "\n"  # Ajout d'un retour à la ligne
            produit_count = 0  # Réinitialiser le compteur pour la nouvelle ligne
        
        ventes_text += texte + ", "  # Ajouter les informations du produit à la chaîne
        produit_count += 1
    
    # Supprimer la dernière virgule et espace de la chaîne
    ventes_text = ventes_text.rstrip(", ")
    
    # Affichage des ventes par produit
    tk.Label(sales_report_frame, text=ventes_text, font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=1, column=0, sticky="w", pady=4)
    tk.Label(sales_report_frame, text=f"Ventes Totales : {ventes_totales_aujourdhui} unités vendues aujourd'hui, {ventes_totales_mois} unités vendues ce mois ", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=2, column=0, sticky="w", pady=4)
    
    comparaison_text = f"Comparaison des ventes : +{pourcentage_hier}% par rapport a hier, +{pourcentage_mois}% par rapport au mois dernier"

    tk.Label(sales_report_frame, text=comparaison_text, font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=3, column=0, sticky="w", pady=4)
    
    # Cadre pour les rapports de stocks
    stock_report_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    stock_report_frame.pack(pady=10, fill="x")
    # Récupération de la rentabilité par produit
    rentabilite_par_produits = utils.get_rentabilite_par_produit()
    # Formatage des résultats pour l'affichage
    texte_rentabilite = "Rentabilité par produit :"
    ligne_actuelle = texte_rentabilite
    for produit, rentabilite in rentabilite_par_produits.items():
        produit_info = f" {produit} ({rentabilite} FCFA),"
        if len(ligne_actuelle) + len(produit_info) > 60:  # Limite pour aller à la ligne
           tk.Label(stock_report_frame, text=ligne_actuelle.rstrip(','), font=("Helvetica", 12), bg="#ffffff", fg="#333").pack(anchor="w", pady=4)
           ligne_actuelle = produit_info
        else:
           ligne_actuelle += produit_info
    
    # Ajouter la dernière ligne si elle existe
    if ligne_actuelle.strip():
     tk.Label(stock_report_frame, text=ligne_actuelle.rstrip(','), font=("Helvetica", 12), bg="#ffffff", fg="#333").pack(anchor="w", pady=4) 
    
    # Récupérer les produits nécessitant un réapprovisionnement
    reapprovisionnement_requis = utils.get_reapprovisionnement_requis()
    
    # Formatage du texte pour réapprovisionnement
    texte_reapprovisionnement = "Réapprovisionnement requis : "
    for produit, quantite_requise in reapprovisionnement_requis.items():
        texte_reapprovisionnement += f"{produit} ({quantite_requise} unités), "

    # Retirer la dernière virgule et l'espace
    texte_reapprovisionnement = texte_reapprovisionnement.rstrip(", ")

    # Affichage du texte dans le label
    tk.Label(stock_report_frame, text=texte_reapprovisionnement, font=("Helvetica", 12), bg="#ffffff", fg="#D32F2F").pack(anchor="w",pady=4)
    


    # Cadre pour les dépenses liées au stock
    expense_frame = tk.Frame(reports_frame, bg="#ffffff", bd=3, relief="solid", padx=10, pady=10)
    expense_frame.pack(pady=10, fill="x")
    
    # Calcul dynamique des dépenses liées au stock
    tk.Label(expense_frame, text=f"Dépenses liées au Stock : ", font=("Helvetica", 12), bg="#ffffff", fg="#333").grid(row=0, column=0, sticky="w", pady=4)
    
    # Bouton pour exporter le rapport
    export_button = tk.Button(reports_frame, text="Exporter Rapport", font=("Helvetica", 12), bg="#FF9800", fg="white", relief="raised", command=lambda: export_report(reports_frame))
    export_button.pack(pady=15, ipadx=10, ipady=5)

    return reports_frame,sales_report_frame,stock_report_frame



# Fonction pour créer un dossier 'rapports' dans 'Documents'
def create_reports_folder():
    """
    Crée un dossier 'GESTOCK' dans 'Documents' et un sous-dossier 'rapports' pour stocker les rapports.
    """
    documents_path = os.path.expanduser("~/Documents")
    gestock_folder = os.path.join(documents_path, "GESTOCK")

    if not os.path.exists(gestock_folder):
        os.makedirs(gestock_folder)

    rapports_folder = os.path.join(gestock_folder, "rapports")
    if not os.path.exists(rapports_folder):
        os.makedirs(rapports_folder)

    return rapports_folder

def export_report(reports_frame):
    """
    Exporte l'interface Tkinter dans un fichier PDF en capturant la fenêtre et en l'ajoutant au PDF.
    """
    # Créer le dossier 'rapports' si nécessaire
    rapports_folder = create_reports_folder()

    # Générer un nom de fichier unique basé sur la date et l'heure actuelles
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = os.path.join(rapports_folder, f"rapport_{current_time}.pdf")

    try:
        # Obtenir les coordonnées et la taille de la fenêtre Tkinter sans inclure la barre des tâches
        window = reports_frame.winfo_toplevel()
        x = window.winfo_rootx()
        y = window.winfo_rooty()
        width = window.winfo_width()
        height = window.winfo_height()

        # Capture de l'écran dans la zone de la fenêtre Tkinter
        img = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Sauvegarder l'image temporairement (si nécessaire pour la conversion en PDF)
        temp_image_path = os.path.join(rapports_folder, "temp_image.png")
        img.save(temp_image_path)

        # Créer un PDF avec le contenu de l'image
        c = canvas.Canvas(pdf_filename, pagesize=(width, height))

        # Ajouter l'image capturée dans le PDF
        c.drawImage(temp_image_path, 0, 0, width=width, height=height)

        # Sauvegarder le PDF
        c.save()

        # Supprimer l'image temporaire après l'ajout au PDF
        os.remove(temp_image_path)

        # Affichage d'un message de confirmation
        messagebox.showinfo("Succès", f"Le rapport a été exporté avec succès vers :\n{pdf_filename}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'exportation du rapport :\n{str(e)}")