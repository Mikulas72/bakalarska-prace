# Knihovny potřebné pro chod GUI
import csv
import tkinter as tk
from tkinter import filedialog
import math
import numpy as np
from PIL import Image, ImageTk
import SimpleITK as sitk
import os


# Propojení ostatních pomocných skriptů s hlavním skriptem GUI
from detekce_GUI_prikazy import nacist_obrazek
from detekce_tromby_napoveda import napoveda
from detekce_GUI_CT_okno import vyber_CT_okna
from detekce_GUI_prikazy import uloz_soubor, odpoved_po_ulozeni
from detekce_tromby_multifaze import vyber_multifazi
from detekce_GUI_registrace import vyber_registraci


# Blok kódu s funkcemi pro správný chod GUI
# Funkce, která upravuje velikost obrázku transverzální roviny podle velikosti tlačítka
def uprava_velikosti_obrazku_axial(event):
    # Zjisti velikost tlačítka
    sirka = event.width
    vyska = event.height

    # Vyber a uprav rozměr nového obrázku
    rozmer = int(max(sirka, vyska) * 0.85)

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
    rozmer = int(max(sirka, vyska) * 0.85)

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
    rozmer = int(max(sirka, vyska) * 0.85)

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
    global obrazek_id
    global ikona_mozku
    global pocatecni_smer_axial

    # Když je funkce pro zobrazení obrázku spuštěna poprvé, tak se automaticky nastaví axiální směr (nejvyužívanější směr)
    if pocatecni_smer_axial == True:
        pocatecni_smer_axial = False
        pouzity_smer = "A"
        text_rovina.config(text="Axiální")

    # Pokud je vstupní proměnná False, znamená to, že si uživatel přeje vymazat obrázek -> zobrazí se defaultní obrázek
    if zobrazit == False:
        default_obrazek = Image.open(r"obrazky_GUI\mozek_default_ikona.png")

        # Při zobrazení defaultního obrazu se proměnná "ikona_mozku" přepne na True -> důležité pro sledovaní pozice myši
        ikona_mozku = True

        # Vstupní obrázek se přizpůsobí podle rozměrů uživatelské obrazovky
        rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
        rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))
        default_obrazek = default_obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))  # Změna velikosti obrázku

        # Defaultní obrázek se načte a zobrazí v příslušné oblasti GUI
        foto = ImageTk.PhotoImage(default_obrazek)

        # Odstraníme starý obrázek
        canvas_obrazek.delete(obrazek_id)

        # Nakonfigurujeme canvas (oblast pro kreslení (kvůli detekci)) tak, aby odpovídal rozměrům obrazu a do takto upraveného canvasu vložíme obrázek jako pozadí
        canvas_obrazek.config(width=rozmer_obrazu_sirka, height=rozmer_obrazu_vyska)
        obrazek_id = canvas_obrazek.create_image((rozmer_obrazu_sirka / 2), (rozmer_obrazu_vyska / 2), image=foto, anchor=kotva)

        # Uchováme nový obrázek, aby nevypršel odkaz
        canvas_obrazek.image = foto

        # Slider se nastaví na 0 (defaultní obrázek má totiž jen 1 rěz -> slider se tím deaktivuje)
        slider.config(to=0)


    # Pokud je vstupní proměnná True, tak je uživateli zobrazen uložený obrázek
    else:
        # Požadovaný obrázek se načte a převede na numpy matici
        obrazek = sitk.ReadImage("upload_image.nii")
        obrazek_pole = sitk.GetArrayFromImage(obrazek)

        # Při zobrazení požadovaného obrazu se proměnná "ikona_mozku" přepne na False -> důležité pro sledovaní pozice myši
        ikona_mozku = False

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

        # Odstraníme starý obrázek
        canvas_obrazek.delete(obrazek_id)

        # Pokud uživatel upravuje axiální obraz, tak se canvas nastaví na čtvercové rozměry, jinak na se nastaví na rozměry obdelníku
        # Nakonfigurujeme canvas (oblast pro kreslení (kvůli detekci)) tak, aby odpovídal rozměrům obrazu a do takto upraveného canvasu vložíme obrázek jako pozadí
        if pouzity_smer == "A":
            canvas_obrazek.config(width=rozmer_obrazu, height=rozmer_obrazu)
            obrazek_id = canvas_obrazek.create_image((rozmer_obrazu / 2), (rozmer_obrazu / 2), image=foto_image, anchor=kotva)
        else:
            canvas_obrazek.config(width=rozmer_obrazu_sirka, height=rozmer_obrazu_vyska)
            obrazek_id = canvas_obrazek.create_image((rozmer_obrazu_sirka / 2), (rozmer_obrazu_vyska / 2), image=foto_image, anchor=kotva)

        # Uchováme nový obrázek, aby nevypršel odkaz
        canvas_obrazek.image = foto_image

        # Slider se přenastaví tak, aby obsáhl všechny možné řezy přes danou anatomickou rovinu daného obrazu
        slider.config(to=(zjisti_pocet_rezu() - 1))

