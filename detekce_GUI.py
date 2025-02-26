import tkinter as tk
from tkinter import Toplevel
import math
from PIL import Image, ImageTk
import SimpleITK as sitk

from pythonProject.projekty.projekt_tromby.detekce_GUI_prikazy import nacist_obrazek, uloz_soubor
from pythonProject.projekty.projekt_tromby.detekce_tromby_napoveda import napoveda


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
    button_axial.config(image=foto_axial, text="Transverzální rovina", compound="top")
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
    button_sagittal.config(image=foto_sagittal, text="Sagitární rovina", compound="top")
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
    button_coronal.config(image=foto_coronal, text="Frontální rovina", compound="top")
    button_coronal.image = foto_coronal

def info_o_rovine(rovina):
    if rovina == "T":
        text_rovina.config(text="Transverzální")
        text_rovina.grid_configure(ipadx=0)
    elif rovina == "S":
        text_rovina.config(text="Sagitární")
        text_rovina.grid_configure(ipadx=int(math.floor(sirka_okna / 100)))
    elif rovina == "F":
        text_rovina.config(text="Frontální")
        text_rovina.grid_configure(ipadx=int(math.floor(sirka_okna / 100)))


# Vytvoření hlavního okna
okno = tk.Tk()

# Nastavení velikosti okna podle obrazovky
okno.state("zoomed")
okno.config(bg="white")
sirka_okna = okno.winfo_screenwidth()
vyska_okna = okno.winfo_screenheight()

# Nastavení Frame containeru pro vytvoření barevných pruhů na pozadí
kontejner = tk.Frame(okno, bg="lightblue")
kontejner_2 = tk.Frame(okno, bg="lightblue")
kontejner_3 = tk.Frame(okno, bg="lightblue")
kontejner.grid(row=0, column=0, sticky="nsew", columnspan=13)
kontejner_2.grid(row=1, column=0, sticky="nsew", rowspan=5)
kontejner_3.grid(row=6, column=0, sticky="nsew", columnspan=13)

# Nastavení a vytvořenní tabulky grid()
odsazeni = 5
odsazeni_mezera = 20
sticky_parametr_sloupec = "ew"
sticky_parametr_radek = "sn"
barva_okraju = "lightblue"
kotva = "center"

for index_sloupce in range(0, 13):
    okno.columnconfigure(index_sloupce, weight=1)
for index_radku in range(2, 5):
    okno.rowconfigure(index_radku, weight=1)

# Vytvoření nadpisu okna a nastavení fontů textu
okno.title("Bolehlav - aplikace pro detekce trombů v CT snímcích mozku")
font_tlacitek = ("Arial", 10, "bold")


# Defaultní obrázek
default_obrazek = Image.open(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")
rozmer_obrazu = min(sirka_okna, vyska_okna) - 200
default_obrazek = default_obrazek.resize((rozmer_obrazu, rozmer_obrazu))  # Změna velikosti obrázku
foto = ImageTk.PhotoImage(default_obrazek)

label_obrazek = tk.Label(okno, image=foto, anchor=kotva)
label_obrazek.grid(row=1, column=1, columnspan=12, rowspan=4)


def zobraz_obrazek():
    obrazek = sitk.ReadImage("upload_image.nii")
    obrazek_pole = sitk.GetArrayFromImage(obrazek)

    index_rezu = 200
    obrazek_image = Image.fromarray(obrazek_pole[index_rezu, :, :])

    rozmer_obrazu = min(sirka_okna, vyska_okna) - 200
    obrazek_image = obrazek_image.resize((rozmer_obrazu, rozmer_obrazu))

    foto_image = ImageTk.PhotoImage(obrazek_image)

    label_obrazek.config(image=foto_image)
    label_obrazek.image = foto_image



# Kontrolní tlačítka
# Tlačítka pro ovládání programu
button_nacti = tk.Button(okno, text="Načíst", anchor=kotva, font=font_tlacitek, command=zobraz_obrazek)
button_nacti.grid(row=0, column=1, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_uloz = tk.Button(okno, text="Uložit", anchor=kotva, font=font_tlacitek, command=uloz_soubor)
button_uloz.grid(row=0, column=2, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_smazat = tk.Button(okno, text="Smazat", anchor=kotva, font=font_tlacitek)
button_smazat.grid(row=0, column=3, padx=odsazeni, sticky=sticky_parametr_sloupec)

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

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=9, sticky=sticky_parametr_sloupec)

# Tlačítko pro postrocessing
button_okno = tk.Button(okno, text="CT okno", anchor=kotva, font=font_tlacitek)
button_okno.grid(row=0, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=11, sticky=sticky_parametr_sloupec)

# Tlačítko s nápovědou
button_napoveda = tk.Button(okno, text="Nápověda", anchor=kotva, font=font_tlacitek, command=napoveda)
button_napoveda.grid(row=0, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=1, column=0, sticky="ns")


# Doprovodný text
nadpis_rovina = tk.Label(okno, text="Zvolená anatomická rovina:", pady=odsazeni, bg=barva_okraju)
nadpis_rovina.grid(row=6, column=0, sticky=sticky_parametr_radek)
text_rovina = tk.Label(okno, text="Transverzální", pady=odsazeni, bg="lightblue")
text_rovina.grid(row=6, column=1, sticky=sticky_parametr_radek, ipadx=0)

nadpis_pozice_kurzoru = tk.Label(okno, text="Pozice kurzoru:" , pady=odsazeni, bg=barva_okraju)
nadpis_pozice_kurzoru.grid(row=6, column=5, sticky=sticky_parametr_radek)
text_pozice_kurzoru = tk.Label(okno, text="(X, Y, Z)", pady=odsazeni, bg=barva_okraju)
text_pozice_kurzoru.grid(row=6, column=6, sticky=sticky_parametr_radek)


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
button_axial = tk.Button(okno, image=foto_axial, text="Transverzální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("T"))
button_axial.grid(row=2, column=0, pady=odsazeni, sticky=sticky_parametr_radek)
button_sagittal = tk.Button(okno, image=foto_sagittal, text="Sagitární rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("S"))
button_sagittal.grid(row=3, column=0, pady=odsazeni, sticky=sticky_parametr_radek)
button_coronal = tk.Button(okno, image=foto_coronal, text="Frontální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("F"))
button_coronal.grid(row=4, column=0, pady=odsazeni, sticky=sticky_parametr_radek)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=5, column=0, sticky=sticky_parametr_radek)

# Funkce pro volání funkcí, které upravují velikost obrázků v tlačítcích
button_axial.bind("<Configure>", uprava_velikosti_obrazku_axial)
button_sagittal.bind("<Configure>", uprava_velikosti_obrazku_sagittal)
button_coronal.bind("<Configure>", uprava_velikosti_obrazku_coronal)

# Řídící tlačítka a posuvník
slider = tk.Scale(orient="horizontal")
slider.grid(row=5, column=4, columnspan=6, sticky=sticky_parametr_sloupec)

tlacitko_predchozi = tk.Button(text="<", font=font_tlacitek)
tlacitko_predchozi.grid(row=5, column=3, sticky="e", padx=odsazeni)
tlacitko_dalsi = tk.Button(text=">", font=font_tlacitek)
tlacitko_dalsi.grid(row=5, column=10, sticky="w", padx=odsazeni)


# Hlavní smyčka aplikace
okno.mainloop()
