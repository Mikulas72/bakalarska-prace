# Knihovny potřebné pro chod pomocných příkazů pro GUI
import SimpleITK as sitk
import tkinter as tk
from tkinter import filedialog
import os



# Blok kódu s funkcemi pro správnou registraci obrszů v GUI
# Funkce, která umožní uživateli vložit cesty k obrazům, které chce registrovat
def vyber_registraci():
    # Vytvoření okna, které umožní uživateli vložit cesty k obrazům
    dotaz_registrace_okno = tk.Tk()
    dotaz_registrace_okno.title("Registrace obrazu")
    dotaz_registrace_okno.geometry("730x200")
    font_tlacitek = ("Arial", 12, "bold")
    sticky_parametr_sloupec = "ew"
    odsazeni = 5
    kotva = "center"

    # Vytvoření nadpisu v okně
    nadpis = tk.Label(dotaz_registrace_okno, text="Vyberte, jaké obrazy se mají registrovat.", anchor=kotva, font=("Arial", 12))
    nadpis.grid(row=0, column=0, columnspan=6, sticky=sticky_parametr_sloupec)

    mezera = tk.Label(dotaz_registrace_okno, padx=odsazeni)
    mezera.grid(row=1, column=0, columnspan=6, sticky=sticky_parametr_sloupec)

    # Popisky k vstupům, aby uživatel věděl, který vstup patří ke kterému obrazu
    popis_fixni_obraz = tk.Label(dotaz_registrace_okno, text="Fixní obraz:")
    popis_fixni_obraz.grid(row=2, column=0, sticky=sticky_parametr_sloupec)
    popis_pohyblivy_obraz = tk.Label(dotaz_registrace_okno, text="Pohyblivý obraz:")
    popis_pohyblivy_obraz.grid(row=3, column=0, sticky=sticky_parametr_sloupec)

    # Vstupní pole pro zadání cesty k obrazům
    vstup_fixni_obraz = tk.Entry(dotaz_registrace_okno)
    vstup_fixni_obraz.grid(row=2, column=1, columnspan=3, sticky=sticky_parametr_sloupec)
    vstup_pohyblivy_obraz = tk.Entry(dotaz_registrace_okno)
    vstup_pohyblivy_obraz.grid(row=3, column=1, columnspan=3, sticky=sticky_parametr_sloupec)

    # Tlačitka, která vloží aktuální obraz (v paměti aplikace) (tedy cestu k němu) do vstupního pole
    tlacitko_vlozit_fixni_obraz = tk.Button(dotaz_registrace_okno, text="Fixní obraz", command=lambda: (
        vstup_fixni_obraz.delete(0, tk.END), vstup_fixni_obraz.insert(0, hledej_cestu_k_obrazu(False, True))))
    tlacitko_vlozit_fixni_obraz.grid(row=2, column=4, padx=odsazeni, pady=1, sticky=sticky_parametr_sloupec)
    tlacitko_vlozit_pohyblivy_obraz = tk.Button(dotaz_registrace_okno, text="Aktuální obraz", command=lambda: (
        vstup_pohyblivy_obraz.delete(0, tk.END), vstup_pohyblivy_obraz.insert(0, hledej_cestu_k_obrazu(False, False))))
    tlacitko_vlozit_pohyblivy_obraz.grid(row=3, column=4, padx=odsazeni, pady=1)

    # Tlačítka, která otevřou průzkumník souborů, aby si uživatel mohl najít požadované obrazy
    tlacitko_hledat_fixni_obraz = tk.Button(dotaz_registrace_okno, text="Hledat", command=lambda: (
    vstup_fixni_obraz.delete(0, tk.END), vstup_fixni_obraz.insert(0, hledej_cestu_k_obrazu(True, True))))
    tlacitko_hledat_fixni_obraz.grid(row=2, column=5, padx=odsazeni, pady=1)
    tlacitko_hledat_pohyblivy_obraz = tk.Button(dotaz_registrace_okno, text="Hledat", command=lambda: (
    vstup_pohyblivy_obraz.delete(0, tk.END), vstup_pohyblivy_obraz.insert(0, hledej_cestu_k_obrazu(True, False))))
    tlacitko_hledat_pohyblivy_obraz.grid(row=3, column=5, padx=odsazeni, pady=1)

    mezera = tk.Label(dotaz_registrace_okno, padx=odsazeni)
    mezera.grid(row=4, column=0, columnspan=6, sticky=sticky_parametr_sloupec)

    # Zpráva, která informuje uživatele, aby nevypínal registraci, protože potřebuje nějaký čas
    info_registrace = tk.Label(dotaz_registrace_okno, text="Po spuštění registrace obrazu nezavírejte toto okno. Vyčkejte na informační zprávu, že byla registrace ukončena.")
    info_registrace.grid(row=7, column=0, columnspan=6, sticky=sticky_parametr_sloupec)

    # Kontrolní tlačítka v dotazovém oknu
    # Tlačítka pro ovládání okna (smazat vložené cesty a potvrzení a spuštění tvorby multifázického obrazu)
    tlacitko_potvrzeni_1_faze = tk.Button(dotaz_registrace_okno, text="Registrace 1. fáze", font=font_tlacitek, command=lambda: (hlavni_funkce_registrace(vstup_fixni_obraz.get(), vstup_pohyblivy_obraz.get(), 1), dotaz_registrace_okno.destroy(), info_zprava()))
    tlacitko_potvrzeni_1_faze.grid(row=5, column=1, padx=odsazeni)
    tlacitko_potvrzeni_2_faze = tk.Button(dotaz_registrace_okno, text="Registrace 2. fáze", font=font_tlacitek,
                                          command=lambda: (hlavni_funkce_registrace(vstup_fixni_obraz.get(), vstup_pohyblivy_obraz.get(), 2), dotaz_registrace_okno.destroy(), info_zprava()))
    tlacitko_potvrzeni_2_faze.grid(row=5, column=2, padx=odsazeni)
    tlacitko_potvrzeni_3_faze = tk.Button(dotaz_registrace_okno, text="Registrace 3. fáze", font=font_tlacitek,
                                          command=lambda: (hlavni_funkce_registrace(vstup_fixni_obraz.get(), vstup_pohyblivy_obraz.get(), 3), dotaz_registrace_okno.destroy(), info_zprava()))
    tlacitko_potvrzeni_3_faze.grid(row=5, column=3, padx=odsazeni)

    tlacitko_smazat = tk.Button(dotaz_registrace_okno, text="Smazat", font=font_tlacitek, command=lambda: (
        vstup_fixni_obraz.delete(0, tk.END), vstup_pohyblivy_obraz.delete(0, tk.END)))
    tlacitko_smazat.grid(row=5, column=4)

    mezera = tk.Label(dotaz_registrace_okno, padx=odsazeni)
    mezera.grid(row=6, column=0, columnspan=6, sticky=sticky_parametr_sloupec)

    # Hlavní smyčka dotazového okna pro vytváření multifázického obrazu
    dotaz_registrace_okno.mainloop()