# Tato funkce mění již zobrazený obraz podle toho, jaký řez si přeje uživatel
def upravit_rez(cislo_rezu, parametr=0):
    global pouzity_smer
    global obrazek_id

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

    # Odstraníme starý obrázek
    canvas_obrazek.delete(obrazek_id)

    # Pokud uživatel upravuje axiální obraz, tak se canvas nastaví na čtvercové rozměry, jinak na se nastaví na rozměry obdelníku
    # Nakonfigurujeme canvas (oblast pro kreslení (kvůli detekci)) tak, aby odpovídal rozměrům obrazu a do takto upraveného canvasu vložíme obrázek jako pozadí
    if pouzity_smer == "A":
        canvas_obrazek.config(width=rozmer_obrazu, height=rozmer_obrazu)
        obrazek_id = canvas_obrazek.create_image((rozmer_obrazu / 2), (rozmer_obrazu / 2), image=foto, anchor=kotva)
    else:
        canvas_obrazek.config(width=rozmer_obrazu_sirka, height=rozmer_obrazu_vyska)
        obrazek_id = canvas_obrazek.create_image((rozmer_obrazu_sirka / 2), (rozmer_obrazu_vyska / 2), image=foto, anchor=kotva)

    # Uchováme nový obrázek, aby nevypršel odkaz
    canvas_obrazek.image = foto

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
        obrazek = sitk.ReadImage(r"obrazky_GUI\mozek_default_ikona.png")
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

# Funkce, která spouští kreslení detekčního polynomu při manuální detekci
def manualni_detekce():
    # Funkce si zjistí, jaký je současný stav spuštění manuální detekce a kolikrát byla spuštěna
    global pocet_spusteni_manualni_detekce
    global spusteni_manualni_detekce
    global uprava_polygonu
    global bod_v_polynomu
    global prvni_spusteni_manualni_detekce

    # Přičte se počet spuštění manuální detekce o 1
    pocet_spusteni_manualni_detekce = pocet_spusteni_manualni_detekce + 1

    # Pokud je zbytek po dělení počet spuštění manuální detekce 3 roven 1, tak se změní barva tlačítka a kreslení polynomu se umožní
    if (pocet_spusteni_manualni_detekce % 3) == 1:
        button_manual_detekce.config(bg="yellow")
        spusteni_manualni_detekce = True
        uprava_polygonu = False

    # Pokud je zbytek po dělení počet spuštění manuální detekce 3 roven 2, tak se změní barva tlačítka a úprava polynomu se umožní
    elif (pocet_spusteni_manualni_detekce % 3) == 2:
        button_manual_detekce.config(bg="orange")
        spusteni_manualni_detekce = True
        bod_v_polynomu = 0
        uprava_polygonu = True

    # Pokud je zbytek po dělení počet spuštění manuální detekce 3 roven 0, tak se změní barva tlačítka a kreslení polynomu a úprava polynomu se zakáže
    else:
        button_manual_detekce.config(bg="white")
        spusteni_manualni_detekce = False

# Funkce, která provádí kreslení detekčního polynomu při manuální detekci
def kresleni_polygonu(event):
    # Funkce si zjistí, jaký je současný stav spuštění manuální detekce, body detekčního
    # polynomu a zmáčknuté tlačítko na myši
    global spusteni_manualni_detekce
    global uprava_polygonu
    global body_polynomu
    global bod_v_polynomu
    global body_polynomu_ulozeni
    global pouzity_smer
    global predchozi_smer
    global predchozi_rez
    global index_ulozeni

    zmacnute_tlacitko = event.num

    # Provádí se kontrola, zda uživatel potvrdil, že chce provádět manuální detekci trombů
    if spusteni_manualni_detekce == True:
        # Pokud je manuální detekce spuštěna poprvé, tak si funkce zjistí směr a řez zobrazovaného obrázku
        if predchozi_smer == None or predchozi_rez == None:
            predchozi_smer = pouzity_smer
            predchozi_rez = slider.get()

        # Pokud se změní řez obrázku, tak se vykreslovaný detekční rámec smaže a nastaví se nový řez zobrazovaného obrázku
        elif predchozi_rez != slider.get():
            index_ulozeni = index_ulozeni + len(body_polynomu)
            body_polynomu = []
            predchozi_rez = slider.get()

        # Pokud se změní směr obrázku, tak se vykreslovaný detekční rámec smaže a nastaví se nový směr zobrazovaného obrázku
        elif predchozi_smer != pouzity_smer:
            index_ulozeni = index_ulozeni + len(body_polynomu)
            body_polynomu = []
            predchozi_smer = pouzity_smer

        # Pokud je vstupní hodnota False, znamená to, že chce uživatel vytvořit detekční polynom
        if uprava_polygonu == False:
            # Pokud bylo zmáčknuto levé tlačítko, tak se přidá bod k detekčnímu polynomu a souřadnice se uloží i do seznamu ukládaných souřadnic
            if zmacnute_tlacitko == 1:
                body_polynomu.append((event.x, event.y))
                body_polynomu_ulozeni.append((event.x, event.y, pouzity_smer, slider.get()))

            # Pokud bylo zmáčknuto pravé tlačítko, tak se odebere bod z detekčního polynomu
            elif zmacnute_tlacitko == 3:
                body_polynomu.pop()
                body_polynomu_ulozeni.pop()

            # Smaže se původní polynom
            canvas_obrazek.delete("polynom")

            # Pokud seznam bodů obsahuje alespoň 2 body, tak se vytvoří detekční polynom
            if len(body_polynomu) > 1:
                canvas_obrazek.create_polygon(body_polynomu, fill="", outline="orange", width=2, tags="polynom")

            # Smaže se původní body ve vrcholech polynomu
            canvas_obrazek.delete("body_polynomu")

            # For cyklus, kde v každém vrcholu detekčního polynomu se vytvoří kulatý bod
            for x, y in body_polynomu:
                canvas_obrazek.create_oval(x-2, y-2, x+2, y+2, fill="orange", tags="body_polynomu")

        # Pokud je vstupní hodnota True, znamená to, že chce uživatel upravovat detekční polynom
        else:
            # Zjistí se pocet bodů v polynomu
            delka_polynomu = len(body_polynomu)

            # Pokud bylo zmáčknuto levé tlačítko, tak se upraví bod v detekčním polynomu
            if zmacnute_tlacitko == 1:
                index_zmeny = bod_v_polynomu % delka_polynomu

                # Zjistí se nové souřadnice a ty se vloží na správné místo do seznamu souřadnic bodů
                zmenene_souradnice = (event.x, event.y)
                body_polynomu[index_zmeny] = zmenene_souradnice

                # Nové souřadnice se upraví a zapíšou do seznamu ukládaných souřadnic
                zmena_ulozeni = zmenene_souradnice + (pouzity_smer, ) + (slider.get(),)
                body_polynomu_ulozeni[index_ulozeni + index_zmeny] = zmena_ulozeni

            # Pokud bylo zmáčknuto pravé tlačítko, tak se odebere bod z detekčního polynomu
            elif zmacnute_tlacitko == 3:
                body_polynomu.pop()
                body_polynomu_ulozeni.pop()

            # Smaže se původní polynom
            canvas_obrazek.delete("polynom")

            # Pokud seznam bodů obsahuje alespoň 2 body, tak se vytvoří detekční polynom
            if len(body_polynomu) > 1:
                canvas_obrazek.create_polygon(body_polynomu, fill="", outline="orange", width=2, tags="polynom")

            # Smaže se původní body ve vrcholech polynomu
            canvas_obrazek.delete("body_polynomu")

            # For cyklus, kde v každém vrcholu detekčního polynomu se vytvoří kulatý bod a v současném bodě se vytvoří větší bod, aby uživatel veděl, s jakým bodem pracuje
            for index in range(0, len(body_polynomu)):
                if index == index_zmeny:
                    canvas_obrazek.create_oval(body_polynomu[index_zmeny][0] - 5, body_polynomu[index_zmeny][1] - 5,
                                               body_polynomu[index_zmeny][0] + 5, body_polynomu[index_zmeny][1] + 5,
                                               fill="yellow", tags="body_polynomu")
                else:
                    canvas_obrazek.create_oval(body_polynomu[index][0] - 2, body_polynomu[index][1] - 2,
                                               body_polynomu[index][0] + 2, body_polynomu[index][1] + 2, fill="orange",
                                               tags="body_polynomu")

            # Počítadlo se zvedne o 1
            bod_v_polynomu = bod_v_polynomu + 1

