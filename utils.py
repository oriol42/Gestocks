import tkinter as tk

def show_frame(frame_name, frames, expand=True, fill="both"):
    """
    Affiche le cadre correspondant au nom donné.

    Paramètres :
    frame_name (str) : Le nom de la frame à afficher.
    frames (dict) : Un dictionnaire contenant les frames, avec leurs noms comme clés.
    expand (bool) : Si True, le cadre occupe tout l'espace disponible. Par défaut, True.
    fill (str) : Direction dans laquelle la frame doit être étendue. Par défaut, "both".
    """
    # Vérifier si le nom de la frame existe dans le dictionnaire des frames
    if frame_name not in frames:
        raise ValueError(f"Le cadre '{frame_name}' n'existe pas dans les frames.")
    
    # Masquer toutes les autres frames
    for frame in frames.values():
        frame.pack_forget()
    
    # Afficher la frame sélectionnée
    frames[frame_name].pack(fill=fill, expand=expand)

