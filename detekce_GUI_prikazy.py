# Knihovny potřebné pro chod pomocných příkazů pro GUI
import tkinter as tk
from tkinter import filedialog
import SimpleITK as sitk


# Blok kódu s funkcemi pro správný chod pomocných příkazů v GUI
# Funkce, jejíž funkcí je načtení obrazu ze složky do formátu SimpleITK
def nacti_obrazek(cesta):
    reader = sitk.ImageSeriesReader()
    slozka = reader.GetGDCMSeriesFileNames(cesta)
    reader.SetFileNames(slozka)

    obrazek = reader.Execute()

    return obrazek

# Funkce, která vytvoří pomocné okno, které uživateli umožní si zvolit, co chce nahrát do programu GUI
def nacist_obrazek(nadpis_obrazku):
    # Základní nastavení pomocného okna (font tlačítek, rozměry pomocného okna a nadpis)
    dotaz_okno = tk.Tk()
    dotaz_okno.geometry("400x100")
    font_tlacitek = ("Arial", 12, "bold")

    if nadpis_obrazku == "N":
        dotaz_okno.title("Načtení nativní obrazu")
    elif nadpis_obrazku == "1":
        dotaz_okno.title("Načtení CTA1 obrazu")
    elif nadpis_obrazku == "2":
        dotaz_okno.title("Načtení CTA2 obrazu")
    elif nadpis_obrazku == "3":
        dotaz_okno.title("Načtení CTA3 obrazu")
    else:
        dotaz_okno.title("Načtení obrazu")

    dotaz = tk.Label(dotaz_okno, text="Vyberte, zda chcete načíst obraz ve formátu DICOM nebo ve formátu NIfTI.")
    dotaz.pack()

    # Vytvoření a umístění tlačítek pro výběr typu souboru určeného pro nahrání do programu GUI
    tlacitko_soubor = tk.Button(dotaz_okno, text="DICOM", font=font_tlacitek, command=lambda: (dotaz_okno.destroy(), nacti_soubor(nadpis_obrazku)))
    tlacitko_soubor.pack(side="left", padx=30, anchor="center")
    tlacitko_slozka = tk.Button(dotaz_okno, text="NIfTI", font=font_tlacitek, command=lambda: (dotaz_okno.destroy(), nacti_slozku(nadpis_obrazku)))
    tlacitko_slozka.pack(side="right", padx=30, anchor="center")

    # Hlavní smyčka pomocného okna
    dotaz_okno.mainloop()

# Funkce, která umožňuje nahrání konkrétního souboru nalezeného pomocí průzkumníka souborů
def nacti_soubor(nadpis_obrazku):
    # Vytvoří se průzkumník souborů, který uživateli umožní vyhledat požadovaný soubor
    soubor = filedialog.askopenfilename(title="Vyber soubor", filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])

    # Nalezená cesta se upraví a použije pro nahrání obrazu pomocí knihovny SimpleITK
    cesta = soubor.replace("\\", "/")
    obrazek_nacteny = sitk.ReadImage(cesta)

    # Obraz se uloží do paměti GUI pod takovým názvem, který odpovídá výběru uživatele
    if nadpis_obrazku == "N":
        sitk.WriteImage(obrazek_nacteny, "nativ_image.nii")

    elif nadpis_obrazku == "1":
        sitk.WriteImage(obrazek_nacteny, "CTA1_image.nii")

    elif nadpis_obrazku == "2":
        sitk.WriteImage(obrazek_nacteny, "CTA2_image.nii")

    elif nadpis_obrazku == "3":
        sitk.WriteImage(obrazek_nacteny, "CTA3_image.nii")

    else:
        sitk.WriteImage(obrazek_nacteny, "upload_image.nii")

    # Zavolá se funkce, která uživateli oznámí, že nahrávání bylo dokončeno
    odpoved_po_nacteni()

