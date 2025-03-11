import tkinter as tk
from tkinter import Toplevel
import math

import numpy as np
from PIL import Image, ImageTk
import SimpleITK as sitk

from detekce_GUI_prikazy import nacist_obrazek
from detekce_tromby_napoveda import napoveda
from detekce_GUI_CT_okno import vyber_CT_okna
from projekty.projekt_tromby.detekce_GUI_prikazy import uloz_soubor


# Funkce, která upravuje velikost obrázku transverzální roviny podle velikosti tlačítka
def uprava_velikosti_obrazku_axial(event):
    # Zjisti velikost tlačítka
    sirka = event.width
    vyska = event.height

    # Vyber a uprav rozměr nového obrázku
    rozmer = int(max(sirka, vyska) * 0.8)

    # Změna velikosti obrázku
    obrazek_axial_zmena = obrazek_axial.resize((rozmer, rozmer))
    foto_axial = ImageTk.PhotoImage(obrazek_axial_zmena)

    # Vlož upravený obrázek do tlačítka
    button_axial.config(image=foto_axial, text="Axiální rovina", compound="top")
    button_axial.image = foto_axial

# Funkce, která upravuje velikost obrázku sagitární roviny podle velikosti tlačítka
def uprava_velikosti_obrazku_sagittal(event):
    # Zjisti velikost tlačítka
    sirka = event.width
    vyska = event.height

    # Vyber a uprav rozměr nového obrázku
    rozmer = int(max(sirka, vyska) * 0.8)

    # Změna velikosti obrázku
    obrazek_sagittal_zmena = obrazek_sagittal.resize((rozmer, rozmer))
    foto_sagittal = ImageTk.PhotoImage(obrazek_sagittal_zmena)

    # Vlož upravený obrázek do tlačítka
    button_sagittal.config(image=foto_sagittal, text="Sagitální rovina", compound="top")
    button_sagittal.image = foto_sagittal

# Funkce, která upravuje velikost obrázku frontální roviny podle velikosti tlačítka
def uprava_velikosti_obrazku_coronal(event):
    # Zjisti velikost tlačítka
    sirka = event.width
    vyska = event.height

    # Vyber a uprav rozměr nového obrázku
    rozmer = int(max(sirka, vyska) * 0.8)

    # Změna velikosti obrázku
    obrazek_coronal_zmena = obrazek_coronal.resize((rozmer, rozmer))
    foto_coronal = ImageTk.PhotoImage(obrazek_coronal_zmena)

    # Vlož upravený obrázek do tlačítka
    button_coronal.config(image=foto_coronal, text="Koronální rovina", compound="top")
    button_coronal.image = foto_coronal

# Funkce, která přepisuje současnou anatomickou rovinu
def info_o_rovine(rovina):
    global pouzity_smer
    obrazek = sitk.ReadImage("upload_image.nii")

    # Podle vstupní hodnoty se upraví label na tu anatomickou rovinu, která byla vybrána
    if rovina == "A":
        osa_roviny = (1, 0, 0, 0, 1, 0, 0, 0, 1)
        obrazek.SetDirection(osa_roviny)
        sitk.WriteImage(obrazek, "upload_image.nii")

        pouzity_smer = "A"
        zobraz_obrazek(True)

        text_rovina.config(text="Axiální")
        text_rovina.grid_configure(ipadx=int(math.floor(sirka_okna / 100)))

    elif rovina == "S":
        osa_roviny = (0, 0, -1, 1, 0, 0, 0, 1, 0)
        obrazek.SetDirection(osa_roviny)
        sitk.WriteImage(obrazek, "upload_image.nii")

        pouzity_smer = "S"
        zobraz_obrazek(True)

        text_rovina.config(text="Sagitální")
        text_rovina.grid_configure(ipadx=0)
    else:
        osa_roviny = (1, 0, 0, 0, 0, -1, 0, 1, 0)
        obrazek.SetDirection(osa_roviny)
        sitk.WriteImage(obrazek, "upload_image.nii")

        pouzity_smer = "K"
        zobraz_obrazek(True)

        text_rovina.config(text="Koronální")
        text_rovina.grid_configure(ipadx=0)


