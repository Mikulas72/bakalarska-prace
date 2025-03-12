# Knihovny potřebné pro chod GUI
import tkinter as tk
import math
import numpy as np
from PIL import Image, ImageTk
import SimpleITK as sitk

# Propojení ostatních pomocných skriptů s hlavním skriptem GUI
from detekce_GUI_prikazy import nacist_obrazek
from detekce_tromby_napoveda import napoveda
from detekce_GUI_CT_okno import vyber_CT_okna
from projekty.projekt_tromby.detekce_GUI_prikazy import uloz_soubor


# Blok kódu s funkcemi pro správný chod GUI
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

    # Podle vstupní hodnoty se upraví zpráva a pomocný text na tu anatomickou rovinu, která byla vybrána
    if rovina == "A":
        # Nastavení správného direction podle vybraného požadavku uživatele
        osa_roviny = (1, 0, 0, 0, 1, 0, 0, 0, 1)
        obrazek.SetDirection(osa_roviny)
        sitk.WriteImage(obrazek, "upload_image.nii")

        # Volání funkce "zobraz_obrazek" která podle vybrané anatomické roviny upraví obraz a ten zobrazí uživateli
        pouzity_smer = "A"
        zobraz_obrazek(True)

        # Úprava pomocného textu, aby uživatel věděl, v jaké anatomické rovině se nachází
        text_rovina.config(text="Axiální")
        text_rovina.grid_configure(ipadx=int(math.floor(sirka_okna / 100)))

    elif rovina == "S":
        # Nastavení správného direction podle vybraného požadavku uživatele
        osa_roviny = (0, 0, -1, 1, 0, 0, 0, 1, 0)
        obrazek.SetDirection(osa_roviny)
        sitk.WriteImage(obrazek, "upload_image.nii")

        # Volání funkce "zobraz_obrazek" která podle vybrané anatomické roviny upraví obraz a ten zobrazí uživateli
        pouzity_smer = "S"
        zobraz_obrazek(True)

        # Úprava pomocného textu, aby uživatel věděl, v jaké anatomické rovině se nachází
        text_rovina.config(text="Sagitální")
        text_rovina.grid_configure(ipadx=0)
    else:
        # Nastavení správného direction podle vybraného požadavku uživatele
        osa_roviny = (1, 0, 0, 0, 0, -1, 0, 1, 0)
        obrazek.SetDirection(osa_roviny)
        sitk.WriteImage(obrazek, "upload_image.nii")

        # Volání funkce "zobraz_obrazek" která podle vybrané anatomické roviny upraví obraz a ten zobrazí uživateli
        pouzity_smer = "K"
        zobraz_obrazek(True)

        # Úprava pomocného textu, aby uživatel věděl, v jaké anatomické rovině se nachází
        text_rovina.config(text="Koronální")
        text_rovina.grid_configure(ipadx=0)