# Funkce, která ukládá detekční rámec do CSV souboru
def ulozit_manualni_detekci():
    # Funkce si načte vytvořený seznam se souřadnicemi detekčního rámce
    global body_polynomu_ulozeni

    # Načte se obrázek, se kterým uživatel pracuje a zjistíme jeho metadata
    obrazek = sitk.ReadImage("upload_image.nii")
    metadata_obrazu = obrazek.GetMetaDataKeys()

    # Vytvoří se průzkumník souborů, který uživateli umožní vyhledat místo uložení souboru
    cesta_k_ulozene_manual_detekci = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV soubor", "*.csv"), ("Všechny soubory", "*.*")])

    # Spustí se tvorba CSV souboru
    with open(cesta_k_ulozene_manual_detekci, mode="w", newline="") as data:
        writer = csv.writer(data)

        # For cyklem se do nově vytvářeného CSV souboru uloží název a hodnota dané metadata
        for index_metadat in range(0, len(metadata_obrazu)):
            nazev_metadata = metadata_obrazu[index_metadat]
            hodnota_metadata = obrazek.GetMetaData(key=nazev_metadata)

            writer.writerow([f"{nazev_metadata}: ", hodnota_metadata])

        # Vytvoří se mezera v CSV souboru, aby byl přehlednější
        writer.writerow("")
        writer.writerow("")

        # Do CSV souboru se zapíšou údaje o obraze
        writer.writerow(["Size: ", obrazek.GetSize()])
        writer.writerow(["Spacing: ", obrazek.GetSpacing()])
        writer.writerow(["Direction: ", obrazek.GetDirection()])
        writer.writerow(["Origin: ", obrazek.GetOrigin()])
        writer.writerow(["PixelID: ", obrazek.GetPixelID()])
        writer.writerow(["PixelIDTypeAsString: ", obrazek.GetPixelIDTypeAsString()])
        writer.writerow(["Depth: ", obrazek.GetDepth()])
        writer.writerow(["Dimension: ", obrazek.GetDimension()])
        writer.writerow(["Height: ", obrazek.GetHeight()])
        writer.writerow(["ITKBase: ", obrazek.GetITKBase()])
        writer.writerow(["NumberOfComponentsPerPixel: ", obrazek.GetNumberOfComponentsPerPixel()])
        writer.writerow(["NumberOfPixels: ", obrazek.GetNumberOfPixels()])
        writer.writerow(["PixelIDValue: ", obrazek.GetPixelIDValue()])
        writer.writerow(["SizeOfPixelComponent: ", obrazek.GetSizeOfPixelComponent()])
        writer.writerow(["Width: ", obrazek.GetWidth()])

        # Vytvoří se mezera v CSV souboru, aby byl přehlednější
        writer.writerow("")
        writer.writerow("")

        # Nakonec se do CSV souboru zapíšou souřadnice vrcholů detekčního rámce (1 řádek = 1 bod)
        writer.writerow(["X [px]", "Y [px]", "direction", "slice"])
        writer.writerows(body_polynomu_ulozeni)

        # Zavolá se funkce, která uživateli oznámí, že ukládání bylo dokončeno
        odpoved_po_ulozeni(False)

