import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date
import matplotlib.pyplot as plt
from collections import defaultdict

# Fișierul unde sunt salvate cheltuielile
FIȘIER = "cheltuieli.json"

# Funcția care încarcă cheltuielile din fișier
def incarca_cheltuieli():
    if os.path.exists(FIȘIER):
        with open(FIȘIER, 'r') as f:
            return json.load(f)
    return []

# Funcția care salvează cheltuielile în fișier
def salveaza_cheltuieli(cheltuieli):
    with open(FIȘIER, 'w') as f:
        json.dump(cheltuieli, f, indent=4)

# Funcția care adaugă o cheltuială
def adauga_cheltuiala(suma, categorie, descriere):
    cheltuieli = incarca_cheltuieli()
    cheltuieli.append({
        "suma": suma,
        "categorie": categorie,
        "descriere": descriere,
        "data": str(date.today())
    })
    salveaza_cheltuieli(cheltuieli)

# Funcția care afișează graficul cheltuielilor pe categorii
def arata_grafic_cheltuieli():
    cheltuieli = incarca_cheltuieli()
    date = defaultdict(float)
    for item in cheltuieli:
        date[item["categorie"]] += float(item["suma"])
    
    categorii = list(date.keys())
    valori = list(date.values())

    plt.bar(categorii, valori, color='skyblue')
    plt.title("Cheltuieli pe Categorie")
    plt.ylabel("Suma")
    plt.show()

# Funcția care se execută atunci când adaugi o cheltuială
def trimite():
    try:
        suma = float(entry_suma.get())
        categorie = combo_categorie.get()
        descriere = entry_descriere.get()
        adauga_cheltuiala(suma, categorie, descriere)
        messagebox.showinfo("Succes", "Cheltuiala a fost adăugată!")
        entry_suma.delete(0, tk.END)
        entry_descriere.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Eroare", "Sumă invalidă!")

# Interfața grafică
fereastra = tk.Tk()
fereastra.title("Aplicație de Urmărire Cheltuieli")
fereastra.geometry("300x300")

# Eticheta și câmpul pentru sumă
tk.Label(fereastra, text="Sumă").pack(pady=2)
entry_suma = tk.Entry(fereastra)
entry_suma.pack()

# Eticheta și lista derulantă pentru categorie
tk.Label(fereastra, text="Categorie").pack(pady=2)
combo_categorie = ttk.Combobox(fereastra, values=["Mâncare", "Transport", "Utilități", "Distracție", "Altele"])
combo_categorie.pack()
combo_categorie.set("Mâncare")

# Eticheta și câmpul pentru descriere
tk.Label(fereastra, text="Descriere").pack(pady=2)
entry_descriere = tk.Entry(fereastra)
entry_descriere.pack()

# Butonul pentru a adăuga cheltuiala
tk.Button(fereastra, text="Adaugă Cheltuială", command=trimite).pack(pady=5)
# Butonul pentru a arăta graficul
tk.Button(fereastra, text="Arată Grafic", command=arata_grafic_cheltuieli).pack(pady=5)

fereastra.mainloop()
