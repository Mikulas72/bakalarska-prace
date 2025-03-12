# Knihovny potřebné pro chod postprocessingové aplikace CT okna
import tkinter as tk
import SimpleITK as sitk
import numpy as np


# Blok kódu s funkcemi pro správný chod postprocessingové aplikace CT okna
# Funkce, která umožní uživateli výběr požadovaného CT okna
def vyber_CT_okna(pocet_spusteni):
    # Vytvoření okna, které umožní uživateli výběr CT okna
    dotaz_ct_okno = tk.Tk()
    dotaz_ct_okno.title("Výběr CT okna")
    dotaz_ct_okno.geometry("450x200")
    font_tlacitek = ("Arial", 12, "bold")
    sticky_parametr_sloupec = "ew"
    odsazeni = 5
    kotva = "center"

    # Vytvoření nadpisu v okně
    nadpis = tk.Label(dotaz_ct_okno, text="Vyberte, jaké CT okno chcete aplikovat.", anchor=kotva, font=("Arial", 12))
    nadpis.grid(row=0, column=0, columnspan=3, sticky=sticky_parametr_sloupec, padx=odsazeni)

    mezera = tk.Label(dotaz_ct_okno, padx=odsazeni)
    mezera.grid(row=1, column=0, columnspan=3, sticky=sticky_parametr_sloupec)


    # Tlačítka pro výběr požadovaného mozkového okna
    tlacitko_mozkove_okno = tk.Button(dotaz_ct_okno, text="Mozkové okno", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("mozek", pocet_spusteni)))
    tlacitko_mozkove_okno.grid(row=2, column=0, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_kostni_okno = tk.Button(dotaz_ct_okno, text="Kostní okno", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("kost", pocet_spusteni)))
    tlacitko_kostni_okno.grid(row=2, column=1, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_subduralni_okno = tk.Button(dotaz_ct_okno, text="Subdurální okno", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("subdural", pocet_spusteni)))
    tlacitko_subduralni_okno.grid(row=2, column=2, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_mekotkanove_okno = tk.Button(dotaz_ct_okno, text="Měkkotkáňové okno", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("tkan", pocet_spusteni)))
    tlacitko_mekotkanove_okno.grid(row=3, column=0, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_krvaceni_okno = tk.Button(dotaz_ct_okno, text="Krvácení", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("krev", pocet_spusteni)))
    tlacitko_krvaceni_okno.grid(row=3, column=1, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_vlastni_okno = tk.Button(dotaz_ct_okno, text="Vlastní", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("vlastni", pocet_spusteni)))
    tlacitko_vlastni_okno.grid(row=3, column=2, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)

    mezera = tk.Label(dotaz_ct_okno, padx=odsazeni)
    mezera.grid(row=4, column=0, columnspan=3, sticky=sticky_parametr_sloupec)


    # Resetovací tlačítko (odstrani z obrazu všechny CT okna)
    tlacitko_reset = tk.Button(dotaz_ct_okno, text="Reset", anchor=kotva, font=font_tlacitek, command=lambda: (dotaz_ct_okno.destroy(), nastav_CT_okno("reset", pocet_spusteni)))
    tlacitko_reset.grid(row=5, column=1, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)

# Funkce, která podle výběru uživatele (jaké tlačítko zmáčkl) zvolí a aplikuje dané CT okno
def nastav_CT_okno(okno, pocet_spusteni):
    # Pokud je vyokňování spuštěno poprvé, tak se uloží kopie původního obrazu
    if pocet_spusteni == 0:
        obrazek_puvodni = sitk.ReadImage("upload_image.nii")
        sitk.WriteImage(obrazek_puvodni, "puvodni_ct_obrazek.nii")

    # Pokud bylo již vyoknění spuštěno, tak se vyvolá původní obraz, se kterým se bude pracovat
    else:
        obrazek_puvodni = sitk.ReadImage("puvodni_ct_obrazek.nii")

    # Převod na numpy pole
    obrazek_pole = sitk.GetArrayFromImage(obrazek_puvodni).astype(np.float32)

    # Pokud uživatel zvolil tlačítko "reset", tak se nahraje původní obrázek
    if okno =="reset":
        obrazek = sitk.ReadImage("puvodni_ct_obrazek.nii")

        sitk.WriteImage(obrazek, "upload_image.nii")
        # Zavolá se funkce, která uživateli oznámí, že došlo k resetu
        odpoved_po_uprave(True)

    # Podle zvoleného okna se nastaví střed okna a šířka okna
    else:
        if okno == "mozek":
            stred_okna = 40
            sirka_okna = 80
        elif okno == "kost":
            stred_okna = 1524
            sirka_okna = 3000
        elif okno == "subdural":
            stred_okna = 50
            sirka_okna = 300
        elif okno == "tkan":
            stred_okna = 40
            sirka_okna = 400
        elif okno == "krev":
            stred_okna = 75
            sirka_okna = 150
        else:
            # Pokud uživatel zvolí "vlastní" CT okno, tak se zavolá funkce, která provede jeho nastavení
            return dotaz_ct_okno_vlastni(pocet_spusteni)

        # Výpočet okrajů CT okna
        minimum = stred_okna - (sirka_okna / 2)
        maximum = stred_okna + (sirka_okna / 2)

        # Hodnoty mimo vymezené okno se nastaví na 0 nebo 1
        obrazek_pole = np.clip(obrazek_pole, minimum, maximum)
        # Normalizace rozsahu
        obrazek_pole = 255.0 * (obrazek_pole - minimum) / (maximum - minimum)

        # Převod na SimpleITK obraz a jeho uložení
        obrazek_zmeneny = sitk.GetImageFromArray(obrazek_pole)
        sitk.WriteImage(obrazek_zmeneny, "upload_image.nii")

        # Zavolá se funkce, která uživateli oznámí, že se CT okno aplikovalo
        return odpoved_po_uprave(False)