# Funkce, která sleduje pohyb myši po obrázku a vypisuje uživateli její pozici
def sledovani_mysi_na_obrazu(event):
    # Funkce si zjistí, jakou anatomickou rovinu uživatel teď používá a zda je zobrazen defaultní obrázek
    global pouzity_smer
    global ikona_mozku

    # Načte se zpracovávaný obraz a zjistí se jeho spacing (fyzické rozměry voxelů)
    obrazek = sitk.ReadImage("upload_image.nii")
    spacing_obrazu = obrazek.GetSpacing()

    # Funkce si zjistí, na jakých souřadnicích se teď nachází kurzor myši
    souradnice_x, souradnice_y = event.x, event.y

    # Pokud je hodnota proměnné False, znamená to, že uživatel pracuje se skutečným obrazem (ne s defaultním obrázkem)
    if ikona_mozku == False:
        # Podle toho, s jakou anatomickou rovinou uživatel pracuje, se upraví souřadnice pixelu vynásobením příslušným spacingem
        if pouzity_smer == "A":
            souradnice_x_upravena = round(souradnice_x * spacing_obrazu[0], 1)
            souradnice_y_upravena = round(souradnice_y * spacing_obrazu[1], 1)
        else:
            souradnice_x_upravena = round(souradnice_x * spacing_obrazu[0], 1)
            souradnice_y_upravena = round(souradnice_y * spacing_obrazu[2], 1)

        # Informační text se upraví podle nových souřadnic
        text_pozice_kurzoru_X.config(text=f"souřadnice X: {souradnice_x_upravena} mm")
        text_pozice_kurzoru_Y.config(text=f"souřadnice Y: {souradnice_y_upravena} mm")

    # Pokud je hodnota proměnné True, znamená to, že uživatel pracuje s defaultním obrázkem
    else:
        # Souřadnice není potřeba nijak upravovat, protože pixely v defaultním obrázku nemají fyzické rozměry
        souradnice_x_upravena = round(souradnice_x, 1)
        souradnice_y_upravena = round(souradnice_y, 1)

        # Informační text se upraví podle nových souřadnic
        text_pozice_kurzoru_X.config(text=f"souřadnice X: {souradnice_x_upravena} px")
        text_pozice_kurzoru_Y.config(text=f"souřadnice Y: {souradnice_y_upravena} px")

# Funkce, která přepíše uložený upravený obrázek (multifázický obraz, registrovaný obraz, atd.) na obraz, který se bude zobrazovat v GUI
# Funkce se bude ještě doplňovat
def zobraz_upraveny_obraz(zmeneny_obraz):
    # Zobrazí se jen ten upravený obraz, který si uživatel přeje
    if zmeneny_obraz == "M":
        # Načte se uložený multifázický obraz
        obrazek_upraveny = sitk.ReadImage("multiphase_image.nii")

    elif zmeneny_obraz == "R":
        # Načte se uložený registrovaný obraz (jakákoliv fáze)
        obrazek_upraveny = sitk.ReadImage("registered_image.nii")

    elif zmeneny_obraz == "O":
        # Načte se uložený obraz s CT oknem
        obrazek_upraveny = sitk.ReadImage("CT_window_image.nii")

    elif zmeneny_obraz == "N":
        # Načte se uložený nativní obraz
        obrazek_upraveny = sitk.ReadImage("nativ_image.nii")

    elif zmeneny_obraz == "1":
        # Načte se uložený CTA1 obraz
        obrazek_upraveny = sitk.ReadImage("CTA1_image.nii")

    elif zmeneny_obraz == "2":
        # Načte se uložený CTA2 obraz
        obrazek_upraveny = sitk.ReadImage("CTA2_image.nii")

    elif zmeneny_obraz == "3":
        # Načte se uložený CTA3 obraz
        obrazek_upraveny = sitk.ReadImage("CTA3_image.nii")

    else:
        # Načte se uložený registrovaný obraz
        obrazek_upraveny = sitk.ReadImage("upload_image.nii")
        # Ještě je nutné dodělat

    # Načtený upravený obraz se přepíše (uloží) jako "upload_image.nii", se kterým poté budou pracovat ostatní funkce v GUI
    sitk.WriteImage(obrazek_upraveny, "upload_image.nii")

    # Zavolá se funkce pro zobrazení obrazení obrazu v GUI
    zobraz_obrazek(True)