# Funkce, jejímž úkolem na načítat uložené obrázky
def zobraz_obrazek(zobrazit):
    global pouzity_smer

    # Pokud je vstupní proměnná False, znamená to, že si uživatel přeje vymazat obrázek -> zobrazí se defaultní obrázek
    if zobrazit == False:
        default_obrazek = Image.open(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")

        # Vstupní obrázek se přizpůsobí podle rozměrů uživatelské obrazovky
        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
        default_obrazek = default_obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))  # Změna velikosti obrázku

        # Defaultní obrázek se načte a zobrazí v příslušné oblasti GUI
        foto = ImageTk.PhotoImage(default_obrazek)
        label_obrazek.config(image=foto)
        label_obrazek.image = foto

        # Slider se nastaví na 0 (defaultní obrázek má totiž jen 1 rěz -> slider se tím deaktivuje)
        slider.config(to=0)


    # Pokud je vstupní proměnná True, tak je uživateli zobrazen uložený obrázek
    else:
        # Požadovaný obrázek se načte a převede na numpy matici
        obrazek = sitk.ReadImage("upload_image.nii")
        obrazek_pole = sitk.GetArrayFromImage(obrazek)

        index_rezu = 0

        # Funkce následně zjišťuje, jakou anatomickou rovinu se uživatel přál
        # Pokud je požadovaný směr označen "A", tak to znamená, že si uživatel přeje axiální anatomickou rovinu
        if pouzity_smer == "A":
            # Provede se výběr požadovaného řezu
            obrazek_image = Image.fromarray(obrazek_pole[index_rezu, :, :])

            # Změní se rozměry řezu tak, aby odpovídali obrazovce uživatele
            rozmer_obrazu = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
            obrazek_image = obrazek_image.resize((rozmer_obrazu, rozmer_obrazu))

        # Pokud je požadovaný směr označen "S", tak to znamená, že si uživatel přeje sagitární anatomickou rovinu
        elif pouzity_smer == "S":
            # Provede se výběr požadovaného řezu a obraz se překlopí (aby nebyl zobrazen vzhůru nohama)
            obrazek_pole_vyrez = obrazek_pole[:, :, index_rezu]
            obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)
            obrazek_image = Image.fromarray(obrazek_pole_vyrez)

            # Změní se rozměry řezu tak, aby odpovídali obrazovce uživatele
            rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
            rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
            obrazek_image = obrazek_image.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))

        # Pokud je požadovaný směr označen "K", tak to znamená, že si uživatel přeje koronální anatomickou rovinu
        else:
            # Provede se výběr požadovaného řezu a obraz se překlopí (aby nebyl zobrazen vzhůru nohama)
            obrazek_pole_vyrez = obrazek_pole[:, index_rezu, :]
            obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)
            obrazek_image = Image.fromarray(obrazek_pole_vyrez)

            # Změní se rozměry řezu tak, aby odpovídali obrazovce uživatele
            rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
            rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
            obrazek_image = obrazek_image.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))

        # Provede se vykreslení daného řezu v konkrétním místě GUI
        foto_image = ImageTk.PhotoImage(obrazek_image)
        label_obrazek.config(image=foto_image)
        label_obrazek.image = foto_image

        # Slider se přenastaví tak, aby obsáhl všechny možné řezy přes danou anatomickou rovinu daného obrazu
        slider.config(to=(zjisti_pocet_rezu() - 1))

# Tato funkce mění již zobrazený obraz podle toho, jaký řez si přeje uživatel
def upravit_rez(cislo_rezu, parametr=0):
    global pouzity_smer

    # Konkrétní obraz se nahraje z paměti a převede se na numpy matici
    obrazek = sitk.ReadImage("upload_image.nii")
    obrazek_pole = sitk.GetArrayFromImage(obrazek)

    # Index požadovaného řezu se nastaví podle zadání uživatele
    index_rezu = int(cislo_rezu) + int(parametr)

    # Pokud je požadovaný směr označen "A", tak to znamená, že si uživatel přeje axiální anatomickou rovinu
    if pouzity_smer == "A":
        # Provede se výběr požadovaného řezu
        obrazek = Image.fromarray(obrazek_pole[index_rezu, :, :])

        # Změní se rozměry řezu tak, aby odpovídali obrazovce uživatele
        rozmer_obrazu = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        obrazek = obrazek.resize((rozmer_obrazu, rozmer_obrazu))

    # Pokud je požadovaný směr označen "S", tak to znamená, že si uživatel přeje sagitární anatomickou rovinu
    elif pouzity_smer == "S":
        # Provede se výběr požadovaného řezu a obraz se překlopí (aby nebyl zobrazen vzhůru nohama)
        obrazek_pole_vyrez = obrazek_pole[:, :, index_rezu]
        obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)
        obrazek = Image.fromarray(obrazek_pole_vyrez)

        # Změní se rozměry řezu tak, aby odpovídali obrazovce uživatele
        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
        obrazek = obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))

    # Pokud je požadovaný směr označen "K", tak to znamená, že si uživatel přeje koronální anatomickou rovinu
    else:
        # Provede se výběr požadovaného řezu a obraz se překlopí (aby nebyl zobrazen vzhůru nohama)
        obrazek_pole_vyrez = obrazek_pole[:, index_rezu, :]
        obrazek_pole_vyrez = np.flip(obrazek_pole_vyrez, axis=0)
        obrazek = Image.fromarray(obrazek_pole_vyrez)

        # Změní se rozměry řezu tak, aby odpovídali obrazovce uživatele
        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
        obrazek = obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))

    # Provede se vykreslení daného řezu v konkrétním místě GUI
    foto = ImageTk.PhotoImage(obrazek)
    label_obrazek.config(image=foto)
    label_obrazek.image = foto

    # Změní se text na pomocné liště, čímž je uživateli přesně řečeno, s jakou anatomickou rovinou pracuje
    text_aktualni_rez.config(text=cislo_rezu)

