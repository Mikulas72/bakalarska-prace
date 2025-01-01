import SimpleITK as sitk


# Funkce, jejíž funkčí je načtení obrazu ze složky do formátu SimpleITK
def nacti_obrazek(cesta):
    reader = sitk.ImageSeriesReader()
    slozka = reader.GetGDCMSeriesFileNames(cesta)
    reader.SetFileNames(slozka)

    obrazek = reader.Execute()

    return obrazek

# Funkce, jejímž úkolem je provést predzpracování obrazů (sjednocení metadat)
def predzpracovani_obrazu(fixni_obrazek, pohyblivy_obrazek):
    # Sjednocuji orientaci registrovaného obrazu tak, aby odpovídal orientaci fixního obrazu
    if fixni_obrazek.GetDirection() != pohyblivy_obrazek.GetDirection():
        pohyblivy_obrazek.SetDirection(fixni_obrazek.GetDirection())

    # Nastavuji společnou pozici počátku
    pohyblivy_obrazek.SetOrigin(fixni_obrazek.GetOrigin())

    return pohyblivy_obrazek

# Funkce, která provádí rigidní registraci obrazu
def registrace_obrazu_rigidni(fixni_obrazek, pohyblivy_obrazek):
    # Sjednocuji datový typ registrovaného obrazu tak, aby odpovídal datovému typu fixního obrazu
    if pohyblivy_obrazek.GetPixelIDTypeAsString() != fixni_obrazek.GetPixelIDTypeAsString():
        fixni_obrazek = sitk.Cast(fixni_obrazek, sitk.sitkFloat32)
        pohyblivy_obrazek = sitk.Cast(pohyblivy_obrazek, sitk.sitkFloat32)

    rigidni_registrace = sitk.ImageRegistrationMethod()
    # Nastavení rigidní transformace
    inicializacni_transformace = sitk.CenteredTransformInitializer(fixni_obrazek, pohyblivy_obrazek,
                                                                   sitk.Euler3DTransform(),
                                                                   sitk.CenteredTransformInitializerFilter.GEOMETRY)

    # Provedení rigidní transformace
    rigidni_registrace.SetInitialTransform(inicializacni_transformace, inPlace=False)
    rigidni_registrace.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    rigidni_registrace.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=200)
    rigidni_registrace.SetInterpolator(sitk.sitkLinear)
    rigidni_registrace.SetShrinkFactorsPerLevel([4, 2, 1])
    rigidni_registrace.SetSmoothingSigmasPerLevel([2, 1, 0])

    # Aplikace rigidní transformace
    rigidni_transformace = rigidni_registrace.Execute(fixni_obrazek, pohyblivy_obrazek)
    return rigidni_transformace

# Funkce, která provádí elastickou registraci obrazu
def registrace_obrazu(fixni_obrazek, pohyblivy_obrazek):
    # Sjednocuji datový typ registrovaného obrazu tak, aby odpovídal datovému typu fixního obrazu
    if pohyblivy_obrazek.GetPixelIDTypeAsString() != fixni_obrazek.GetPixelIDTypeAsString():
        fixni_obrazek = sitk.Cast(fixni_obrazek, sitk.sitkFloat32)
        pohyblivy_obrazek = sitk.Cast(pohyblivy_obrazek, sitk.sitkFloat32)

    registracni_metoda = sitk.ImageRegistrationMethod()
    # Nastavení elastické transformace
    registracni_metoda.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)

    # Provedení elastické transformace
    registracni_metoda.SetMetricSamplingStrategy(registracni_metoda.RANDOM)
    registracni_metoda.SetMetricSamplingPercentage(0.01)
    registracni_metoda.SetShrinkFactorsPerLevel([4, 2, 1])
    registracni_metoda.SetSmoothingSigmasPerLevel([2.0, 1.0, 0.0])

    registracni_metoda.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                     convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registracni_metoda.SetOptimizerScalesFromPhysicalShift()

    pocatecni_transformace = sitk.CenteredTransformInitializer(fixni_obrazek, pohyblivy_obrazek,
                                                               sitk.Euler3DTransform(),
                                                               sitk.CenteredTransformInitializerFilter.GEOMETRY)
    registracni_metoda.SetInitialTransform(pocatecni_transformace, inPlace=False)
    registracni_metoda.SetInterpolator(sitk.sitkLinear)

    # Aplikace elastické transformace
    finalni_transformace = registracni_metoda.Execute(fixni_obrazek, pohyblivy_obrazek)
    return finalni_transformace

# Hlavní funkce programu (sjednocuje celý chod programu)
def hlavni_funkce(cesta_k_souborum_reference, cesta_k_souborum):
    # Načtení fixního a pohyblivého obrazu
    pohyblivy_obrazek = nacti_obrazek(cesta=cesta_k_souborum)
    fixni_obrazek = nacti_obrazek(cesta=cesta_k_souborum_reference)

    # Prvotní predzpracování pohyblivého obrazu tak, aby jeho metadata co nejvíce odpovídali fixnímu obrazu
    pohyblivy_obrazek_zpracovany = predzpracovani_obrazu(fixni_obrazek=fixni_obrazek, pohyblivy_obrazek=pohyblivy_obrazek)

    # Provedení rigidní transformace
    transformace = registrace_obrazu_rigidni(fixni_obrazek=fixni_obrazek, pohyblivy_obrazek=pohyblivy_obrazek_zpracovany)

    # Aplikace rigidní transformace na pohyblivý obraz
    vysledek_rigidni = sitk.Resample(pohyblivy_obrazek_zpracovany, fixni_obrazek, transformace, sitk.sitkLinear, 0.0, pohyblivy_obrazek_zpracovany.GetPixelID())
    pohyblivy_obrazek_novy = vysledek_rigidni

    # Aplikace elastické transformace na pohyblivý obraz
    transformace_nova = registrace_obrazu(fixni_obrazek=fixni_obrazek, pohyblivy_obrazek=pohyblivy_obrazek_novy)
    vysledek = sitk.Resample(pohyblivy_obrazek_novy, fixni_obrazek, transformace_nova, sitk.sitkLinear, 0.0, pohyblivy_obrazek_novy.GetPixelID())

    return fixni_obrazek, vysledek


# Cesty k složce, kde se nachází referenční obraz a obraz, který se má registrovat
cesta_k_souborum = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\CTA2"
cesta_k_souborum_reference = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\nativ"

# Volání hlavní funkce, které provede celou registraci
fixni_obrazek, vysledek = hlavni_funkce(cesta_k_souborum=cesta_k_souborum, cesta_k_souborum_reference=cesta_k_souborum_reference)

# Uložení registrovaného obrazu
sitk.WriteImage(vysledek, "vysledek_registrace.nii")

# Vykreslení registrovaného obrazu a nativního obrazu ve Fiji
fixni_obrazek = sitk.Cast(fixni_obrazek, sitk.sitkFloat32)
sitk.Show(fixni_obrazek, "nativ", debugOn=True)
vysledek = sitk.Cast(vysledek, sitk.sitkFloat32)
sitk.Show(vysledek, "CT snímky", debugOn=True)