# Funkce, která se před uzavřením programu zeptá uživatele, zda chce ponechat uložené obrazy v aplikaci nebo zda je chce vymazat
# Funkce, mazání je dočasně vypnutá -> před odevzdáním ji je nutné zapnout (1. "N" -> "A")
def pred_uzavrenim_aplikace_dotaz():
    # Základní nastavení dotazového okna (font tlačítek, rozměry pomocného okna a nadpis)
    okno_pred_uzavrenim = tk.Tk()
    okno_pred_uzavrenim.title("Vymazat obrazy z paměti aplikace")
    okno_pred_uzavrenim.geometry("450x160")
    kotva = "center"
    font_tlacitek = ("Arial", 12, "bold")
    sticky_parametr_sloupec = "ew"
    odsazeni = 5

    # Vytvoření a umístění nadpisu do dotazového okna
    okno_uzavreni_text = tk.Label(okno_pred_uzavrenim, text="Přejete si před vypnutím aplikace vymazat obrazy z její paměti?", anchor=kotva, font=("Arial", 12))
    okno_uzavreni_text.grid(row=0, column=0, columnspan=3, sticky=sticky_parametr_sloupec, padx=odsazeni)

    mezera = tk.Label(okno_pred_uzavrenim, padx=odsazeni)
    mezera.grid(row=1, column=0, columnspan=3, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění textového upozornění do dotazového okna
    okno_uzavreni_text_upozorneni = tk.Label(okno_pred_uzavrenim, text="Upozornění: Pokud potvrdíte smazání obrazů z aplikace, vymažou se jak nahrané obrazy do aplikace, tak i ty, které jste v aplikaci upravovanovali (např.: aplikací CT okna nebo tvorbou registrovaného obrazu).", wraplength=450, justify="left")
    okno_uzavreni_text_upozorneni.grid(row=2, column=0, columnspan=3, padx=odsazeni, sticky=sticky_parametr_sloupec)

    mezera = tk.Label(okno_pred_uzavrenim, padx=odsazeni)
    mezera.grid(row=3, column=0, columnspan=3, sticky=sticky_parametr_sloupec)

    # Tlačítko pro vymazání obrazů z paměti programu a uzavření aplikace
    tlacitko_smazat_pamet = tk.Button(okno_pred_uzavrenim, text="Ano, smazat", anchor=kotva, font=font_tlacitek, command=lambda: (pred_uzavrenim_aplikace("A"), okno_pred_uzavrenim.destroy()))
    tlacitko_smazat_pamet.grid(row=4, column=0, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)

    # Tlačítko pro ponechání obrazů v paměti programu a provede se jen uzavření aplikace
    tlacitko_zachovat_pamet = tk.Button(okno_pred_uzavrenim, text="Ne, zachovat", anchor=kotva, font=font_tlacitek, command=lambda: (pred_uzavrenim_aplikace("N"), okno_pred_uzavrenim.destroy()))
    tlacitko_zachovat_pamet.grid(row=4, column=1, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)

    # Tlačítko pro setrvání v programu
    tlacitko_zrusit = tk.Button(okno_pred_uzavrenim, text="Zrušit", anchor=kotva, font=font_tlacitek, command=lambda: (pred_uzavrenim_aplikace("Z"), okno_pred_uzavrenim.destroy()))
    tlacitko_zrusit.grid(row=4, column=2, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)

    # Hlavní smyčka dotazového okna
    okno_pred_uzavrenim.mainloop()

# Funkce, která provádí vymazání uložených obrazů a následnému uzavření programu
# Funkce se bude ještě doplňovat
def pred_uzavrenim_aplikace(povel_uzavreni):

    if povel_uzavreni == "A":
        # Pokud je vstupní proměnná "A", tak se funkce pokusí vymazat postupně všechny uložené obrazy v paměti programu a poté zavře celý program
        try:
            os.remove("puvodni_ct_obrazek.nii")
        except:
            pass
        try:
            os.remove("upload_image.nii")
        except:
            pass
        try:
            os.remove("multiphase_image.nii")
        except:
            pass
        try:
            os.remove("CT_window_image.nii")
        except:
            pass
        try:
            os.remove("nativ_image.nii")
        except:
            pass
        try:
            os.remove("CTA1_image.nii")
        except:
            pass
        try:
            os.remove("CTA2_image.nii")
        except:
            pass
        try:
            os.remove("CTA3_image.nii")
        except:
            pass
        try:
            os.remove("registered_image.nii")
        except:
            pass

        okno.destroy()

    elif povel_uzavreni == "N":
        # Pokud je vstupní proměnná "N", tak funkce pouze ukončí běh programu
        okno.destroy()

    else:
        # Pokud je vstupní proměnná "Z", tak funkce nic neudělá a program dál běží
        pass

# Funkce, která přepíná obrazy podle výběru uživatele
def zmen_obrazek(vybrany_obrazek):
    # Pokud je vstupní proměnná "N", tak to znamená, že uživatel chce zobrazit nativní snímek
    if vybrany_obrazek == "N":
        # Změní se nastavení přepínacích tlačítek tak, aby uživatel věděl, které obrázek si vybral
        button_nativ.config(bg="yellow")
        button_CTA1.config(bg=barva_pozadi_tlacitka)
        button_CTA2.config(bg=barva_pozadi_tlacitka)
        button_CTA3.config(bg=barva_pozadi_tlacitka)
        button_multi.config(bg=barva_pozadi_tlacitka)

        # Funkce se pokusí načíst příslušný obrázek. Pokud se to nepodaří, funkce zavolá jinou funkci pro načítání obrazů
        try:
            zobraz_upraveny_obraz("N")
        except:
            nacist_obrazek("N")

    # Pokud je vstupní proměnná "1", tak to znamená, že uživatel chce zobrazit CTA1 snímek
    elif vybrany_obrazek == "1":
        # Změní se nastavení přepínacích tlačítek tak, aby uživatel věděl, které obrázek si vybral
        button_nativ.config(bg=barva_pozadi_tlacitka)
        button_CTA1.config(bg="yellow")
        button_CTA2.config(bg=barva_pozadi_tlacitka)
        button_CTA3.config(bg=barva_pozadi_tlacitka)
        button_multi.config(bg=barva_pozadi_tlacitka)

        # Funkce se pokusí načíst příslušný obrázek. Pokud se to nepodaří, funkce zavolá jinou funkci pro načítání obrazů
        try:
            zobraz_upraveny_obraz("1")
        except:
            nacist_obrazek("1")

    # Pokud je vstupní proměnná "2", tak to znamená, že uživatel chce zobrazit CTA2 snímek
    elif vybrany_obrazek == "2":
        # Změní se nastavení přepínacích tlačítek tak, aby uživatel věděl, které obrázek si vybral
        button_nativ.config(bg=barva_pozadi_tlacitka)
        button_CTA1.config(bg=barva_pozadi_tlacitka)
        button_CTA2.config(bg="yellow")
        button_CTA3.config(bg=barva_pozadi_tlacitka)
        button_multi.config(bg=barva_pozadi_tlacitka)

        # Funkce se pokusí načíst příslušný obrázek. Pokud se to nepodaří, funkce zavolá jinou funkci pro načítání obrazů
        try:
            zobraz_upraveny_obraz("2")
        except:
            nacist_obrazek("2")

    # Pokud je vstupní proměnná "3", tak to znamená, že uživatel chce zobrazit CTA3 snímek
    elif vybrany_obrazek == "3":
        # Změní se nastavení přepínacích tlačítek tak, aby uživatel věděl, které obrázek si vybral
        button_nativ.config(bg=barva_pozadi_tlacitka)
        button_CTA1.config(bg=barva_pozadi_tlacitka)
        button_CTA2.config(bg=barva_pozadi_tlacitka)
        button_CTA3.config(bg="yellow")
        button_multi.config(bg=barva_pozadi_tlacitka)

        # Funkce se pokusí načíst příslušný obrázek. Pokud se to nepodaří, funkce zavolá jinou funkci pro načítání obrazů
        try:
            zobraz_upraveny_obraz("3")
        except:
            nacist_obrazek("3")

    # Pokud je vstupní proměnná "M", tak to znamená, že uživatel chce zobrazit multifázický snímek
    elif vybrany_obrazek == "M":
        # Změní se nastavení přepínacích tlačítek tak, aby uživatel věděl, které obrázek si vybral
        button_nativ.config(bg=barva_pozadi_tlacitka)
        button_CTA1.config(bg=barva_pozadi_tlacitka)
        button_CTA2.config(bg=barva_pozadi_tlacitka)
        button_CTA3.config(bg=barva_pozadi_tlacitka)
        button_multi.config(bg="yellow")

        # Funkce se pokusí načíst příslušný obrázek. Pokud se to nepodaří, funkce zavolá jinou funkci pro načítání obrazů
        try:
            zobraz_upraveny_obraz("M")
        except:
            vyber_multifazi()

    # Pokud je vstupní proměnná odlišná, tak to znamená, že si uživatel nepřeje zobrazit žádný obrázek z vybrané nabítky
    else:
        # Změní se nastavení přepínacích tlačítek tak, aby uživatel věděl, které obrázek si vybral
        button_nativ.config(bg=barva_pozadi_tlacitka)
        button_CTA1.config(bg=barva_pozadi_tlacitka)
        button_CTA2.config(bg=barva_pozadi_tlacitka)
        button_CTA3.config(bg=barva_pozadi_tlacitka)
        button_multi.config(bg=barva_pozadi_tlacitka)


# Vytvoření hlavního okna
okno = tk.Tk()

# Nastavení velikosti okna podle obrazovky a anatomické rovina na axiální (využívá se nejvíce)
okno.state("zoomed")
okno.config(bg="white")
sirka_okna = okno.winfo_screenwidth()
vyska_okna = okno.winfo_screenheight()
pouzity_smer = "S"


# Nastavení Frame containeru pro vytvoření barevných pruhů na pozadí
kontejner = tk.Frame(okno, bg="lightblue")
kontejner_2 = tk.Frame(okno, bg="lightblue")
kontejner_3 = tk.Frame(okno, bg="lightblue")
kontejner_4 = tk.Frame(okno, bg="lightblue")
kontejner.grid(row=0, column=0, sticky="nsew", columnspan=14, rowspan=2)
kontejner_2.grid(row=1, column=0, sticky="nsew", rowspan=18)
kontejner_3.grid(row=19, column=0, sticky="nsew", columnspan=14)
kontejner_4.grid(row=3, column=12, sticky="nsew", rowspan=5)


# Parametry použité pro nastavení tabulky grid() a běhu programu
odsazeni = 5
odsazeni_mezera = 20
sticky_parametr_sloupec = "ew"
barva_okraju = "lightblue"
kotva = "center"
pocet_spusteni = 0
pocet_spusteni_manualni_detekce = 0
barva_pozadi_tlacitka = "white"
spusteni_manualni_detekce = False
body_polynomu = []
body_polynomu_ulozeni = []
predchozi_smer = None
predchozi_rez = None
index_ulozeni = 0
ikona_mozku = True
pocatecni_smer_axial = True
zavreni_aplikace = False
uprava_polygonu = False
bod_v_polynomu = 0


# For cykly vytvářející prvotní strukturu tabulky grid() pro GUI
for index_sloupce in range(0, 13):
    okno.columnconfigure(index_sloupce, weight=1)
for index_radku in range(3, 18):
    okno.rowconfigure(index_radku, weight=1)

# Vytvoření nadpisu okna a nastavení fontu tlačítek
okno.title("Bolehlav - aplikace pro detekce trombů v CT snímcích mozku")
font_tlacitek = ("Arial", 10, "bold")


# Vytvoření a umístění posuvníku
slider = tk.Scale(okno, from_=0, to=(zjisti_pocet_rezu() - 1), orient="horizontal", command=upravit_rez)
slider.grid(row=18, column=4, columnspan=6, sticky=sticky_parametr_sloupec)

# Vytovření a umístění tlačítek pro přepínání předchozího a následujícího řezu
tlacitko_predchozi = tk.Button(text="<", font=font_tlacitek, command=lambda: (posun_vlevo_vpravo(False)))
tlacitko_predchozi.grid(row=18, column=3, sticky="e", padx=odsazeni)
tlacitko_dalsi = tk.Button(text=">", font=font_tlacitek, command=lambda: (posun_vlevo_vpravo(True)))
tlacitko_dalsi.grid(row=18, column=10, sticky="w", padx=odsazeni)


# Defaultní obrázek
default_obrazek = Image.open(r"obrazky_GUI\mozek_default_ikona.png")
rozmer_obrazu_vyska = min(sirka_okna, vyska_okna) - round(((min(sirka_okna, vyska_okna) / 8) * 2.35))
rozmer_obrazu_sirka = max(sirka_okna, vyska_okna) - round((max(sirka_okna, vyska_okna) / 3.03))

# Změna velikosti defaultního obrázku podle velikosti uživatelova okna
default_obrazek = default_obrazek.resize((rozmer_obrazu_sirka, rozmer_obrazu_vyska))
foto = ImageTk.PhotoImage(default_obrazek)

# Umístění defaultního obrázku do GUI
canvas_obrazek = tk.Canvas(okno, width=rozmer_obrazu_sirka, height=rozmer_obrazu_vyska, cursor="tcross", bg="white")
canvas_obrazek.grid(row=2, column=3, columnspan=8, rowspan=16)
obrazek_id = canvas_obrazek.create_image((rozmer_obrazu_sirka / 2), (rozmer_obrazu_vyska / 2), image=foto, anchor=kotva)

# Uchováme nový obrázek, aby nevypršel odkaz
canvas_obrazek.image = foto

# Nastavení slideru na nulu
slider.config(to=0)

# Kontrolní tlačítka
# Tlačítka pro ovládání programu (Načíst, Uložit, Smazat a Zobrazit obraz)
button_nacti = tk.Button(okno, text="Načíst", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (nacist_obrazek("X")))
button_nacti.grid(row=0, column=1, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_uloz = tk.Button(okno, text="Uložit", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=uloz_soubor)
button_uloz.grid(row=0, column=2, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_smazat = tk.Button(okno, text="Smazat", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("X"), zobraz_obrazek(False)))
button_smazat.grid(row=0, column=3, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("X"), zobraz_obrazek(True)))
button_zobraz.grid(row=1, column=1, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=4, sticky=sticky_parametr_sloupec)


# Tlačítka pro úpravu obrazu (Registrace, Časová projekce maximální intenzity, manuální a automatická detekce a Zobraz výsledky)
button_registrace = tk.Button(okno, text="Registrace", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=vyber_registraci)
button_registrace.grid(row=0, column=5, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_multifaze = tk.Button(okno, text="Časová projekce", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=vyber_multifazi)
button_multifaze.grid(row=0, column=6, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_manual_detekce = tk.Button(okno, text="Manuální detekce", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=manualni_detekce)
button_manual_detekce.grid(row=0, column=7, columnspan=2, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("X"), zobraz_upraveny_obraz("R")))
button_zobraz.grid(row=1, column=5, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)
button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("X"), zobraz_upraveny_obraz("M")))
button_zobraz.grid(row=1, column=6, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

# Tlačítko pro smazání a uložení detekčního polynomu při manuální detekci trombů
button_smazat_manualni_detekci = tk.Button(okno, text="Smazat", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (canvas_obrazek.delete("polynom"), canvas_obrazek.delete("body_polynomu"), body_polynomu.clear(), body_polynomu_ulozeni.clear()))
button_smazat_manualni_detekci.grid(row=1, column=7, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)
button_uloz_manualni_detekci = tk.Button(okno, text="Uložit", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=ulozit_manualni_detekci)
button_uloz_manualni_detekci.grid(row=1, column=8, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=9, sticky=sticky_parametr_sloupec)


# Tlačítko pro postrocessing (nastavení požadovaného CT okna a zobrazení výsledného CT okna)
button_okno = tk.Button(okno, text="CT okno", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (vyber_CT_okna(pocet_spusteni), pocitadlo()))
button_okno.grid(row=0, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec)

button_zobraz = tk.Button(okno, text="Zobrazit", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("X"), zobraz_upraveny_obraz("O")))
button_zobraz.grid(row=1, column=10, padx=odsazeni, sticky=sticky_parametr_sloupec, pady=odsazeni)

