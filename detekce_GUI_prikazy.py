import tkinter as tk
from tkinter import filedialog
import SimpleITK as sitk
from PIL import Image, ImageTk
import numpy as np



# Funkce, jejíž funkčí je načtení obrazu ze složky do formátu SimpleITK
def nacti_obrazek(cesta):
    reader = sitk.ImageSeriesReader()
    slozka = reader.GetGDCMSeriesFileNames(cesta)
    reader.SetFileNames(slozka)

    obrazek = reader.Execute()

    return obrazek

def nacist_obrazek():
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Načíst složku nebo soubor")
    dotaz_okno.geometry("350x100")
    font_tlacitek = ("Arial", 12, "bold")

    dotaz = tk.Label(dotaz_okno, text="Vyberte, zda chcece načíst samotný soubor nebo celou složku.")
    dotaz.pack()
    tlacitko_soubor = tk.Button(dotaz_okno, text="DICOM", font=font_tlacitek, command=lambda: (dotaz_okno.destroy(), nacti_soubor()))
    tlacitko_soubor.pack(side="left", padx=30, anchor="center")
    tlacitko_slozka = tk.Button(dotaz_okno, text="NIfTI", font=font_tlacitek, command=lambda: (dotaz_okno.destroy(), nacti_slozku()))
    tlacitko_slozka.pack(side="right", padx=30, anchor="center")

    dotaz_okno.mainloop()

def nacti_soubor():
    soubor = filedialog.askopenfilename(title="Vyber soubor", filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])

    cesta = soubor.replace("\\", "/")
    obrazek_nacteny = sitk.ReadImage(cesta)

    sitk.WriteImage(obrazek_nacteny, "upload_image.nii")
    odpoved_po_nacteni()


def nacti_slozku():
    slozka = filedialog.askdirectory(title="Vyber složku")

    cesta = slozka.replace("\\", "/")
    obrazek_nacteny = nacti_obrazek(cesta=cesta)

    sitk.WriteImage(obrazek_nacteny, "upload_image.nii")
    odpoved_po_nacteni()


def odpoved_po_nacteni():
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Nahrávání obrazu")
    dotaz_okno.geometry("300x50")

    dotaz = tk.Label(dotaz_okno, text="Obraz byl úspěšně načtený a uložený do paměti.", anchor="center")
    dotaz.pack()


def uloz_soubor():
    cesta_k_ulozenemu_souboru = filedialog.asksaveasfilename(defaultextension=".nii",
                                          filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])

    if cesta_k_ulozenemu_souboru:
        obrazek = sitk.ReadImage("upload_image.nii")
        sitk.WriteImage(obrazek, cesta_k_ulozenemu_souboru)
        odpoved_po_ulozeni()


def odpoved_po_ulozeni():
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Uložení obrazu")
    dotaz_okno.geometry("300x50")

    dotaz = tk.Label(dotaz_okno, text="Obraz byl úspěšně uložený na vybrané místo.", anchor="center")
    dotaz.pack()

