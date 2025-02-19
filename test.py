import tkinter as tk
from tkinter import ttk, messagebox,simpledialog
import os
import sqlite3
from datetime import datetime,timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser
from dotenv import load_dotenv
from tkinter.simpledialog import askstring
import bcrypt
import shutil 

def get_db_path():
    # Récupère le dossier %AppData%/Gestocks
    db_dir = os.path.join(os.getenv('APPDATA'), "Gestocks")
    os.makedirs(db_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas
    return os.path.join(db_dir, "GESTOCK.db")

def calculate_stock_cost():
    db_path = get_db_path()
    if not os.path.exists(db_path):
     original_db_path = os.path.join(os.path.dirname(__file__), "DataBase", "GESTOCK.db")
     shutil.copy2(original_db_path, db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(PrixAchatUnite) FROM stocks")
    stock_cost = cursor.fetchone()[0]
    conn.close()
if calculate_stock_cost() is None:
    print("hey")
else :
    print("raahh")