mezera = tk.Label(okno, padx=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=0, column=11, sticky=sticky_parametr_sloupec)


# Tlačítko s nápovědou k GUI
button_napoveda = tk.Button(okno, text="Nápověda", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=napoveda)
button_napoveda.grid(row=0, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)


# Tlačítka pro přepínání různých obrazů
button_nativ = tk.Button(okno, text="Nativ", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("N")))
button_nativ.grid(row=3, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_CTA1 = tk.Button(okno, text="CTA1", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("1")))
button_CTA1.grid(row=4, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_CTA2 = tk.Button(okno, text="CTA2", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("2")))
button_CTA2.grid(row=5, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_CTA3 = tk.Button(okno, text="CTA3", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, command=lambda: (zmen_obrazek("3")))
button_CTA3.grid(row=6, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)
button_multi = tk.Button(okno, text="Časová projekce", anchor=kotva, font=font_tlacitek, bg=barva_pozadi_tlacitka, wraplength=80, command=lambda: (zmen_obrazek("M")))
button_multi.grid(row=7, column=12, padx=odsazeni, sticky=sticky_parametr_sloupec)


# Pomocný text pro lepší orientaci uživatele (zvolená anatomická rovina, pozice kurzoru (X, Y) a aktuální řez obrazem)
mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=2, column=0, sticky="ns")