# Funkce, jejímž úkolem na načítat uložené obrázky
def zobraz_obrazek(zobrazit):
    global pouzity_smer

    # Pokud je vstupní proměnná False, znamená to, že si uživatel přeje vymazat obrázek -> zobrazí se defaultní obrázek
    if zobrazit == False:
        default_obrazek = Image.open(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")
        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))

        default_obrazek = default_obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))  # Změna velikosti obrázku
        foto = ImageTk.PhotoImage(default_obrazek)

        label_obrazek.config(image=foto)
        label_obrazek.image = foto
        slider.config(to=0)


    # Pokud je vstupní proměnná True, tak je uživateli zobrazen uložený obrázek
    else:
        obrazek = sitk.ReadImage("upload_image.nii")
        obrazek_pole = sitk.GetArrayFromImage(obrazek)

        index_rezu = 0

        if pouzity_smer == "A":
            obrazek_image = Image.fromarray(obrazek_pole[index_rezu, :, :])

            rozmer_obrazu = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
            obrazek_image = obrazek_image.resize((rozmer_obrazu, rozmer_obrazu))

        elif pouzity_smer == "S":
            obrazek_pole_vyrez = obrazek_pole[:, :, index_rezu]
            obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)

            obrazek_image = Image.fromarray(obrazek_pole_vyrez)

            rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
            rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
            obrazek_image = obrazek_image.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))

        else:
            obrazek_pole_vyrez = obrazek_pole[:, index_rezu, :]
            obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)

            obrazek_image = Image.fromarray(obrazek_pole_vyrez)

            rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
            rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
            obrazek_image = obrazek_image.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))


        foto_image = ImageTk.PhotoImage(obrazek_image)

        label_obrazek.config(image=foto_image)
        label_obrazek.image = foto_image
        slider.config(to=(zjisti_pocet_rezu() - 1))

def upravit_rez(cislo_rezu, parametr=0):
    global pouzity_smer

    obrazek = sitk.ReadImage("upload_image.nii")
    obrazek_pole = sitk.GetArrayFromImage(obrazek)

    index_rezu = int(cislo_rezu) + int(parametr)

    if pouzity_smer == "A":
        obrazek = Image.fromarray(obrazek_pole[index_rezu, :, :])

        rozmer_obrazu = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        obrazek = obrazek.resize((rozmer_obrazu, rozmer_obrazu))

    elif pouzity_smer == "S":
        obrazek_pole_vyrez = obrazek_pole[:, :, index_rezu]
        obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)

        obrazek = Image.fromarray(obrazek_pole_vyrez)

        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
        obrazek = obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))

    else:
        obrazek_pole_vyrez = obrazek_pole[:, index_rezu, :]
        obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)

        obrazek = Image.fromarray(obrazek_pole_vyrez)

        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
        obrazek = obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))


    foto = ImageTk.PhotoImage(obrazek)
    label_obrazek.config(image=foto)
    label_obrazek.image = foto
    text_aktualni_rez.config(text=cislo_rezu)

