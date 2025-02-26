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
    tlacitko_soubor = tk.Button(dotaz_okno, text="Soubor", font=font_tlacitek, command=lambda: (dotaz_okno.destroy(), nacti_soubor()))
    tlacitko_soubor.pack(side="left", padx=30, anchor="center")
    tlacitko_slozka = tk.Button(dotaz_okno, text="Složka", font=font_tlacitek, command=lambda: (dotaz_okno.destroy(), nacti_slozku()))
    tlacitko_slozka.pack(side="right", padx=30, anchor="center")

    dotaz_okno.mainloop()

def nacti_soubor():
    soubor = filedialog.askopenfilename(title="Vyber soubor", filetypes=[("Všechny soubory", "*.*")])

    if soubor:
        print("Vybraný soubor: ", soubor)


def nacti_slozku():
    slozka = filedialog.askdirectory(title="Vyber složku")

    cesta = slozka.replace("\\", "/")
    obrazek_nacteny = nacti_obrazek(cesta=cesta)

    sitk.WriteImage(obrazek_nacteny, "upload_image.nii")
    # dotaz_po_nacteni()


def dotaz_po_nacteni():
    dotaz_okno = tk.Tk()
    dotaz_okno.title("Zobrazení")
    dotaz_okno.geometry("300x100")
    font_tlacitek = ("Arial", 12, "bold")

    dotaz = tk.Label(dotaz_okno, text="Obraz byl úspěšně načtený a uložený do paměti.")
    dotaz.pack()
    dotaz_2 = tk.Label(dotaz_okno, text="Chcete ho zobrazit?")
    dotaz_2.pack(side="top")
    tlacitko_soubor = tk.Button(dotaz_okno, text="ANO", font=font_tlacitek)
    tlacitko_soubor.pack(side="left", padx=30, anchor="center")
    tlacitko_slozka = tk.Button(dotaz_okno, text="NE", font=font_tlacitek, command=dotaz_okno.destroy)
    tlacitko_slozka.pack(side="right", padx=30, anchor="center")


def uloz_soubor():
    soubor = filedialog.asksaveasfilename(defaultextension=".nii",
                                          filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])