nadpis_rovina = tk.Label(okno, text="Zvolená anatomická rovina:", pady=odsazeni, bg=barva_okraju)
nadpis_rovina.grid(row=19, column=0, sticky=sticky_parametr_sloupec)
text_rovina = tk.Label(okno, text="Sagitální", pady=odsazeni, bg="lightblue")
text_rovina.grid(row=19, column=1, sticky=sticky_parametr_sloupec, ipadx=int(math.floor(sirka_okna / 100)))

nadpis_pozice_kurzoru = tk.Label(okno, text="Pozice kurzoru:" , pady=odsazeni, bg=barva_okraju)
nadpis_pozice_kurzoru.grid(row=19, column=5, sticky=sticky_parametr_sloupec)
text_pozice_kurzoru_X = tk.Label(okno, text="souřadnice X", pady=odsazeni, bg=barva_okraju)
text_pozice_kurzoru_X.grid(row=19, column=6, sticky=sticky_parametr_sloupec)
text_pozice_kurzoru_Y = tk.Label(okno, text="souřadnice Y", pady=odsazeni, bg=barva_okraju)
text_pozice_kurzoru_Y.grid(row=19, column=7, columnspan=2, sticky=sticky_parametr_sloupec)

nadpis_aktualni_rez = tk.Label(okno, text="Aktuální řez:" , pady=odsazeni, bg=barva_okraju)
nadpis_aktualni_rez.grid(row=19, column=10, sticky=sticky_parametr_sloupec)
text_aktualni_rez = tk.Label(okno, text=0 , pady=odsazeni, bg=barva_okraju)
text_aktualni_rez.grid(row=19, column=11, sticky=sticky_parametr_sloupec)