def zjisti_pocet_rezu():
    global pouzity_smer

    try:
        obrazek = sitk.ReadImage("upload_image.nii")
        if pouzity_smer == "A":
            pocet_rezu = obrazek.GetSize()[2]
        else:
            pocet_rezu = obrazek.GetSize()[0]

    except:
        obrazek = sitk.ReadImage(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")
        pocet_rezu = 1

    return pocet_rezu

def pocitadlo():
    global pocet_spusteni
    pocet_spusteni = pocet_spusteni + 1

def posun_vlevo_vpravo(smer):

    pozice_rezu = slider.get()
    maximum_rezu = zjisti_pocet_rezu()

    # True znamená posun doprava, False znamená posun doleva
    if smer == True:
        if pozice_rezu < (maximum_rezu - 1):
            parametr = 1
            upravit_rez(pozice_rezu, parametr)
            slider.set(pozice_rezu + 1)

    else:
        if pozice_rezu > 0:
            parametr = -1
            upravit_rez(pozice_rezu, parametr)
            slider.set(pozice_rezu - 1)

def posun_vlevo_vpravo_klavesnice(event):
    stisknuta_klavesa = event.keysym

    if stisknuta_klavesa == "Left":
        posun_vlevo_vpravo(False)
    else:
        posun_vlevo_vpravo(True)


# Vytvoření hlavního okna
okno = tk.Tk()

# Nastavení velikosti okna podle obrazovky
okno.state("zoomed")
okno.config(bg="white")
sirka_okna = okno.winfo_screenwidth()
vyska_okna = okno.winfo_screenheight()
pouzity_smer = "A"


# Nastavení Frame containeru pro vytvoření barevných pruhů na pozadí
kontejner = tk.Frame(okno, bg="lightblue")
kontejner_2 = tk.Frame(okno, bg="lightblue")
kontejner_3 = tk.Frame(okno, bg="lightblue")
kontejner.grid(row=0, column=0, sticky="nsew", columnspan=13, rowspan=2)
kontejner_2.grid(row=1, column=0, sticky="nsew", rowspan=6)
kontejner_3.grid(row=7, column=0, sticky="nsew", columnspan=13)

# Nastavení a vytvořenní tabulky grid()
odsazeni = 5
odsazeni_mezera = 20
sticky_parametr_sloupec = "ew"
sticky_parametr_radek = "sn"
barva_okraju = "lightblue"
kotva = "center"
pocet_spusteni = 0


for index_sloupce in range(0, 13):
    okno.columnconfigure(index_sloupce, weight=1)
for index_radku in range(3, 6):
    okno.rowconfigure(index_radku, weight=1)

# Vytvoření nadpisu okna a nastavení fontů textu
okno.title("Bolehlav - aplikace pro detekce trombů v CT snímcích mozku")
font_tlacitek = ("Arial", 10, "bold")


# Řídící tlačítka a posuvník
slider = tk.Scale(okno, from_=0, to=(zjisti_pocet_rezu() - 1), orient="horizontal", command=upravit_rez)
slider.grid(row=6, column=4, columnspan=6, sticky=sticky_parametr_sloupec)

tlacitko_predchozi = tk.Button(text="<", font=font_tlacitek, command=lambda: (posun_vlevo_vpravo(False)))
tlacitko_predchozi.grid(row=6, column=3, sticky="e", padx=odsazeni)
tlacitko_dalsi = tk.Button(text=">", font=font_tlacitek, command=lambda: (posun_vlevo_vpravo(True)))
tlacitko_dalsi.grid(row=6, column=10, sticky="w", padx=odsazeni)

# Defaultní obrázek
default_obrazek = Image.open(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")
rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))

default_obrazek = default_obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))  # Změna velikosti obrázku
foto = ImageTk.PhotoImage(default_obrazek)

label_obrazek = tk.Label(okno, image=foto, anchor=kotva, cursor="tcross")
label_obrazek.grid(row=2, column=1, columnspan=12, rowspan=4)
slider.config(to=0)