# Funkce, která umožňuje nahrání konkrétní složky nalezené pomocí průzkumníka souborů
def nacti_slozku(nadpis_obrazku):
    # Vytvoří se průzkumník souborů, který uživateli umožní vyhledat požadovanou složku
    slozka = filedialog.askdirectory(title="Vyber složku")

    # Nalezená cesta se upraví a použije pro nahrání obrazu pomocí funkce "nacti_obrazek"
    cesta = slozka.replace("\\", "/")
    obrazek_nacteny = nacti_obrazek(cesta=cesta)

    # Obraz se uloží do paměti GUI pod takovým názvem, který odpovídá výběru uživatele
    if nadpis_obrazku == "N":
        sitk.WriteImage(obrazek_nacteny, "nativ_image.nii")

    elif nadpis_obrazku == "1":
        sitk.WriteImage(obrazek_nacteny, "CTA1_image.nii")

    elif nadpis_obrazku == "2":
        sitk.WriteImage(obrazek_nacteny, "CTA2_image.nii")

    elif nadpis_obrazku == "3":
        sitk.WriteImage(obrazek_nacteny, "CTA3_image.nii")

    else:
        sitk.WriteImage(obrazek_nacteny, "upload_image.nii")

    # Zavolá se funkce, která uživateli oznámí, že nahrávání bylo dokončeno
    odpoved_po_nacteni()

# Funkce, která vytváří oznamovací okno, že nahrávání proběhlo úspěšně
def odpoved_po_nacteni():
    # Základní nastavení oznamovacího okna (rozměry pomocného okna a nadpis)
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Nahrávání obrazu")
    dotaz_okno.geometry("300x50")

    # Vytvoření a umístění oznámení do oznamovacího okna
    dotaz = tk.Label(dotaz_okno, text="Obraz byl úspěšně načtený a uložený do paměti.", anchor="center")
    dotaz.pack()

# Funkce, která umožňuje uložení rozpracovaného obrazu pomocí průzkumníka souboru
def uloz_soubor():
    # Vytvoří se průzkumník souborů, který uživateli umožní vyhledat místo uložení souboru
    cesta_k_ulozenemu_souboru = filedialog.asksaveasfilename(defaultextension=".nii",
                                          filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])

    # Jakmile je cesta uživatelem potvrzena, tak se soubor uloží na dané místo
    if cesta_k_ulozenemu_souboru:
        obrazek = sitk.ReadImage("upload_image.nii")

        # Provede se kontrola, jestli si uživatel přeje uložit ve formátu .dcm (DICOM), .nii (NIfTI) nebo úplně v jiném formátu
        test_formatu = cesta_k_ulozenemu_souboru[-4:]

        # Podle požadovaného formátu uložení se buď obraz uloží přímo (u NIfTI souborů) nebo přes pomocný soubor, který je převed na požadovaný formát
        if test_formatu == ".nii":
            sitk.WriteImage(obrazek, cesta_k_ulozenemu_souboru)

        else:
            obrazek_pred_ulozeni = sitk.Cast(obrazek, sitk.sitkUInt16)
            sitk.WriteImage(obrazek_pred_ulozeni, f"upload_image{test_formatu}")
            obrazek_k_ulozeni = sitk.ReadImage(f"upload_image{test_formatu}")
            sitk.WriteImage(obrazek_k_ulozeni, cesta_k_ulozenemu_souboru)

        # Zavolá se funkce, která uživateli oznámí, že ukládání bylo dokončeno
        odpoved_po_ulozeni(True)

# Funkce, která vytváří oznamovací okno, že ukládání souboru proběhlo úspěšně
def odpoved_po_ulozeni(obraz):
    # Základní nastavení oznamovacího okna (rozměry pomocného okna)
    dotaz_okno = tk.Tk()
    dotaz_okno.geometry("300x50")

    # Pokud je vstupní proměnná True, tak to znamená, že se má uložit zobrazený obrázek
    if obraz == True:
        dotaz_okno.title("Uložení obrazu")
        dotaz = tk.Label(dotaz_okno, text="Obraz byl úspěšně uložený na vybrané místo.", anchor="center")

    # Pokud je vstupní proměnná False, tak to znamená, že se má uložit manuální detekce
    else:
        dotaz_okno.title("Uložení manuální detekce")
        dotaz = tk.Label(dotaz_okno, text="Manuální detekce byla úspěšně uložena.", anchor="center")

    # Vytvoření a umístění oznámení do oznamovacího okna
    dotaz.pack()