# Počáteční nastavení velikostí tlačítek
velikost_obrazu_tlacitka = int(round(((vyska_okna / 4.84) + (sirka_okna / 7.75)) / 2) * 0.9)


# Počáteční nahrání obrázků do tlačítek pro výběr anatomické roviny
obrazek_axial = Image.open(r"obrazky_GUI\axial_tlacitko.png")
obrazek_axial_zmena = obrazek_axial.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_axial = ImageTk.PhotoImage(obrazek_axial_zmena)
obrazek_sagittal = Image.open(r"obrazky_GUI\sagittal_tlacitko.png")
obrazek_sagittal_zmena = obrazek_sagittal.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_sagittal = ImageTk.PhotoImage(obrazek_sagittal_zmena)
obrazek_coronal = Image.open(r"obrazky_GUI\coronal_tlacitko.png")
obrazek_coronal_zmena = obrazek_coronal.resize((velikost_obrazu_tlacitka, velikost_obrazu_tlacitka))  # Změna velikosti obrázku
foto_coronal = ImageTk.PhotoImage(obrazek_coronal_zmena)

# Tlačítka pro změnu anatomické roviny (axiální, sagitární a koronální roviny)
button_axial = tk.Button(okno, image=foto_axial, text="Axiální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("A"))
button_axial.grid(row=3, column=0, rowspan=5, pady=odsazeni)
button_sagittal = tk.Button(okno, image=foto_sagittal, text="Sagitální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("S"))
button_sagittal.grid(row=8, column=0, rowspan=5, pady=odsazeni)
button_coronal = tk.Button(okno, image=foto_coronal, text="Koronální rovina", compound="top", font=font_tlacitek, command=lambda: info_o_rovine("K"))
button_coronal.grid(row=13, column=0, rowspan=5, pady=odsazeni)

mezera = tk.Label(okno, pady=odsazeni_mezera, bg=barva_okraju)
mezera.grid(row=18, column=0, sticky=sticky_parametr_sloupec)


# Funkce pro volání funkcí, které upravují velikost obrázků v tlačítcích (automaticky)
button_axial.bind("<Configure>", uprava_velikosti_obrazku_axial)
button_sagittal.bind("<Configure>", uprava_velikosti_obrazku_sagittal)
button_coronal.bind("<Configure>", uprava_velikosti_obrazku_coronal)

# Funkce pro volání funkcí, které reagují na zmáčknutí šipek na klávesnici (automaticky)
okno.bind("<Left>", posun_vlevo_vpravo_klavesnice)
okno.bind("<Right>", posun_vlevo_vpravo_klavesnice)

# Funkce pro volání funkcí, které reagují na zmáčknutí tlačítek na myši (automaticky)
canvas_obrazek.bind("<Button-1>", kresleni_polygonu)
canvas_obrazek.bind("<Button-3>", kresleni_polygonu)

# Funkce pro volání funkce, která reaguje na pohyb myši po obrazovce (automaticky)
canvas_obrazek.bind("<Motion>", sledovani_mysi_na_obrazu)

# Funkce pro volání funkce, která reaguje až při pokusu o zavření programu (automaticky)
okno.protocol("WM_DELETE_WINDOW", pred_uzavrenim_aplikace_dotaz)

# Hlavní smyčka aplikace
okno.mainloop()
