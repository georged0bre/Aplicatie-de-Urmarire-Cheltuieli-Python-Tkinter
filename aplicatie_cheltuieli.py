import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date
import matplotlib.pyplot as plt
from collections import defaultdict

# fisierul unde sunt salvate cheltuielile
FIȘIER = "cheltuieli.json"

# functia care încarcă cheltuielile din fișier
def incarca_cheltuieli():
    if os.path.exists(FIȘIER):
        with open(FIȘIER, 'r') as f:
            return json.load(f)
    return []

# functia care salvează cheltuielile în fișier
def salveaza_cheltuieli(cheltuieli):
    with open(FIȘIER, 'w') as f:
        json.dump(cheltuieli, f, indent=4)

# functia care adaugă o cheltuială
def adauga_cheltuiala(suma, categorie, descriere):
    cheltuieli = incarca_cheltuieli()
    cheltuieli.append({
        "suma": suma,
        "categorie": categorie,
        "descriere": descriere,
        "data": str(date.today())
    })
    salveaza_cheltuieli(cheltuieli)

# functia care afișează graficul cheltuielilor pe categorii
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

# functia care se execută atunci când adaugi o cheltuială
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

# interfata grafica
fereastra = tk.Tk()
fereastra.title("Aplicație de Urmărire Cheltuieli")
fereastra.geometry("300x300")

# eticheta si campul pentru suma
tk.Label(fereastra, text="Sumă").pack(pady=2)
entry_suma = tk.Entry(fereastra)
entry_suma.pack()

# eticheta si lista derulanta pentru categorie
tk.Label(fereastra, text="Categorie").pack(pady=2)
combo_categorie = ttk.Combobox(fereastra, values=["Mâncare", "Transport", "Utilități", "Distracție", "Altele"])
combo_categorie.pack()
combo_categorie.set("Mâncare")

# eticheta și campul pentru descriere
tk.Label(fereastra, text="Descriere").pack(pady=2)
entry_descriere = tk.Entry(fereastra)
entry_descriere.pack()

# butonul pentru a adauga cheltuiala
tk.Button(fereastra, text="Adaugă Cheltuială", command=trimite).pack(pady=5)
# butonul pentru a arata graficul
tk.Button(fereastra, text="Arată Grafic", command=arata_grafic_cheltuieli).pack(pady=5)

fereastra.mainloop()
