import tkinter as tk
from PIL import Image, ImageTk
import os

def show_loading_screen():
    # Créer une nouvelle fenêtre de chargement
    loading_window = tk.Toplevel()
    loading_window.title("Chargement...")

    # Taille personnalisée de la fenêtre de chargement (1000x720)
    window_width = 1000
    window_height = 720

    # Configurer la fenêtre de chargement avec une taille fixe
    loading_window.geometry(f"{window_width}x{window_height}")

    # Déterminer le chemin de l'image avec os.path.join()
    image_path = os.path.join("Gestocks/images", "image.jpg")  # Utilisation de os.path.join()

    # Charger l'image JPG
    loading_image = Image.open(image_path)  # Ouvrir l'image avec le chemin déterminé
    loading_image = loading_image.resize((window_width, window_height))  # Redimensionner l'image pour qu'elle s'adapte à la fenêtre
    loading_photo = ImageTk.PhotoImage(loading_image)

    # Afficher l'image dans un label
    label = tk.Label(loading_window, image=loading_photo)
    label.image = loading_photo  # Garder une référence à l'image pour éviter qu'elle ne soit collectée par le garbage collector
    label.pack(fill="both", expand=True)

    # Retourner la fenêtre de chargement pour qu'elle puisse être détruite plus tard
    return loading_window