# Výstupem této funkce je cesta k příslušnému obrazu.
# Podle vstupu buď umožní vyhledávání cesty k souboru pomocí průzkumníka souborů, nebo najde cestu k aktuálnímu obrazu v paměti aplikace(případně k fixnímu obrazu v paměti aplikace)
def hledej_cestu_k_obrazu(samostatne_hledani, fixni_obraz):
    # Pokud je vstupní hodnota True, znamená to, že chce uživatel hledat cestu pomocí průzkumníka souborů
    if samostatne_hledani == True:
        soubor = filedialog.askopenfilename(title="Vyber soubor", filetypes=[("DICOM soubor", "*.dcm"), ("NIfTI soubor", "*.nii"), ("Všechny soubory", "*.*")])

    # Pokud je vstupní hodnota False, tak to znamená, že si uživatel přeje použít aktuální obraz nebo fixní obraz z paměti programu
    else:
        # Pokud je proměnná True, znamená to, že se uživatel snaží najít fixní obraz
        # Funkce se pokusí požadovaný soubor nalézt, ale pokud se mu to nepodaří, tak vypíše poruchovou hlášku
        if fixni_obraz == True:
            try:
                soubor = os.path.abspath("nativ_image.nii")
            except:
                soubor = ""
                poruchova_hlaska(True)

        # Pokud je proměnná False, znamená to, že se uživatel snaží najít pohyblivý obraz
        # Funkce se pokusí požadovaný soubor nalézt, ale pokud se mu to nepodaří, tak vypíše poruchovou hlášku
        else:
            try:
                soubor = os.path.abspath("upload_image.nii")
            except:
                soubor = ""
                poruchova_hlaska(False)

    # Nalezená cesta se upraví, aby ji bylo možné dále zpracovávat
    cesta = soubor.replace("\\", "/")

    # Výstupem je nalezená a upravená cesta k požadovanému obrazu
    return cesta

 # Funkce, která zajišťuje vypisování poruchové hlášky při nenalezení požadovaných souborů