# Kontrolní tlačítka
# Tlačítka pro ovládání programu
button_nacti = tk.Button(okno, text="Načíst", anchor=kotva, font=font_tlacitek, command=nacist_obrazek)
button_nacti.grid(row=0, column=1, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_uloz = tk.Button(okno, text="Uložit", anchor=kotva, font=font_tlacitek, command=uloz_soubor)
button_uloz.grid(row=0, column=2, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_smazat = tk.Button(okno, text="Smazat", anchor=kotva, font=font_tlacitek, command=lambda: (zobraz_obrazek(False)))
button_smazat.grid(row=0, column=3, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, command=lambda: (zobraz_obrazek(True)))
button_zobraz.grid(row=1, column=1, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=4, sticky=sticky_parametr_sloupec)

# Tlačítka pro úpravu obrazu
button_registrace = tk.Button(okno, text="Registrace", anchor=kotva, font=font_tlacitek)
button_registrace.grid(row=0, column=5, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_multifaze = tk.Button(okno, text="Multifázický obraz", anchor=kotva, font=font_tlacitek)
button_multifaze.grid(row=0, column=6, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_manual_detekce = tk.Button(okno, text="Manuální detekce", anchor=kotva, font=font_tlacitek)
button_manual_detekce.grid(row=0, column=7, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_auto_detekce = tk.Button(okno, text="Automatická detekce", anchor=kotva, font=font_tlacitek)
button_auto_detekce.grid(row=0, column=8, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek)
button_zobraz.grid(row=1, column=5, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)
button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek)
button_zobraz.grid(row=1, column=6, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=9, sticky=sticky_parametr_sloupec)

# Tlačítko pro postrocessing
button_okno = tk.Button(okno, text="CT okno", anchor=kotva, font=font_tlacitek, command=lambda: (vyber_CT_okna(pocet_spusteni), pocitadlo()))
button_okno.grid(row=0, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, command=lambda: (zobraz_obrazek(True)))
button_zobraz.grid(row=1, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=11, sticky=sticky_parametr_sloupec)

# Tlačítko s nápovědou
button_napoveda = tk.Button(okno, text="Nápověda", anchor=kotva, font=font_tlacitek, command=napoveda)
button_napoveda.grid(row=0, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=2, column=0, sticky="ns")


# Doprovodný text
nadpis_rovina = tk.Label(okno, text="Zvolená anatomická rovina:", pady=odsazeni, bg=barva_okraju)
nadpis_rovina.grid(row=7, column=0, sticky=sticky_parametr_radek)
text_rovina = tk.Label(okno, text="Axiální", pady=odsazeni, bg="lightblue")
text_rovina.grid(row=7, column=1, sticky=sticky_parametr_radek, ipadx=int(math.floor(sirka_okna / 100)))

nadpis_pozice_kurzoru = tk.Label(okno, text="Pozice kurzoru:" , pady=odsazeni, bg=barva_okraju)
nadpis_pozice_kurzoru.grid(row=7, column=5, sticky=sticky_parametr_radek)
text_pozice_kurzoru_X = tk.Label(okno, text="souřadnice X", pady=odsazeni, bg=barva_okraju)
text_pozice_kurzoru_X.grid(row=7, column=6, sticky=sticky_parametr_radek)
text_pozice_kurzoru_Y = tk.Label(okno, text="souřadnice Y", pady=odsazeni, bg=barva_okraju)
text_pozice_kurzoru_Y.grid(row=7, column=7, sticky=sticky_parametr_radek)

nadpis_aktualni_rez = tk.Label(okno, text="Aktuální řez:" , pady=odsazeni, bg=barva_okraju)
nadpis_aktualni_rez.grid(row=7, column=10, sticky=sticky_parametr_radek)
text_aktualni_rez = tk.Label(okno, text=0 , pady=odsazeni, bg=barva_okraju)
text_aktualni_rez.grid(row=7, column=11, sticky=sticky_parametr_radek)


# Počáteční nastavení velikostí tlačítek
velikost_obrazu_tlacitka = int(round(((vyska_okna / 4.84) + (sirka_okna / 7.75)) / 2) * 0.9)

# Počáteční nahrání obrázků do tlačítek
obrazek_axial = Image.open(r"C:\Users\perla\OneDrive\Plocha\axial_tlacitko.png")
obrazek_axial_zmena = obrazek_axial.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_axial = ImageTk.PhotoImage(obrazek_axial_zmena)
obrazek_sagittal = Image.open(r"C:\Users\perla\OneDrive\Plocha\sagittal_tlacitko.png")
obrazek_sagittal_zmena = obrazek_sagittal.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_sagittal = ImageTk.PhotoImage(obrazek_sagittal_zmena)
obrazek_coronal = Image.open(r"C:\Users\perla\OneDrive\Plocha\coronal_tlacitko.png")
obrazek_coronal_zmena = obrazek_coronal.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_coronal = ImageTk.PhotoImage(obrazek_coronal_zmena)

# Tlačítka pro změnu anatomické roviny
button_axial = tk.Button(okno, image=foto_axial, text="Axiální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("A"))
button_axial.grid(row=3, column=0, pady=odsazeni, sticky=sticky_parametr_radek)
button_sagittal = tk.Button(okno, image=foto_sagittal, text="Sagitální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("S"))
button_sagittal.grid(row=4, column=0, pady=odsazeni, sticky=sticky_parametr_radek)
button_coronal = tk.Button(okno, image=foto_coronal, text="Koronální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("K"))
button_coronal.grid(row=5, column=0, pady=odsazeni, sticky=sticky_parametr_radek)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=6, column=0, sticky=sticky_parametr_radek)

# Funkce pro volání funkcí, které upravují velikost obrázků v tlačítcích
button_axial.bind("<Configure>", uprava_velikosti_obrazku_axial)
button_sagittal.bind("<Configure>", uprava_velikosti_obrazku_sagittal)
button_coronal.bind("<Configure>", uprava_velikosti_obrazku_coronal)
okno.bind("<Left>", posun_vlevo_vpravo_klavesnice)
okno.bind("<Right>", posun_vlevo_vpravo_klavesnice)

# Hlavní smyčka aplikace
okno.mainloop()
