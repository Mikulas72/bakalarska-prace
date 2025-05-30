# Knihovny potřebné pro vytváření multifázických obrazů pro GUI
import tkinter as tk
import SimpleITK as sitk
from tkinter import filedialog
import os



# Blok kódu s funkcemi pro správné vytváření multifázických obrazů v GUI
# Funkce, která umožní uživateli vložit cesty k obrazům, ze kterých chce vytvořit multifázický obraz
def vyber_multifazi():
    # Vytvoření okna, které umožní uživateli vložit cesty k obrazům
    dotaz_multifaze_okno = tk.Tk()
    dotaz_multifaze_okno.title("Vytvoření multifázického obrazu")
    dotaz_multifaze_okno.geometry("430x190")
    font_tlacitek = ("Arial", 12, "bold")
    sticky_parametr_sloupec = "ew"
    odsazeni = 5
    kotva = "center"

    # Vytvoření nadpisu v okně
    nadpis = tk.Label(dotaz_multifaze_okno, text="Vyberte, z jakých obrazů chcete vytvořit multifázický obraz.", anchor=kotva, font=("Arial", 12))
    nadpis.grid(row=0, column=0, columnspan=8, sticky=sticky_parametr_sloupec)

    mezera = tk.Label(dotaz_multifaze_okno, padx=odsazeni)
    mezera.grid(row=1, column=0, columnspan=8, sticky=sticky_parametr_sloupec)


    # Popisky k vstupům, aby uživatel věděl, který vstup patří ke kterému obrazu
    popis_CTA1 = tk.Label(dotaz_multifaze_okno, text="CTA1 obraz:")
    popis_CTA1.grid(row=2, column=0, sticky=sticky_parametr_sloupec)
    popis_CTA2 = tk.Label(dotaz_multifaze_okno, text="CTA2 obraz:")
    popis_CTA2.grid(row=3, column=0, sticky=sticky_parametr_sloupec)
    popis_CTA3 = tk.Label(dotaz_multifaze_okno, text="CTA3 obraz:")
    popis_CTA3.grid(row=4, column=0, sticky=sticky_parametr_sloupec)


    # Vstupní pole pro zadání cesty k obrazům
    vstup_CTA1 = tk.Entry(dotaz_multifaze_okno)
    vstup_CTA1.grid(row=2, column=1, columnspan=5, sticky=sticky_parametr_sloupec)
    vstup_CTA2 = tk.Entry(dotaz_multifaze_okno)
    vstup_CTA2.grid(row=3, column=1, columnspan=5, sticky=sticky_parametr_sloupec)
    vstup_CTA3 = tk.Entry(dotaz_multifaze_okno)
    vstup_CTA3.grid(row=4, column=1, columnspan=5, sticky=sticky_parametr_sloupec)


    # Tlačitka, která vloží aktuální obraz (v paměti aplikace) (tedy cestu k němu) do vstupního pole
    tlacitko_vlozit_CTA1 = tk.Button(dotaz_multifaze_okno, text="Aktuální obraz", command=lambda: (
    vstup_CTA1.delete(0, tk.END), vstup_CTA1.insert(0, hledej_cestu_k_obrazu(False))))
    tlacitko_vlozit_CTA1.grid(row=2, column=6, padx=odsazeni, pady=1)
    tlacitko_vlozit_CTA2 = tk.Button(dotaz_multifaze_okno, text="Aktuální obraz", command=lambda: (
    vstup_CTA2.delete(0, tk.END), vstup_CTA2.insert(0, hledej_cestu_k_obrazu(False))))
    tlacitko_vlozit_CTA2.grid(row=3, column=6, padx=odsazeni, pady=1)
    tlacitko_vlozit_CTA3 = tk.Button(dotaz_multifaze_okno, text="Aktuální obraz", command=lambda: (
    vstup_CTA3.delete(0, tk.END), vstup_CTA3.insert(0, hledej_cestu_k_obrazu(False))))
    tlacitko_vlozit_CTA3.grid(row=4, column=6, padx=odsazeni, pady=1)


    # Tlačítka, která otevřou průzkumník souborů, aby si uživatel mohl najít požadované obrazy
    tlacitko_hledat_CTA1 = tk.Button(dotaz_multifaze_okno, text="Hledat", command=lambda: (vstup_CTA1.delete(0, tk.END), vstup_CTA1.insert(0, hledej_cestu_k_obrazu(True))))
    tlacitko_hledat_CTA1.grid(row=2, column=7, padx=odsazeni, pady=1)
    tlacitko_hledat_CTA2 = tk.Button(dotaz_multifaze_okno, text="Hledat", command=lambda: (vstup_CTA2.delete(0, tk.END), vstup_CTA2.insert(0, hledej_cestu_k_obrazu(True))))
    tlacitko_hledat_CTA2.grid(row=3, column=7, padx=odsazeni, pady=1)
    tlacitko_hledat_CTA3 = tk.Button(dotaz_multifaze_okno, text="Hledat", command=lambda: (vstup_CTA3.delete(0, tk.END), vstup_CTA3.insert(0, hledej_cestu_k_obrazu(True))))
    tlacitko_hledat_CTA3.grid(row=4, column=7, padx=odsazeni, pady=1)

    mezera = tk.Label(dotaz_multifaze_okno, padx=odsazeni)
    mezera.grid(row=5, column=0, columnspan=8, sticky=sticky_parametr_sloupec)


    # Kontrolní tlačítka v dotazovém oknu
    # Tlačítka pro ovládání okna (smazat vložené cesty a potvrzení a spuštění tvorby multifázického obrazu)
    tlacitko_potvrzeni = tk.Button(dotaz_multifaze_okno, text="Vytvoř multifázický obraz", font=font_tlacitek, command=lambda: (vytvor_multifazicky_obraz(vstup_CTA1.get(), vstup_CTA2.get(), vstup_CTA3.get()), dotaz_multifaze_okno.destroy()))
    tlacitko_potvrzeni.grid(row=6, column=1)
    tlacitko_smazat = tk.Button(dotaz_multifaze_okno, text="Smazat", font=font_tlacitek, command=lambda: (
    vstup_CTA1.delete(0, tk.END), vstup_CTA2.delete(0, tk.END), vstup_CTA3.delete(0, tk.END)))
    tlacitko_smazat.grid(row=6, column=6)


    # Hlavní smyčka dotazového okna pro vytváření multifázického obrazu
    dotaz_multifaze_okno.mainloop()