# Tato funkce vytvoří oznamovací okno, že byl na obraz aplikováno vybrané CT okno nebo že z něho bylo odstraněno
def odpoved_po_uprave(reset):
    # Vytvoření oznamovacího okna (nadpisu a rozměrů okna)
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Upravení obrazu")
    dotaz_okno.geometry("300x50")

    # Pokud byla vstupní hodnota False, znamená to, že si užýivatel přeje aplikovat na obraz CT okno a v oznamovacím okně se vypíše příslušné oznámení
    if reset == False:
        dotaz = tk.Label(dotaz_okno, text="Na obraz bylo úspěšně aplikováno vybrané CT okno.", anchor="center")

    # Pokud byla vstupní hodnota True, znamená to, že si užýivatel přeje odstranit z obrazu CT okno a v oznamovacím okně se vypíše příslušné oznámení
    else:
        dotaz = tk.Label(dotaz_okno, text="Z obrazu bylo úspěšně odebráno CT okno.", anchor="center")

    dotaz.pack()

# Tato funkce vytváří nabídkové okno, které uživateli umožní vložit vlastní parametry pro CT okno
def dotaz_ct_okno_vlastni(pocet_spusteni):
    # Základní parapetry a vytvoření nabídkového okno (nadpis, rozměry okna a parametry textu)
    dotaz_vlastni_ct_okno = tk.Tk()
    dotaz_vlastni_ct_okno.title("Vlastní CT okno")
    dotaz_vlastni_ct_okno.geometry("510x170")
    odsazeni = 5
    sticky_parametr_sloupec = "ew"
    var = tk.StringVar()
    var.set("A")

    # Vytvoření a umístění textu pro navedení uživatele
    nadpis = tk.Label(dotaz_vlastni_ct_okno, text="Nastavte si požadované parametry vlastního CT okna.", font=("Arial", 12))
    nadpis.grid(row=0, column=0, columnspan=5, sticky=sticky_parametr_sloupec, padx=odsazeni)

    mezera = tk.Label(dotaz_vlastni_ct_okno, padx=odsazeni)
    mezera.grid(row=1, column=0, columnspan=5, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění nadpisů a vstupů pro zadání středu a šířky vlastního CT okna
    popis_stred = tk.Label(dotaz_vlastni_ct_okno, text="Střed okna:")
    popis_stred.grid(row=2, column=0, sticky=sticky_parametr_sloupec)
    vstup_stred = tk.Entry(dotaz_vlastni_ct_okno, validate="key", validatecommand=(dotaz_vlastni_ct_okno.register(overeni_vstupu), "%P"))
    vstup_stred.grid(row=2, column=1, sticky=sticky_parametr_sloupec)
    popis_sirka = tk.Label(dotaz_vlastni_ct_okno, text="Šířka okna:")
    popis_sirka.grid(row=3, column=0, sticky=sticky_parametr_sloupec)
    vstup_sirka = tk.Entry(dotaz_vlastni_ct_okno, validate="key", validatecommand=(dotaz_vlastni_ct_okno.register(overeni_vstupu), "%P"))
    vstup_sirka.grid(row=3, column=1, sticky=sticky_parametr_sloupec)

    mezera = tk.Label(dotaz_vlastni_ct_okno, pady=5)
    mezera.grid(row=2, column=2, rowspan=3, sticky="sn")

    # Vytvoření a umístění nadpisů a vstupů pro zadání maxima a minima vlastního CT okna
    popis_max = tk.Label(dotaz_vlastni_ct_okno, text="Horní hranice okna:")
    popis_max.grid(row=2, column=3, sticky=sticky_parametr_sloupec)
    vstup_max = tk.Entry(dotaz_vlastni_ct_okno, validate="key", validatecommand=(dotaz_vlastni_ct_okno.register(overeni_vstupu), "%P"))
    vstup_max.grid(row=2, column=4, sticky=sticky_parametr_sloupec)
    popis_min = tk.Label(dotaz_vlastni_ct_okno, text="Spodní hranice okna:")
    popis_min.grid(row=3, column=3, sticky=sticky_parametr_sloupec)
    vstup_minimum = tk.Entry(dotaz_vlastni_ct_okno, validate="key", validatecommand=(dotaz_vlastni_ct_okno.register(overeni_vstupu), "%P"))
    vstup_minimum.grid(row=3, column=4, sticky=sticky_parametr_sloupec)

    mezera = tk.Label(dotaz_vlastni_ct_okno, padx=odsazeni)
    mezera.grid(row=4, column=0, columnspan=5, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění upozornění pro uživatele, že lze zadávat pouze číselné hodnoty
    text_upozorneni = tk.Label(dotaz_vlastni_ct_okno, text="Upozornění: Zadávejte pouze číselné hodnoty.")
    text_upozorneni.grid(row=5, column=0, columnspan=5, sticky=sticky_parametr_sloupec)

    # Tlačítka pro potvrzení zadaných údajů a tlačítko pro vymazání vstupů (kdyby si to uživatel rozmyslel)
    tlacitko_spustit_A = tk.Button(dotaz_vlastni_ct_okno, text="Použít šírku a výšku okna", font=("Arial", 10, "bold"), command=lambda: (zpracuj_vlastni_ct_okno(vstup_stred.get(), vstup_sirka.get(), "", "", True, pocet_spusteni), dotaz_vlastni_ct_okno.destroy()))
    tlacitko_spustit_A.grid(row=6, column=0, columnspan=2, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_spustit_B = tk.Button(dotaz_vlastni_ct_okno, text="Použít maximum a minimum okna", font=("Arial", 10, "bold"), command=lambda: (zpracuj_vlastni_ct_okno("", "", vstup_minimum.get(), vstup_max.get(), False, pocet_spusteni), dotaz_vlastni_ct_okno.destroy()))
    tlacitko_spustit_B.grid(row=6, column=3, columnspan=2, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)
    tlacitko_smazat = tk.Button(dotaz_vlastni_ct_okno, text="Smazat", font=("Arial", 10, "bold"), command=lambda: (vstup_stred.delete(0, tk.END), vstup_sirka.delete(0, tk.END), vstup_max.delete(0, tk.END), vstup_minimum.delete(0, tk.END)))
    tlacitko_smazat.grid(row=6, column=2, sticky=sticky_parametr_sloupec, padx=odsazeni, pady=odsazeni)

    # Hlavní smyčka nabídkového okna
    dotaz_vlastni_ct_okno.mainloop()

# Funkce aplikující zadané hodnoty uživatelem pro vlastní CT okno na daný obraz
def zpracuj_vlastni_ct_okno(stred, sirka, minimum, maximum, vyber, pocet_spusteni):
    # Podle počtu spuštění postprocessingu se vybere, zda se může pro úpravy využít současný obrázek nebo se musí vyvolat záloha
    # (Zabraňuje kumulativnímu použití CT oken na již upravené obrazy)
    if pocet_spusteni == 0:
        obrazek_puvodni = sitk.ReadImage("upload_image.nii")
    else:
        obrazek_puvodni = sitk.ReadImage("puvodni_ct_obrazek.nii")

    # Nahraný obraz se převede na numpy matici a nastaví se jeho datový typ
    obrazek_pole = sitk.GetArrayFromImage(obrazek_puvodni).astype(np.float32)

    # Pokud je vstupní hodnota True, tak to znamená, že si uživatel přeje nastavit CT okno podle středu okna a jeho šířky
    if vyber == True:
        stred = int(stred)
        sirka = int(sirka)
        minimum = stred - (sirka / 2)
        maximum = stred + (sirka / 2)

    # Pokud je vstupní hodnota False, tak to znamená, že si uživatel přeje nastavit CT okno podle maxima a minima
    else:
        maximum = int(maximum)
        minimum = int(minimum)

    # Obraz se ořízne (tedy nastaví se vlastní CT okno) a provede se normalizace
    obrazek_pole = np.clip(obrazek_pole, minimum, maximum)
    obrazek_pole = 255.0 * (obrazek_pole - minimum) / (maximum - minimum)

    # Obraz se převede zpět z numpy matice a uloží se do paměti GUI
    obrazek_zmeneny = sitk.GetImageFromArray(obrazek_pole)
    sitk.WriteImage(obrazek_zmeneny, "upload_image.nii")

    # Vypíše se upozornění pro uživatele, že postprocessingové úpravy byli dokončeny
    odpoved_po_uprave(False)

# Funke kontroluje, jaké vstupy zadává uživatel do vstupů pro parametry vlastního CT okna
def overeni_vstupu(text_vstup):
    # Pokud uživatel zadá číslo, pomlčku (mínus) nebo nezadá nic, tak funkce vstup povolí
    if text_vstup.isdigit() or text_vstup == "" or text_vstup == "-":
        return True

    # Pokud uživatel zadá záporné číslo, tak funkce vstup povolí
    elif text_vstup.lstrip("-").isdigit():
        return True

    # Pokud ale uživatel zadá něco jiného, tak funkce vstup zamítne
    else:
        return False
