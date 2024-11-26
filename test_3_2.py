import SimpleITK as sitk

# Provedení elastické registrace obrazu podle referencniho obrazku.
def elasticka_registrace_obrazu(CT_snimky, referencni_obraz, pocet_iteraci=50, minimalni_chyba=1.0):
    elasticky_filtr_obrazu = sitk.DemonsRegistrationFilter()

    # Nastavení parametrů registrace
    elasticky_filtr_obrazu.SetNumberOfIterations(pocet_iteraci)  # Počet iterací
    elasticky_filtr_obrazu.SetStandardDeviations(minimalni_chyba)  # Výchozí hodnoty pro standardní odchylky (ovlivňuje hladkost deformace)

    # Zkontroluj, že pohyblivý a referenční obrázek mají stejný datový typ, pokud nemají, sjednoď ho
    if CT_snimky.dtype != referencni_obraz.dtype:
        typ_CT_snimky = CT_snimky.dtype.name
        typ_reference = referencni_obraz.dtype.name
        cislo_CT_snimky = int(typ_CT_snimky[len(typ_CT_snimky) - 2 : len(typ_CT_snimky)])
        cislo_reference = int(typ_reference[len(typ_reference) - 2 : len(typ_reference)])

        if cislo_CT_snimky > cislo_reference:
            novy_type = "int" + str(cislo_CT_snimky)
            referencni_obraz = referencni_obraz.astype(novy_type)
        else:
            novy_type = "int" + str(cislo_reference)
            CT_snimky = CT_snimky.astype(novy_type)

    # Prováděj elastickou registraci obrazu vrstvu po vrstvě
    list_obrazu_sitk = []
    for index in range(0, CT_snimky.shape[0]):
        print(f"Zpracovávám {index + 1} vrstvu.")
        rez = CT_snimky[index, :, :]
        rez_sitk = sitk.GetImageFromArray(rez)

        referencni_rez = referencni_obraz[index, :, :]
        referencni_rez_sitk = sitk.GetImageFromArray(referencni_rez)

        # Provádění elastické registrace
        deformace = elasticky_filtr_obrazu.Execute(referencni_rez_sitk, rez_sitk)
        registrovany_obraz = sitk.Warp(rez_sitk, deformace)

        list_obrazu_sitk.append(registrovany_obraz)

    list_obrazu_sitk = tuple(list_obrazu_sitk)
    spojeni_rezu = sitk.JoinSeries(list_obrazu_sitk)
    return spojeni_rezu

# Načtení řezů a převod do 3D matice obrazu
def nacteni_referencniho_a_pohybliveho_obrazu(cesta_k_souborum, cesta_k_souborum_reference):
    # Zpracování pohyblivého 3D obrazu
    serie_obrazku = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(cesta_k_souborum)
    serie_obrazku = list(serie_obrazku)

    ctecka_serie = sitk.ImageSeriesReader()
    ctecka_serie.SetFileNames(serie_obrazku)
    obrazek_3D = ctecka_serie.Execute()
    CT_snimky = sitk.GetArrayFromImage(obrazek_3D)

    # Zpracování referenčního 3D obrazu
    serie_obrazku_reference = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(cesta_k_souborum_reference)
    serie_obrazku_reference = list(serie_obrazku_reference)

    ctecka_serie_reference = sitk.ImageSeriesReader()
    ctecka_serie_reference.SetFileNames(serie_obrazku_reference)
    reference_3D = ctecka_serie_reference.Execute()
    CT_reference = sitk.GetArrayFromImage(reference_3D)

    return CT_snimky, CT_reference

# Cesty k souborům a referencím
cesta_k_souborum = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\CTA3"
cesta_k_souborum_reference = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\nativ"

# Volání funkce
CT_snimky, CT_reference = nacteni_referencniho_a_pohybliveho_obrazu(cesta_k_souborum=cesta_k_souborum, cesta_k_souborum_reference=cesta_k_souborum_reference)
spojeni_rezu = elasticka_registrace_obrazu(CT_snimky=CT_snimky, referencni_obraz=CT_reference)

# Zobrazení pomocí Fiji
sitk.Show(spojeni_rezu, "CT snímky", debugOn=True)