# Tato funkce zjišťuje, kolik celkem řezů má obraz, který se uživatel snaží zobrazit
def zjisti_pocet_rezu():
    global pouzity_smer

    # Funkce vyzkouší, zda je vůbec možné zjistit počet řezů
    # Pokud je to možné, tak počet řezů zjistí
    try:
        obrazek = sitk.ReadImage("upload_image.nii")

        # Podle vybrané anatomické roviny se si funkce zjistí celkový počet řezů v dané anatomické rovině
        if pouzity_smer == "A":
            pocet_rezu = obrazek.GetSize()[2]
        else:
            pocet_rezu = obrazek.GetSize()[0]

    # Pokud to není možné (např.: pracuje se z defaultním obrazem), nastaví se počet řezů na 1
    except:
        obrazek = sitk.ReadImage(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")
        pocet_rezu = 1

    # Funkce následně vrátí celkový počet řezů daného obrazu v dané anatomické rovině
    return pocet_rezu

# Úkolem této funkce je počítat, kolikrát byla spuštěn postprocessing (CT okno) -> důležité pro správné fungování postprocessingu
def pocitadlo():
    global pocet_spusteni
    pocet_spusteni = pocet_spusteni + 1

# Tato funkce zajišťuje fungování tlačítek pro posun řezu anatomickou rovinou
def posun_vlevo_vpravo(smer):
    # Nejprve je zjištěna pozice slideru a maximální počet řezů
    pozice_rezu = slider.get()
    maximum_rezu = zjisti_pocet_rezu()

    # Pokud je příchozí hodnota True, tak to znamená posun o 1 řez doprava
    if smer == True:
        # Zkontroluje se podmínka, že se slider nenachází v krajních podmínkách (že se uživatel snaží vybrat řez mimo rozsah všech řezů)
        if pozice_rezu < (maximum_rezu - 1):
            parametr = 1
            # Zavolá se funkce pro nastavení nového řezu
            upravit_rez(pozice_rezu, parametr)
            # Slider se nastaví na nový řez
            slider.set(pozice_rezu + 1)

    # Pokud je příchozí hodnota False, tak to znamená posun o 1 řez doleva
    else:
        # Zkontroluje se podmínka, že se slider nenachází v krajních podmínkách (že se uživatel snaží vybrat řez mimo rozsah všech řezů)
        if pozice_rezu > 0:
            parametr = -1
            # Zavolá se funkce pro nastavení nového řezu
            upravit_rez(pozice_rezu, parametr)
            # Slider se nastaví na nový řez
            slider.set(pozice_rezu - 1)

# Tato funkce zajišťuje fungování kláves pro posun řezu anatomickou rovinou
def posun_vlevo_vpravo_klavesnice(event):
    stisknuta_klavesa = event.keysym

    # Podle zmáčknuté klávesy "Left" nebo "Right" je zavolána funkce "posun_vlevo_vpravo" s příslušným parametrem
    if stisknuta_klavesa == "Left":
        posun_vlevo_vpravo(False)
    else:
        posun_vlevo_vpravo(True)


# Vytvoření hlavního okna
okno = tk.Tk()

# Nastavení velikosti okna podle obrazovky a anatomické rovina na axiální (využívá se nejvíce)
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

# Parametry použité pro nastavení tabulky grid()
odsazeni = 5
odsazeni_mezera = 20
sticky_parametr_sloupec = "ew"
sticky_parametr_radek = "sn"
barva_okraju = "lightblue"
kotva = "center"
pocet_spusteni = 0

# For cykly vytvářející prvotní strukturu tabulky grid() pro GUI
for index_sloupce in range(0, 13):
    okno.columnconfigure(index_sloupce, weight=1)
for index_radku in range(3, 6):
    okno.rowconfigure(index_radku, weight=1)

# Vytvoření nadpisu okna a nastavení fontu tlačítek
okno.title("Bolehlav - aplikace pro detekce trombů v CT snímcích mozku")
font_tlacitek = ("Arial", 10, "bold")


# Vytovření a umístění posuvníku
slider = tk.Scale(okno, from_=0, to=(zjisti_pocet_rezu() - 1), orient="horizontal", command=upravit_rez)
slider.grid(row=6, column=4, columnspan=6, sticky=sticky_parametr_sloupec)

# Vytovření a umístění tlačítek pro přepínání předchozího a následujícího řezu
tlacitko_predchozi = tk.Button(text="<", font=font_tlacitek, command=lambda: (posun_vlevo_vpravo(False)))
tlacitko_predchozi.grid(row=6, column=3, sticky="e", padx=odsazeni)
tlacitko_dalsi = tk.Button(text=">", font=font_tlacitek, command=lambda: (posun_vlevo_vpravo(True)))
tlacitko_dalsi.grid(row=6, column=10, sticky="w", padx=odsazeni)


# Defaultní obrázek
default_obrazek = Image.open(r"C:\Users\perla\OneDrive\Plocha\mozek_default_ikona.png")
rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))

