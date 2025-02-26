import SimpleITK as sitk
from skimage.metrics import structural_similarity as ssim
import numpy as np


# Funkce pro načtení snímků
def nacti_obrazek(cesta):
    # Načtení 3D obrazu
    reader = sitk.ImageSeriesReader()
    slozka = reader.GetGDCMSeriesFileNames(cesta)

    reader.SetFileNames(slozka)

    obrazek = reader.Execute()
    return obrazek

# Funkce, která provádí rigidní registraci obrazu
def registrace_obrazu_rigidni(fixni_obrazek, pohyblivy_obrazek):
    # Sjednocuji datový typ registrovaného obrazu tak, aby odpovídal datovému typu fixního obrazu
    if pohyblivy_obrazek.GetPixelIDTypeAsString() != fixni_obrazek.GetPixelIDTypeAsString():
        fixni_obrazek = sitk.Cast(fixni_obrazek, sitk.sitkFloat32)
        pohyblivy_obrazek = sitk.Cast(pohyblivy_obrazek, sitk.sitkFloat32)

    # Vytvoření binární masky pro fixní a pohyblivý obrázek (u registrace bez masek tuto část kódu vymazat)
    binarni_maska_fixni = sitk.BinaryThreshold(fixni_obrazek, lowerThreshold=-250,
                                               upperThreshold=2000, insideValue=1,
                                               outsideValue=0)
    binarni_maska_pohyblivy = sitk.BinaryThreshold(pohyblivy_obrazek, lowerThreshold=-250,
                                                   upperThreshold=2000, insideValue=1,
                                                   outsideValue=0)

    rigidni_registrace = sitk.ImageRegistrationMethod()
    # Nastavení rigidní transformace
    rigidni_registrace.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)

    # Volání binárních masek (u registrace bez masek tyto 2 řádky vymazat)
    rigidni_registrace.SetMetricFixedMask(binarni_maska_fixni)
    rigidni_registrace.SetMetricMovingMask(binarni_maska_pohyblivy)

    rigidni_registrace.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=200)

    inicializacni_transformace = sitk.CenteredTransformInitializer(fixni_obrazek, pohyblivy_obrazek,
                                                                   sitk.Euler3DTransform())
                                                                   #, sitk.CenteredTransformInitializerFilter.GEOMETRY)

    # Provedení rigidní transformace
    rigidni_registrace.SetInitialTransform(inicializacni_transformace, inPlace=False)
    # rigidni_registrace.SetInterpolator(sitk.sitkLinear)
    # rigidni_registrace.SetShrinkFactorsPerLevel([4, 2, 1])
    # rigidni_registrace.SetSmoothingSigmasPerLevel([2, 1, 0])

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

    registracni_metoda.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=200,
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
def hlavni_funkce(fixni_obrazek, pohyblivy_obrazek_zpracovany):
    # Provedení rigidní transformace
    transformace = registrace_obrazu_rigidni(fixni_obrazek=fixni_obrazek, pohyblivy_obrazek=pohyblivy_obrazek_zpracovany)
    print("Rigidní registrace hotova")

    # Aplikace rigidní transformace na pohyblivý obraz
    vysledek_rigidni = sitk.Resample(pohyblivy_obrazek_zpracovany, fixni_obrazek, transformace, sitk.sitkLinear) #  0.0, pohyblivy_obrazek_zpracovany.GetPixelID())
    pohyblivy_obrazek_novy = vysledek_rigidni


    # Aplikace elastické transformace na pohyblivý obraz
    transformace_nova = registrace_obrazu(fixni_obrazek=fixni_obrazek, pohyblivy_obrazek=pohyblivy_obrazek_novy)
    vysledek = sitk.Resample(pohyblivy_obrazek_novy, fixni_obrazek, transformace_nova, sitk.sitkLinear, 0.0, pohyblivy_obrazek_novy.GetPixelID())
    print("Registrace hotova")

    return vysledek


# Cesty k uložištím obrázků
cesta_k_souborum = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\CTA2"
cesta_k_souborum_2 = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\CTA3"
cesta_k_souborum_reference = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\CTA1"
cesta_k_souborum_ref = r"C:\Users\perla\OneDrive\Plocha\škola\bakalářka\Data_BP\Data_BP\41\nativ"

# Volání funkce pro načtení obrazků
pohyblivy_obrazek = nacti_obrazek(cesta=cesta_k_souborum_reference)
pohyblivy_obrazek_2 = nacti_obrazek(cesta=cesta_k_souborum)
pohyblivy_obrazek_3 = nacti_obrazek(cesta=cesta_k_souborum_2)
fixni_obrazek = nacti_obrazek(cesta=cesta_k_souborum_ref)


# Odstranění hrudníku, ramen a krku
# Vytvoření průměrného snímku který ukazuje začátek oblasti s mozkem
pohyblivy_obrazek_pole = sitk.GetArrayFromImage(pohyblivy_obrazek)
pohyblivy_obrazek_pole_2 = sitk.GetArrayFromImage(pohyblivy_obrazek_2)[0, :, :]
pohyblivy_obrazek_pole_3 = sitk.GetArrayFromImage(pohyblivy_obrazek_3)[0, :, :]

prumerny_obraz_pole = (pohyblivy_obrazek_pole_2 + pohyblivy_obrazek_pole_3) / 2
prumerny_obraz = sitk.GetImageFromArray(prumerny_obraz_pole)
prumerny_obraz = sitk.Cast(prumerny_obraz, sitk.sitkInt16)
prumerny_obraz_pole = sitk.GetArrayFromImage(prumerny_obraz)

# For cyklus, který každý snímek CTA1 porovná pomocí metody SSIM s průměrným obrazem a uloží hodnotu podobnosti
podobnosti = []
for index_obrazu in range(0, pohyblivy_obrazek_pole.shape[0]):
    index_podobnosti, balast = ssim(pohyblivy_obrazek_pole[index_obrazu, :, :], prumerny_obraz_pole, full=True, multichannel=False)
    podobnosti.append(index_podobnosti)

# Vyhledání nejpodobnějšího obrazu s průměrným obrazem a ořez oblasti obsahující jen mozek
index_maxima = np.argmax(podobnosti)
novy_obraz = pohyblivy_obrazek_pole[index_maxima:, :, :]
novy_obraz = sitk.GetImageFromArray(novy_obraz)


# Sjednocení originu, spacingu, datového typu a směru (direction)
novy_obraz.SetSpacing(fixni_obrazek.GetSpacing())
novy_obraz.SetOrigin(fixni_obrazek.GetOrigin())
novy_obraz.SetDirection(fixni_obrazek.GetDirection())
fixni_obrazek = sitk.Cast(fixni_obrazek, sitk.sitkFloat32)
novy_obraz = sitk.Cast(novy_obraz, sitk.sitkFloat32)

# Volání funkce pro registraci obrazu
vysledek = hlavni_funkce(fixni_obrazek=fixni_obrazek, pohyblivy_obrazek_zpracovany=novy_obraz)

# Uložení obrázku
sitk.WriteImage(vysledek, "vysledek_zmena_2.nii.gz")

# Zobrazení obrázků ve Fiji
fixni_obrazek = sitk.Cast(fixni_obrazek, sitk.sitkFloat32)
sitk.Show(fixni_obrazek, "nativní obraz", debugOn=True)
vysledek = sitk.Cast(vysledek, sitk.sitkFloat32)
sitk.Show(vysledek, "výsledek", debugOn=True)