def poruchova_hlaska(fixni_obraz):
    # Vytvoření okna, ve kterém se bude poruchová hláška vypisovat
    poruchova_hlaska_okno = tk.Tk()
    poruchova_hlaska_okno.title("Soubor nenalezen")
    font_tlacitek = ("Arial", 12, "bold")
    sticky_parametr_sloupec = "ew"
    odsazeni = 5
    kotva = "center"

    # Pokud je proměnná True, znamená to, že se poruchová hláška týká fixního obrazu
    if fixni_obraz == True:
        poruchova_hlaska_okno.geometry("400x130")

        # Vytvoření nadpisu v okně
        nadpis = tk.Label(poruchova_hlaska_okno, text="Hledaný fixní obraz nebyl nalezen v paměti programu.", anchor=kotva, font=("Arial", 12))
        nadpis.grid(row=0, column=0, columnspan=3, sticky=sticky_parametr_sloupec)

        mezera = tk.Label(poruchova_hlaska_okno, padx=odsazeni)
        mezera.grid(row=1, column=0, columnspan=3, sticky=sticky_parametr_sloupec)

        # Popisek toho, proč se objevila poruchová hláška a jak ji vyřešit
        popis = tk.Label(poruchova_hlaska_okno, text="Hledaný fixní obraz se nepodařilo nalézt. Přejete si použít aktuální obraz v uživatelském rozhraní jako fixní obraz?", anchor=kotva, wraplength=(400 - odsazeni), justify="left")
        popis.grid(row=2, column=0, columnspan=3, padx=odsazeni, sticky=sticky_parametr_sloupec)

        # Tlačítka, díky kterým je možné nahradit chybějící fixní obraz aktuálním obrazem v uživatelském rozhraní
        tlacitko_ano = tk.Button(poruchova_hlaska_okno, text="Ano, chci", font=font_tlacitek, command=lambda: (konverze_aktualni_na_fixni()))
        tlacitko_ano.grid(row=4, column=0, padx=odsazeni, pady=odsazeni)
        tlacitko_ne = tk.Button(poruchova_hlaska_okno, text="Ne, nechci", font=font_tlacitek, command=lambda: (poruchova_hlaska_okno.destroy()))
        tlacitko_ne.grid(row=4, column=2, padx=odsazeni, pady=odsazeni)

    # Pokud je proměnná False, znamená to, že se poruchová hláška týká pohyblivého obrazu
    else:
        poruchova_hlaska_okno.geometry("300x50")

        # Vytvoření nadpisu v okně
        nadpis = tk.Label(poruchova_hlaska_okno, text="Hledaný soubor nebyl nalezen v paměti programu.", anchor=kotva)
        nadpis.pack()

    # Hlavní smyčka okna s poruchovovou hláškou
    poruchova_hlaska_okno.mainloop()

# Funkce, která zajišťuje konverzi aktuálního snímku na fixní snímek (pokud si to uživatel bude přát)
def konverze_aktualni_na_fixni():
    # Přeuložení aktuálního obrazu na fixní obraz
    aktualni_obrazek = sitk.ReadImage("upload_image.nii")
    sitk.WriteImage(aktualni_obrazek, "nativ_image_test.nii")

    # Blok kódu, který zajišťuje vytvoření informačního okna pro uživatele
    # Vytvoření okna, ve kterém se bude zpráva vypisovat
    info_okno = tk.Tk()
    info_okno.geometry("420x30")
    kotva = "center"

    # Vytvoření zprávy v okně
    nadpis = tk.Label(info_okno, text="Aktuální obraz byl úspěšně změněn na fixní obraz. Opakujte proces registrace.", anchor=kotva)
    nadpis.pack()

    # Hlavní smyčka okna s informačním oknem
    info_okno.mainloop()