# Změna velikosti defaultního obrázku podle velikosti uživatelova okna
default_obrazek = default_obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))
foto = ImageTk.PhotoImage(default_obrazek)

# Umístění defaultního obrázku do GUI
label_obrazek = tk.Label(okno, image=foto, anchor=kotva, cursor="tcross")
label_obrazek.grid(row=2, column=1, columnspan=12, rowspan=4)
slider.config(to=0)


# Kontrolní tlačítka
# Tlačítka pro ovládání programu (Načíst, Uložit, Smazat a Zobrazit obraz)
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


# Tlačítka pro úpravu obrazu (Registrace, Vytvoření multifázického obrazu, manuální a automatická detekce a Zobraz výsledky)
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


# Tlačítko pro postrocessing (nastavení požadovaného CT okna a zobrazení výsledného CT okna)
button_okno = tk.Button(okno, text="CT okno", anchor=kotva, font=font_tlacitek, command=lambda: (vyber_CT_okna(pocet_spusteni), pocitadlo()))
button_okno.grid(row=0, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, command=lambda: (zobraz_obrazek(True)))
button_zobraz.grid(row=1, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=11, sticky=sticky_parametr_sloupec)


# Tlačítko s nápovědou k GUI
button_napoveda = tk.Button(okno, text="Nápověda", anchor=kotva, font=font_tlacitek, command=napoveda)
button_napoveda.grid(row=0, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=2, column=0, sticky="ns")


# Pomocný text pro lepší orientaci uživatele (zvolená anatomická rovina, pozice kurzoru (X, Y) a aktuální řez obrazem)
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

# Počáteční nahrání obrázků do tlačítek pro výběr anatomické roviny
obrazek_axial = Image.open(r"C:\Users\perla\OneDrive\Plocha\axial_tlacitko.png")
obrazek_axial_zmena = obrazek_axial.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_axial = ImageTk.PhotoImage(obrazek_axial_zmena)
obrazek_sagittal = Image.open(r"C:\Users\perla\OneDrive\Plocha\sagittal_tlacitko.png")
obrazek_sagittal_zmena = obrazek_sagittal.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_sagittal = ImageTk.PhotoImage(obrazek_sagittal_zmena)
obrazek_coronal = Image.open(r"C:\Users\perla\OneDrive\Plocha\coronal_tlacitko.png")
obrazek_coronal_zmena = obrazek_coronal.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_coronal = ImageTk.PhotoImage(obrazek_coronal_zmena)

# Tlačítka pro změnu anatomické roviny (axiální, sagitární a koronální roviny)
button_axial = tk.Button(okno, image=foto_axial, text="Axiální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("A"))
button_axial.grid(row=3, column=0, pady=odsazeni, sticky=sticky_parametr_radek)
button_sagittal = tk.Button(okno, image=foto_sagittal, text="Sagitální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("S"))
button_sagittal.grid(row=4, column=0, pady=odsazeni, sticky=sticky_parametr_radek)
button_coronal = tk.Button(okno, image=foto_coronal, text="Koronální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("K"))
button_coronal.grid(row=5, column=0, pady=odsazeni, sticky=sticky_parametr_radek)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=6, column=0, sticky=sticky_parametr_radek)


# Funkce pro volání funkcí, které upravují velikost obrázků v tlačítcích (automaticky)
button_axial.bind("<Configure>", uprava_velikosti_obrazku_axial)
button_sagittal.bind("<Configure>", uprava_velikosti_obrazku_sagittal)
button_coronal.bind("<Configure>", uprava_velikosti_obrazku_coronal)

# Funkce pro volání funkcí, které reagují na zmáčknutí šipek na klávesnici (automaticky)
okno.bind("<Left>", posun_vlevo_vpravo_klavesnice)
okno.bind("<Right>", posun_vlevo_vpravo_klavesnice)

# Hlavní smyčka aplikace
okno.mainloop()