# Výstupem této funkce je cesta k příslušnému obrazu.
# Podle vstupu buď umožní vbyhledávání cesty k souboru pomocí průzkumníka souborů, nebo najde cestu k aktuálnímu obrazu v paměti aplikace
def hledej_cestu_k_obrazu(samostatne_hledani):
    # Pokud je vstupní hodnota True, znamená to, že chce uživatel hledat cestu pomocí průzkumníka souborů
    if samostatne_hledani == True:
        soubor = filedialog.askopenfilename(title="Vyber soubor", filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])

    # Pokud je vstupní hodnota False, tak to znamená, že si uživatel přeje použít aktuální obraz
    else:
        soubor = os.path.abspath("upload_image.nii")

    # Nalezená cesta se upraví, aby ji bylo možné dále zpracovávat
    cesta = soubor.replace("\\", "/")

    # Výstupem je nalezená a upravená cesta k požadovanému obrazu
    return cesta

# Funkce, která vytváří multifázický obraz
def vytvor_multifazicky_obraz(cesta_faze_1, cesta_faze_2, cesta_faze_3):
    # Načtení obrazů pomocí cest, vstupujících do funkce
    faze_1 = sitk.ReadImage(cesta_faze_1)
    faze_2 = sitk.ReadImage(cesta_faze_2)
    faze_3 = sitk.ReadImage(cesta_faze_3)

    # Spojení jednotlivých fází do jednoho multifázického obrazu
    spojeni_1_2 = sitk.Maximum(faze_1, faze_2)
    multifaze = sitk.Maximum(spojeni_1_2, faze_3)

    # Uložení obrazu
    sitk.WriteImage(multifaze, "multiphase_image.nii")

    # Po vytvoření multifázického obrazu se vypíše pro uživatele hláška, že byl multifázický obraz vytvořen
    odpoved_po_vytvoreni_multifaze()

# Funkce, která vytváří oznamovací okno, že vytvoření a uložení multifázického obrazu proběhlo úspěšně
def odpoved_po_vytvoreni_multifaze():
    # Základní nastavení oznamovacího okna (rozměry pomocného okna a nadpis)
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Vytvoření multifázického obrazu")
    dotaz_okno.geometry("350x50")


    # Vytvoření a umístění oznámení do oznamovacího okna
    dotaz = tk.Label(dotaz_okno, text="Multifázický obraz byl úspěšně vytvořený a uložený do paměti.", anchor="center")
    dotaz.pack()