# Funkce, která bude uživatele informovat o průběhu registrace
def info_zprava():
    # Vytvoření okna, ve kterém se bude informační okno vypisovat
    info_registrace_okno = tk.Tk()
    info_registrace_okno.title("Registrace obrazu")
    info_registrace_okno.geometry("350x30")
    kotva = "center"

    # Vytvoření nadpisu v okně
    nadpis = tk.Label(info_registrace_okno, text="Registrovaný obraz byl úspěšně vytvořený a uložený do paměti.", anchor=kotva)
    nadpis.pack()

    # Hlavní smyčka okna s informačním oknem
    info_registrace_okno.mainloop()



# Blok kódu, ve kterém probíhá registrace obrazu
# Funkce vytvářející masku hlavy pacienta
def vytvor_masku_hlavy(pohyblivy_obrazek, z_crop_ratio=0.5):
    # Nastavení prahů v HU, které určí, jaké voxely mohou být v masce použity
    spodni_hranice = -200
    horni_hranice = 3000

    # Vytvoření binární masky pomocí thresholdu (součástí masky je lebka i mozek pacienta)
    maska = sitk.BinaryThreshold(pohyblivy_obrazek, lowerThreshold=spodni_hranice, upperThreshold=horni_hranice, insideValue=1, outsideValue=0)

    # Výběr pouze největší spojité části vzniklé masky (pomocí spojených komponent), kterou je pravděpodobně hlava pacienta
    spojene_komponenty = sitk.ConnectedComponent(maska)
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(spojene_komponenty)
    nejvetsi_label = max(stats.GetLabels(), key=lambda l: stats.GetPhysicalSize(l))
    maska = sitk.BinaryThreshold(spojene_komponenty, lowerThreshold=nejvetsi_label, upperThreshold=nejvetsi_label, insideValue=1, outsideValue=0)

    # Ořez, který odstraní krk a tělo pacienta
    size = maska.GetSize()
    z_omez = int(size[2] * z_crop_ratio)

    # vytvoření nové masky, kde jen horní část zůstane
    crop_maska = sitk.Image(maska.GetSize(), sitk.sitkUInt8)
    crop_maska.CopyInformation(maska)
    crop_pole = sitk.GetArrayFromImage(maska)
    crop_pole[:z_omez, :, :] = 0  # odstranění spodních vrstev
    maska_finalni = sitk.GetImageFromArray(crop_pole)
    maska_finalni.CopyInformation(maska)

    return maska_finalni

# Funkce, která provádí ořez podle vytvořené masky
def orez_podle_masky(obrazek, maska):
    # Aplikace masky, čímž se odstraní voxely mimo oblast zájmu
    maskova_uprava = sitk.Mask(obrazek, maska, outsideValue=-1024)

    # Výpočet bounding boxu
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(maska)
    bbox = stats.GetBoundingBox(1)  # (x, y, z, size_x, size_y, size_z)

    # Výřez obrazu podle bounding boxu
    roi = sitk.RegionOfInterestImageFilter()
    roi.SetIndex(bbox[:3])
    roi.SetSize(bbox[3:])
    orezany = roi.Execute(maskova_uprava)

    return orezany

# Funkce zajišťující registraci
def main(fixed_image, moving_image):
    # Sjednocení orientace a datového typu fixního a pohyblivého obrazu
    fixed_normalized = sitk.DICOMOrient(fixed_image, "LPS")
    moving_normalized = sitk.DICOMOrient(moving_image, "LPS")

    fixed = sitk.Cast(fixed_normalized, sitk.sitkFloat32)
    moving = sitk.Cast(moving_normalized, sitk.sitkFloat32)

    # Nastavení registrace
    R = sitk.ImageRegistrationMethod()

    # Nastavení metriky registrace
    R.SetMetricAsMattesMutualInformation(50)
    R.SetMetricSamplingStrategy(R.RANDOM)
    R.SetMetricSamplingPercentage(0.2)

    # Nastavení optimalizátoru
    R.SetOptimizerAsRegularStepGradientDescent(learningRate=3.0, minStep=0.01, numberOfIterations=1000, gradientMagnitudeTolerance=1e-6, relaxationFactor=0.5)

    # Nastavení interpolátoru
    R.SetInterpolator(sitk.sitkLinear)

    # Aktivace víceúrovňové registrace (pro zlepšení registrace)
    R.SetShrinkFactorsPerLevel([4, 2, 1])
    R.SetSmoothingSigmasPerLevel([2, 1, 0])

    # Nastavení počáteční transformace
    initial_transform = sitk.CenteredTransformInitializer(
        fixed,
        moving,
        sitk.Euler3DTransform(),
        sitk.CenteredTransformInitializerFilter.MOMENTS)

    R.SetInitialTransform(initial_transform, inPlace=False)

    # Spuštění registrace
    outTx = R.Execute(fixed, moving)

    # Aplikace registrace na pohyblivý obrázek
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(-1024)
    resampler.SetTransform(outTx)

    out = resampler.Execute(moving)

    # Změna orientace, protože se obraz přetáčí
    out_change = sitk.DICOMOrient(out, "RPS")

    # Výstupem funkce je zregistrovaný obraz
    return out_change

# Hlavní funkce registrace
def hlavni_funkce_registrace(fixni_obraz_cesta, pohyblivy_obraz_cesta, faze):
    # Načtení požadovaných souborů pro registraci
    fixni_obraz = sitk.ReadImage(fixni_obraz_cesta)
    pohyblivy_obraz = sitk.ReadImage(pohyblivy_obraz_cesta)

    # Pokud je vstupní proměnná 1, tak to znamená, že uživatel chce provést registraci 1. fáze CT obrazů
    if faze == 1:
        # Vypočítá se ideální místo, které oddělí hlavu pacienta od zbytku těla
        moving_rezy = pohyblivy_obraz.GetSize()[2]
        fixed_rezy = fixni_obraz.GetSize()[2]
        ratio = ((moving_rezy - fixed_rezy) / moving_rezy) + 0.05

        # Zavolá se funkce, která vytvoří masku hlavy pacienta
        maska = vytvor_masku_hlavy(pohyblivy_obrazek=pohyblivy_obraz, z_crop_ratio=ratio)

        # Zavolá se funkce, která odstraní podle masky krk a hrudník pacienta
        orezany_pohyblivy_obraz = orez_podle_masky(obrazek=pohyblivy_obraz, maska=maska)

        # U ořezaného obrazu se sjednotí počátek soustavy souřadnic a orientace obrazu
        orezany_pohyblivy_obraz.SetOrigin(pohyblivy_obraz.GetOrigin())
        orezany_pohyblivy_obraz.SetDirection(pohyblivy_obraz.GetDirection())

        # Upravený obraz se zavolá do funkce, která provede registraci obrazu
        obrazek_po_rigidni_registraci = main(fixed_image=fixni_obraz, moving_image=orezany_pohyblivy_obraz)

        # Výsledný zregistrovaný obraz se uloží
        sitk.WriteImage(obrazek_po_rigidni_registraci, "CTA1_image.nii")

    # Pokud je vstupní proměnná 2 nebo 3, tak to znamená, že uživatel chce provést registraci 2. nebo 3. fáze CT obrazů
    else:
        # Nahrané obrazy se zavolají do funkce, která provede registraci obrazu
        obrazek_po_rigidni_registraci = main(fixed_image=fixni_obraz, moving_image=pohyblivy_obraz)

        # Pokud je vstupní proměnná 2, tak se ovýsledný obraz uloží jako 2. fáze CT obrazů
        if faze == 2:
            sitk.WriteImage(obrazek_po_rigidni_registraci, "CTA2_image.nii")
        # Pokud je vstupní proměnná 3, tak se ovýsledný obraz uloží jako 3. fáze CT obrazů
        else:
            sitk.WriteImage(obrazek_po_rigidni_registraci, "CTA3_image.nii")

    # Výsledný zregistrovaný obraz se uloží i jako obecný registrovaný obraz
    sitk.WriteImage(obrazek_po_rigidni_registraci, "registered_image.nii")
