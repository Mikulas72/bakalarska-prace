# Knihovny potřebné pro chod nápovědy GUI
import tkinter as tk
from PIL import Image, ImageTk
from PIL.ImageOps import expand
from tkinter import ttk


# Funkce, která zajišťuje zobrazování nápovědy
def napoveda():
    # Vytvoření okna, které umožní uživateli zobrazit nápovědu
    okno_napoveda = tk.Toplevel()
    okno_napoveda.title("Nápověda k programu")
    okno_napoveda.geometry("530x600")
    okno_napoveda.resizable(False, True)
    font_subnadpis = ("Arial", 12, "bold")
    sticky_parametr_sloupec = "ew"
    font_subsubnadpis = ("Arial", 10, "bold")

    sirka = 500

    # Vnitřní funkce, které jsou potřeba pro další fungování okna s nápovědou
    # Dynamicky přizpůsobuje scrollovací oblast podle velikosti vnitřního rámce
    def uprav_oblast_podle_posuvniku(event):
        platno.configure(scrollregion=platno.bbox("all"))

    # Pokud se kurzor nachází na okně a dojde k otočení kolečka na myši, tak se scrollovatelná oblast upraví
    def uprav_oblast_koleckem_mysi_bind(event):
        platno.bind_all("<MouseWheel>", lambda e: platno.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # Pokud se kurzor nenachází na okně a dojde k otočení kolečka na myši, tak se nic nestane
    def uprav_oblast_koleckem_mysi_unbind(event):
        platno.unbind_all("<MouseWheel>")

    # Funkce, která posouvá scrollovatelnou oblast pomocí šipky nahoru
    def uprav_oblast_sipkou_nahoru(event):
        platno.yview_scroll(int(-1), "units")

    # Funkce, která posouvá scrollovatelnou oblast pomocí šipky dolů
    def uprav_oblast_sipkou_dolu(event):
        platno.yview_scroll(int(1), "units")


    # Vnější rámec
    ram_vnejsi = tk.Frame(okno_napoveda)
    ram_vnejsi.pack(fill="both", expand=True)

    # Plátno, na kterém budou všechny widgety
    platno = tk.Canvas(ram_vnejsi)
    platno.pack(side="left", fill="both", expand=True)

    # Svislý posuvník pro posouvání viditelného okna
    posuvnik = tk.Scrollbar(ram_vnejsi, orient="vertical", command=platno.yview)
    posuvnik.pack(side="right", fill="y")

    platno.configure(yscrollcommand=posuvnik.set)

    # Vnitřní rámec, který se bude scrollovat
    vnitrni_scrollovatelny_ram = tk.Frame(platno)

    # Spojení vnitřního rámce s plátnem
    platno.create_window((0, 0), window=vnitrni_scrollovatelny_ram, anchor="nw")

    # Funkce pro volání funkcí, které zajišťují posouvání viditelného plátna
    vnitrni_scrollovatelny_ram.bind("<Configure>", uprav_oblast_podle_posuvniku)
    vnitrni_scrollovatelny_ram.bind("<Enter>", uprav_oblast_koleckem_mysi_bind)
    vnitrni_scrollovatelny_ram.bind("<Leave>", uprav_oblast_koleckem_mysi_unbind)
    vnitrni_scrollovatelny_ram.bind_all("<Up>", uprav_oblast_sipkou_nahoru)
    vnitrni_scrollovatelny_ram.bind_all("<Down>", uprav_oblast_sipkou_dolu)


    # Text, který bude nápověda obsahovat
    # Nadpis nápovědy
    text_nadpis = "Bolehlav"
    text_nadpis_2 = "Nástroj pro detekci trombů v CT datech mozku"

    # Úvod o programu
    text_uvod = "Úvod:"
    text_uvod_2 = "Aplikace Bolehlav je možné použít pro předzpracování, úpravy a prohlížení CT obrazových dat mozku. Kromě těchto úprav je možné aplikaci použít i pro manuální detekování v CT datech mozku. Tento program ovšem není autorizovaný a není určen pro diagnostické nebo terapeutické učely."
    text_uvod_3 = "Tato nápověda poskytuje pro uživatele rady a popis fungování jednotlivých prvků aplikace Bolehlav."

    # Základní přehled uživatelského rozhraní
    text_prehled = "Základní rozvržení aplikace:"
    text_prehled_2 = "Aplikace je rozdělena do několika částí, aby bylo uživatelské rozhraní pro uživatele přehlednější. Rozdělení aplikace do částí je možné si prohlédnout na následujícím obrázku:"
    text_prehled_3 = "Uživatelské rozhraní se tak skládá z 8 řídících bloků, jejichž jednotlivé funkce jsou popsány v seznamu níže."
    seznam_bodu_prehled = ["Správa obrazu (načtení, uložení a vymazaní používného obrazu).",
                           "Úprava a práce s obrazovými daty (registrace, tvorba obrazu časové projekce maximální intenzity a manuální detekce).",
                           "Postprocessingové úpravy obrazu (nastavení CT okna).", "Nápověda",
                           "Tlačítka pro změnu anatomické roviny.",
                           "Nabídka rychlého přepínání mezi jednotlivými fázemi obrazu.",
                           "Posuvník pro změnu řezu daného obrazu.",
                           "Informativní panel s údaji o používané anatomické rovině, souřadnicích kurzoru a současném řezu v obraze."]

    # Text se správou obrazu
    text_sprava_obrazu = "Správa souborů:"
    text_sprava_obrazu_2 = "Tato část programu Vám umožní provádět základní operace se soubory. Konktretně umožňují tyto tlačítka načíst, zobrazit, uložit a vymazat obraz, který se právě zobrazuje v programu. Detail přepínacího části uživatelského rozhraní je možné si prohlednout na následujícím obrázku:"
    text_sprava_obrazu_3 = "Načíst:"
    text_sprava_obrazu_4 = "Tlačítko NAČÍST umožňuje načíst do programu obraz, se kterým chcete pracovat. Program podporuje načítání obrazů ve formátu DICOM nebo ve formátu NIfTI. Načtení obrazu do programu se provádí následovně:"
    text_sprava_obrazu_5 = "- Po zmáčknutí tlačítka NAČÍST se objeví dotazové okno, stejné jako na obrázku níže, které Vám umožní vybrat si formát nahrávaného souboru."
    text_sprava_obrazu_6 = "- Poté, co si vyberete požadovaný formát obrazu, se nabídkové okno zavře a místo něho se objeví průzkumník souborů, který Vám umožní vyhledat požadovaný soubor."
    text_sprava_obrazu_7 = "- Jakmile pomocí Průzkumníka souborů vyhledáte požadovaný soubor, tak se Průzkumník souborů zavře a zobrazí se informační zpráva, že byl soubor uložený do paměti programu. Zobrazená informační zpráva vypadá následovně:"
    text_sprava_obrazu_8 = "- Po zobrazení této informační zprávy je obraz pro Vás připravený."
    text_sprava_obrazu_9 = "Upozornění: Po načtení obrazu pomocí tlačítka NAČÍST se obraz nezobrazí v uživatelském rozhraní, ale pouze se nahraje do paměti aplikace. Pokud chcete načtený obraz zobrazit, musíte po načtení obrazu zmáčknout tlačítko ZOBRAZIT, aby se načtený obraz objevil v uživatelském rozhraní."
    text_sprava_obrazu_10 = "Zobrazit:"
    text_sprava_obrazu_11 = "Tlačítko ZOBRAZIT slouží pro zobrazení obrazu z paměti programu do uživatelského rozhraní."
    text_sprava_obrazu_12 = "Uložit:"
    text_sprava_obrazu_13 = "Tlačítko ULOŽIT Vám poskytuje možnost uložit si obraz, se kterým v uživatelském rozhraní pracujete. Aplikace umožňuje ukládat obrazy ve formátu DICOM nebo ve formátu NIfTI. Ukládání obrazu je možné provést následovně:"
    text_sprava_obrazu_14 = "- Poté, co je ukládánání aktivováno příslušným tlačítkem, se zobrazí Průzkumník souborů, který Vám umožní vybrat místo uložení, pojmenovat ukládaný soubor a i vybrat požadovaný formát."
    text_sprava_obrazu_15 = "- Jakmile potvrdíte uložení souboru, tak se Průzkumník souborů uzavře a vypíše se informační zpráva, že ukládání proběhlo úspěšně. Informační zpráva může vypadat takhle:"
    text_sprava_obrazu_16 = "- Po zobrazení této informační zprávy je Váš soubor uložený na vybraném místě."
    text_sprava_obrazu_17 = "Smazat:"
    text_sprava_obrazu_18 = "Tlačítkem SMAZAT je možné vymazat z uživatelského rozhraní prohlížený obraz a nahradit ho původním obrázkem s ikonou mozku. Vymazání obrázku není trvalé. Obraz je odstraněn jen z uživatelského rozhraní, ale v paměti programu zůstává i nadále. Pro opětovné vyvolání obrazu použijte tlačítko ZOBRAZIT."

    # Text s úpravami a prací s načteným obrazem
    text_prace_s_obrazem = "Práce s obrazem:"
    text_prace_s_obrazem_2 = "Toto je nejdůležitější část celého programu. Umožní Vám provést registraci obrazů, vytvoření obrazu časové projekce maximální intenzity spojením všech fází do jednoho obrazu a manuální hledání trombů v zobrazovaném obraze. Nechybí ani možnost zobrazit si výsledné obrazy nebo uložit pozice detekovaných trombů do CSV souboru. Jednotlivé operace jsou na sobě nezávislé, takže je nemusíte spouštět v přesně daném pořadí (například: pokud mám již registrované obrazy, tak můžete ihned přejít k tvorbě obrazu časové projekce maximální intenzity a nemusíte znovu provádět registraci)."
    text_prace_s_obrazem_3 = "Detailní zobrazení pracovního terminálu je možné si prohlédnout na následujícím obrázku."
    text_prace_s_obrazem_4 = "Registrace:"
    text_prace_s_obrazem_5 = "Úkolem registrace je zarovnat jednotlivé fáze CT snímání tak, aby se vzájemně překrývali. Tímto překrytím se u registrovaných obrazů zajistí vzájemná geometrická poloha i orientace výsledného obrazu. Registraci obrazu v programu zajišťuje skript schovaný za tlačítkem REGISTRACE, jehož fungování je popsáno níže:"
    text_prace_s_obrazem_6 = "- Po zmáčknutí tlačítka REGISTRACE se otevře dotazové okno, které Vám umožní zadat cesty k fixnímu i pohyblivému obrazu, které se budou vzájemně registrovat. Náhled dotazového okna si můžete prohlédnout na obrázku níže:"
    text_prace_s_obrazem_7 = "- Cesty k fixnímu a pohyblivému obrazu je možné zadat 4 různými způsoby:"
    text_prace_s_obrazem_8 = ["Zadáním cesty k souboru do vstupního pole, která vede k požadovanému obrazu.",
                               "Vyhledání požadovaného obrazu pomocí tlačítka HLEDAT, které otevře Průzkumníka souborů.",
                               "Při vybírání fixního obrazu je možné pomocí tlačítka FIXNÍ OBRAZ použít fixní obraz uložený v paměti programu.",
                               "Použití aktuálního obrazu v uživatelském rozhraní jako pohyblivého obrazu pomocí tlačítka AKTUÁLNÍ OBRAZ."]
    text_prace_s_obrazem_9 = "- Pokud je to potřeba, tak je možné tlačítkem SMAZAT vymazat všechny zadané cesty z obou vstupních polí."
    text_prace_s_obrazem_10 = "- Po výběru fixního a pohyblivého obrazu je nutné programu říct, jaká fáze se bude registrovat. Tento výběr provedete zmáčknutím jednoho z nabízených tlačítek, čímž se zároveň spustí registrace:"
    text_prace_s_obrazem_11 = "- Po vytvoření registrovaného obrazu se objeví informační okno, které Vás bude informovat o ukončení registrace. Informační okno bude vypadat jako na následujícím obrázku:"
    text_prace_s_obrazem_12 = "Upozornění: Registrace je výpočetně náročný proces, proto po jeho spuštění nezavírejte dotazové okno se zadanými cestami ani nevypínejte program. Došlo by k přerušení registračního procesu, který by mohl narušit výsledek registrace. Vyčkejte, dokud Vás program neinformuje o ukončení registrace."
    text_prace_s_obrazem_13 = "Upozornění: Registrovaný obraz bude uložen v paměti programu, ale nezobrazí se v uživatelském rozhraní. Pro jeho zobrazení použíjte tlačítko ZOBRAZIT pod tlačítkem REGISTRACE."
    text_prace_s_obrazem_14 = "Časová projekce:"
    text_prace_s_obrazem_15 = "Tlačítkem ČASOVÁ PROJEKCE je možné pomocí metody časové projekce maximální intenzity vytvořit obraz, který spojuje všechny tři fáze CT snímání do jednoho výsledného obrazu. To umožňuje sledování průtoku kontrastní látky přes mozek v jednom jediném obrázku. Spojování fází v této aplikaci zajišťuje program, jehož fungování je dále popsáno:"
    text_prace_s_obrazem_16 = "- Po zmáčknutí tlačítka ČASOVÁ PROJEKCE se otevře dotazové okno, do kterého je nutné zadat cesty k souborům, které mají tvořit jednotlivé fáze obrazu časově projekce maximální intenzity. Náhled dotazového okna je možné si prohlédnout na obrázku níže:"
    text_prace_s_obrazem_17 = "- Cesty k jednotlivým fázím je možné zadat 3 různými způsoby:"
    text_prace_s_obrazem_18 = ["Zadáním cesty k souboru do vstupního pole, která vede k požadovanému obrazu.", "Vyhledání požadovaného obrazu pomocí tlačítka HLEDAT, které otevře Průzkumníka souborů.", "Použití aktuálního obrazu v uživatelském rozhraní pomocí tlačítka AKTUÁLNÍ OBRAZ."]
    text_prace_s_obrazem_19 = "- Pokud je to potřeba, tak je možné tlačítkem SMAZAT vymazat všechny zadané cesty ze všech vstupních polí."
    text_prace_s_obrazem_20 = "- Jakmile jste spokojeni s Vaším výběrem jednotlivých fází, tak je nutné potvrdit svůj výber tlačítkem VYTVOŘ ČASOVOU PROJEKCI. Až poté dojde k spuštení tvorby obrazu s časovou projekcí maximální intenzity."
    text_prace_s_obrazem_21 = "- Po vytvoření obrazu s časovou projekcí maximální intenzity se objeví informační okno, které Vás bude informovat o vytvoření výsledku. Informační okno bude vypadat jako na následujícím obrázku:"
    text_prace_s_obrazem_22 = "Upozornění: Obraz časové projekce maximální intenzity bude uložen v paměti programu, ale nezobrazí se v uživatelském rozhraní. Pro jeho zobrazení použíjte tlačítko ZOBRAZIT pod tlačítkem ČASOVÁ PROJEKCE."
    text_prace_s_obrazem_23 = "Manuální detekce:"
    text_prace_s_obrazem_24 = "Manuální detekce Vám umožní označit podezřelé místo, ve kterém se nachází trombus. Trombu se označuje pomocí orámování podezřelé oblasti detekčním polynomem. Detekce se provádí v každém řezu obrazu samostatně."
    text_prace_s_obrazem_25 = "Program pro manuální detekci se může nacházet ve 3 různých stavech, mezi kterými je možné přepínat klikáním na talčítko MANUÁLNÍ DETEKCE. Co znamenají jednotlivé stavy je popsané v následujících odstavcích."
    text_prace_s_obrazem_26 = "1. stav - bílé tlačítko:"
    text_prace_s_obrazem_27 = "Když je tlačítko MANUÁLNÍ DETEKCE bílé, tak je manuální detekce deaktivovaná a nebude reagovat na žádný pokus o vytvoření detekčního polynomu."
    text_prace_s_obrazem_28 = "2. stav - žluté tlačítko:"
    text_prace_s_obrazem_29 = "Žluté tlačítko MANUÁLNÍ DETEKCE značí, že je aktivováno tvoření detekčního polynomu. Po kliknutí levým tlačítkem do zobrazeného řezu obrazu se na místě kurzoru objeví oranžově obarvený bod, který tvoří jeden vrchol detekčního polynomu. Jestliže umístíte alespoň 2 body, tak se spojí oranžovou čárou a začnou orámovávat detekovanou oblast. Pomocí pravého tlačítka zase můžete vymazat poslední umístěný bod. Příklad vytvořeného detekčního polynomu je možné si prohlédnout zde:"
    text_prace_s_obrazem_30 = "3. stav - oranžové tlačítko:"
    text_prace_s_obrazem_31 = "Pokud se tlačítko MANUÁLNÍ DETEKCE nachází v oranžovém stavu, tak to znamená, že se manuální detekce přepnula do editačního módu. V tomto módu můžete přesouvat již umístěné body detekčního polynomu na nová místa. Stačí, když pouze kliknete levým tlačítkem myši na novém místo a bod se na něj přesune. Právě přesunutý bod se zvýrazní a detekční polynom se automaticky překreslí. Pravým tlačítkem můžete opět odebírat poslední umístěný bod. Příklad upraveného detekčního polynomu je možné vidět na dalším obrázku:"
    text_prace_s_obrazem_32 = "Zobrazit:"
    text_prace_s_obrazem_33 = "Tlačítka ZOBRAZIT slouží pro zobrazení registrovaného obrazu nebo obrazu časové projekce maximální intenzity z paměti programu do uživatelského rozhraní. Požadovaný obraz zobrazíte kliknutím na tlačítko ZOBRAZIT, které se nachází pod danou metodou, kterou byl požadovaný obraz vytvořený."
    text_prace_s_obrazem_34 = "- Chcete-li tedy zobrazit registorvaný obraz, tak klikněte na tlačítko zobrazit pod tlačítkem REGISTRACE."
    text_prace_s_obrazem_35 = "- Pokud ale chcete zobrazit obraz časové projekce maximální intenzity, tak klikněte na tlačítko zobrazit pod tlačítkem ČASOVÁ PROJEKCE."
    text_prace_s_obrazem_36 = "Smazat:"
    text_prace_s_obrazem_37 = "Tímto tlačítkem je možné úplně vymazat všechny boby detekčního polynomu, které byli v jakémkoliv řezu současného obrazu vytvořeny. Dojde také k vymazání paměti ukládající pozice bodů detekčního polynomu."
    text_prace_s_obrazem_38 = "Uložit:"
    text_prace_s_obrazem_39 = "Tlačítko ULOŽIT umožňuje uložit vytvořený detekční polynom do CSV souboru. Vzniklý CSV soubor je složen ze 2 částí. V první části se nachází metadata o použitém obrázku a ve druhé části CSV souboru, odděleném 2 prázdnými řádky, se nachází souřadnice bodů tvořící detekční polynomy."
    text_prace_s_obrazem_40 = "Každý zaznamenaný detekční bod je zapsaný na samostatném řádku a jeho zápis je složen ze 4 údajů:"
    text_prace_s_obrazem_41 = ["x-ová souřadnice", "y-ová souřadnice", "označení použité anatomické roviny (A - axiální, S - sagitární, K - koronální)", "číslo řezu, ve kterém byl detekční bod vytvořen"]
    text_prace_s_obrazem_42 = "Tvorba CSV souboru je automatizována. Jedinné, co musíte udělat před samotným uložením, je vybrat místo uložení souboru a jeho název pomocí Průzkumníku souborů, který se objeví po stisknutí tlačítka ULOŽIT. Jakmile bude CSV soubor vytvořen a uložen na požadované místo, objeví se informační okno, které bude vypadat následovně:"

    # Postprocessingové úpravy obrazu (CT okno)
    text_postproces_upravy = "Postprocessingové úpravy obrazu nastavením CT okna:"
    text_postproces_upravy_2 = "Tato část programu Vám umožní upravit používaný obraz tak, že na něj aplikujete CT okno. CT okno specificky přenastaví parametry používaného obrazu tak, aby se optimálně zvýraznila požadovaná struktura nebo tkáň mozku. Detail přepínacího části uživatelského rozhraní je možné si prohlédnout na následujícím obrázku:"
    text_postproces_upravy_3 = "CT okno:"
    text_postproces_upravy_4 = "Tlačítko CT OKNO Vám umožní aplikovat CT okno na obraz v uživatelském rozhraní. Na výběr máte již přednastavené CT okna, nebo můžete použít svoje vlastní CT okno. Také můžete již aplikované CT okno z obrazu odstranit a vrátit se k původnímu obrazu."
    text_postproces_upravy_5 = "Popis programu pro vyokňování je popsán níže:"
    text_postproces_upravy_6 = "- Po zmáčknutí tlačítka CT OKNO se objeví dotazové okno, které Vám nabídne předpřipravené CT okna, vytvoření vlastního CT okna nebo odstranění již aplikovaného CT okna. Náhled dotazového okna je možné si prohlédnout na obrázku níže:"
    text_postproces_upravy_7 = "Předpřipravené CT okna:"
    text_postproces_upravy_8 = "Předpřipravené CT okna upravují použitý obraz tak, aby byla detailně zobrazena jen ta struktura, pro kterou je dané CT okno použito. Aplikace Bolehlav obsahuj celkem 5 předpřipravených CT oken, jejichž parametry v Hounsfieldových jednotkách (HU) jsou popsány níže."
    text_postproces_upravy_9 = [("Mozkové", 40, 80), ("Kostní", 1524, 3000), ("Subdurální", 50, 300), ("Měkkotkáňové", 40, 400), ("Krvácení", 75, 150)]
    text_postproces_upravy_10 = "- Po Vašem výběru se dotazové okno zavře a program začne vytvářet upravený obraz. Jakmile bude výsledný obraz hotový, tak Vás upozorní toto oznamovací okno:"
    text_postproces_upravy_11 = "Vlastní CT okno:"
    text_postproces_upravy_12 = "Aplikace umožňuje na obraz v uživatelském rozhraní použít i okno s vlastními parametry. Postup pro vytvoření vlastního CT okna je popsaný níže:"
    text_postproces_upravy_13 = "- Po zmáčknutí tlačítka VLASTNÍ na dotazovém oknu se objeví nové dotazové okno, do kterého je nutné zadat parametry vlastního CT okna. Úkazku dotazového okna pro vlastní CT okno si můžeto prohlédnout na následujícím obrázku:"
    text_postproces_upravy_14 = "- Do textových polí zadejte požadované číselné parametry nového CT okna. Nemusíte vyplňovat všechna textová pole, stačí zadat buď střed a šířku CT okna nebo horní a spodní hranici CT okna."
    text_postproces_upravy_15 = "- Pokud si přejete vymazat všechna textová pole, stačí zmáčknout tlačítko SMAZAT."
    text_postproces_upravy_16 = "- Jakmile jste s zadanými parametry spokojení, tak potvrďte vytváření vlastního CT okna. To provedete stisknutím tlačítka POUŽÍT ŠÍŘKU A VÝŠKU OKNA nebo tlačítkem POUŽÍT MAXIMUM A MINIMUM OKNA podle toho, z jakých vstupních parametrů chcete vlastní CT okno vytvořit."
    text_postproces_upravy_17 = "- Až bude výsledný obraz s vlastním CT oknem hotový, tak Vás upozorní toto oznamovací okno:"
    text_postproces_upravy_18 = "Odstranění CT okna:"
    text_postproces_upravy_19 = "Program neumožňuje jenom vytvářet CT okna a aplikovat je na obraz, ale také umí již aplikované CT okno z obrazu odstranit a zobrazit původní obraz. Postup pro resetovaní CT okna je následující:"
    text_postproces_upravy_20 = "- V dotazovém okně zmáčkněte tlačítko RESET."
    text_postproces_upravy_21 = "- Po odstranění aplikovaného CT okna se objeví toto oznamovací okno:"
    text_postproces_upravy_22 = "Upozornění: Obraz s CT oknem se po jeho vytvoření uloží do paměti programu, ale nezobrazí se v uživatelském rozhraní. Pro jeho zobrazení použijte tlačítko ZOBRAZIT pod tlačítkem CT OKNO."
    text_postproces_upravy_23 = "Zobrazit:"
    text_postproces_upravy_24 = "Tlačítko ZOBRAZIT se používá pro zobrazení obrazu s aplikovaným CT oknem nebo pro zobrazení původního obrazu, u kterého bylo CT okno odstraněno."

    # Nápověda k programu
    text_napoveda = "Nápověda k aplikaci:"
    text_napoveda_2 = "Nápověda slouží jako návod k používání této aplikace. Obsahuje i upozornění na méně intuitivní funkce programu a přehled jednotlivých kroků u složitějších funkcí."
    text_napoveda_3 = "Tlačítko pro spuštění nápovědy se nachází v pravém horním rohu uživatelského rozhraní a je označené nápisem NÁPOVĚDA."

    # Výběr anatomické roviny
    text_anatomic_rovina = "Výběr anatomické roviny:"
    text_anatomic_rovina_2 = "Tlačítka pro výběr anatomické roviny Vám poskytnou možnost přepínat u zobrazeného obrázku mezi 3 základními anatomickými rovinami. Program podporuje zobrazení v axiální, sagitální a koronální rovině. Program také hlídá zrovna používanou anatomickou rovinu a v případě změny vypíše do informačního panelu informaci o nové anatomické rovině."
    text_anatomic_rovina_3 = "Příslušná tlačítka se nachází ve sloupci na levé straně uživatelského rozhraní. Detail přepínání anatomických rovin je možné si prohlédnout na následujícím obrázku:"

    # Rychlé přepínání obrazů
    text_faze_obrazu = "Nabídka rychlého přepínání obrazů:"
    text_faze_obrazu_2 = "Nabídka tlačítek na pravé straně uživatelského rozhraní Vám poskytuje možnost rychlého přepínání mezi fázemi, ve kterých byl obraz nasnímán. Program umožňuje přepínat mezi těmito fázemi obrazu:"
    text_faze_obrazu_3 = ["Nativní snímek", "fáze CTA1", "fáze CTA2", "fáze CTA3", "Časová projekce"]
    text_faze_obrazu_4 = "Na obrázku vpravo se nachází nabídka rychlého přepínání obrazů v počátečním nastavení, zatímco na levém obrázku je tlačítko pro obraz CTA2 žluté, což značí, že se pracuje s CTA2 obrazem."
    text_faze_obrazu_5 = "Obraz není v paměti programu:"
    text_faze_obrazu_6 = "Pokud paměť programu neobsahuje příslušný obraz s požadovanou fází, tak Vás program požádá o nahrání obrazu do jeho paměti. To je možné provést pomocí následujícího postupu:"
    text_faze_obrazu_7 = "- Po zmáčknutí tlačítka s požadovanou fází se objeví dotazové okno, stejné jako na obrázku níže, které Vám umožní vybrat si formát nahrávaného souboru."
    text_faze_obrazu_8 = "- Po zobrazení této informační zprávy je obraz pro Vás připravený. Také se příslušné tlačítko v nabídce rychlého přepínaní obrazů zbarví dožluta, což označuje že se pracuje s touto fází obrazu."
    text_faze_obrazu_9 = "Upozornění: Po načtení obrazu pomocí rychlého přepínání obrazu se obraz nezobrazí v uživatelském rozhraní, ale pouze se nahraje do paměti aplikace. Pokud chcete načtený obraz zobrazit, musíte po načtení obrazu zmáčknout ještě jendou na tlačítko s příslušnou fází, aby se načtený obraz objevil v uživatelském rozhraní."
    text_faze_obrazu_10 = "Obraz de nachází v paměti programu:"
    text_faze_obrazu_11 = "Pokud paměť programu již obsahuje příslušný obraz s požadovanou fází, tak program automaticky požadovaný obraz vyhledá a zobrazí ho v uživatelském rozhraní. Také se příslušné tlačítko v nabídce rychlého přepínaní obrazů zbarví dožluta, což označuje že se pracuje s touto fází obrazu."

    # Změna řezu v obraze
    text_zmena_rezu = "Přepínání řezů v obraze:"
    text_zmena_rezu_2 = "Při CT snímání mozku vzniká 3D obraz. Abyste si mohli 3D obraz podrobně prohlédnout, tak je rozdělen do mnoha 2D řezů. Aplikace Vám tedy umožní přepínat mezi jednotlivými řezy obrazu 3 různými způsoby:"
    text_zmena_rezu_3 = ["posuvníkem s číslem řezu", "tlačítky vedle posuvníku", "levou a pravou šipkou na klávesnici"]
    text_zmena_rezu_4 = "Program také monitoruje pořadí zobrazeneného řezu v obraze a jeho číselnou hodnotu vypíše do informačního panelu. Při výměně obrazu za jiný nebo při přepnutí anatomické roviny se navíc rozsah posuvníku automaticky upraví."
    text_zmena_rezu_5 = "Posuvník a tlačítka pro přepínání na následující a předchozí řez se nachází ve spodní části uživatelského rozhraní. Detail posuvníku s příslušnými tlačítky je možné si prohlédnout na následujícím obrázku:"
    text_zmena_rezu_6 = "Upozornění: Po přepnutí obrazu do jiné anatomické roviny nebo při načtení nového obrazu se zobrazí 1. řez nového obrazu, ale posuvník zůstane na původní hodnotě předchozího obrazu. Tuto nesrovnalost lze snadno opravit tím, že přepnete řez obrazu. Tím se program přenastaví a zobrazí se nastavený řez současného obrazu."

    # Informační panel
    text_info_panel = "Informační panel:"
    text_info_panel_2 = "Na informačním panelu ve spodku uživatelského rozhraní můžete najít důležité informace o obrazu, se kterým pracujete. Program Vám poskytne tyto informace o obraze:"
    text_info_panel_3 = ["Použitá anatomická rovina", "Souřadnice kurzoru", "Pořadové číslo současného řezu"]
    text_info_panel_4 = "Program také kontroluje, s jakým obrazem se zrovna pracuje. Pokud pracujete s defaultním obrazem, tak jsou souřadnice kurzoru v pixelech. Jakmile ale v uživatelském rozhraní zobrazíte obraz, se kterým chcete pracovat, tak se souřadnice kurzoru automaticky začnou zobrazovat v milimetrech."
    text_info_panel_5 = "Obrázky informačního panelu s detailním záběrem na zobrazované informace o obrazu je možné si prohlédnout na obrázcích níže. Na následujících obrázcích si také můžete prohlédnout vypsané souřadnice kurzoru ve 2 variantách - souřadnice v pixelech a v milimetrech."

    # Okno před uzavřením programu
    text_uzavreni_programu = "Vypínání aplikace:"
    text_uzavreni_programu_2 = "Při práci v aplikaci Bolehlav můžou vznikat mnoho modifikovaných obrazů. Ty se ukládají do paměti programu, ze které se v případě nutnosti vyvolávají. Před vypnutím programu je proto nutné buď tuto paměť vymazat, nebo ji zachovat do dalšího otevření aplikace."
    text_uzavreni_programu_3 = "Abyste tedy mohli program správně vypnout, je nutné postupovat následovně:"
    text_uzavreni_programu_4 = "- Pro uzavření programu zmáčkněte tlačítko X v pravém horním rohu okna s aplikací."
    text_uzavreni_programu_5 = "- Poté se otevře dotazové okno, stejné jako na obrázku níže, které Vám nabídne možnost vymazání paměti programu."
    text_uzavreni_programu_6 = "- Pokud zvolíte tlačítko ANO, SMAZAT, tak dojde k vypnutí aplikace a zároveň se paměť programu vymaže."
    text_uzavreni_programu_7 = "- Jestliže si zvolíte tlačítko NE, ZACHOVAT, tak dojde pouze k vypnutí aplikace."
    text_uzavreni_programu_8 = "- Pokud zvolíte tlačítko ZRUŠIT, tak program zůstává otevřený a ani paměť programu se nevymaže."


    # Cesty k obrázkům, které jsou použité v nápovědě
    cesta_k_obrazku_prehledu = r"obrazky_GUI\napoveda_prehled.png"

    cesta_k_obrazku_sprava = r"obrazky_GUI\napoveda_sprava_tlacitka.png"
    cesta_k_obrazku_sprava_nacist = r"obrazky_GUI\napoveda_sprava_tlacitka_nacist.png"
    cesta_k_obrazku_sprava_nacist_2 = r"obrazky_GUI\napoveda_sprava_tlacitka_nacist_2.png"
    cesta_k_obrazku_sprava_ulozit = r"obrazky_GUI\napoveda_sprava_tlacitka_nacist_3.png"

    cesta_k_obrazku_prace_registrace = r"obrazky_GUI\napoveda_prace_s_obrazem_registrace.png"
    cesta_k_obrazku_prace_registrace_2 = r"obrazky_GUI\napoveda_prace_s_obrazem_registrace_2.png"
    cesta_k_obrazku_prace_registrace_3 = r"obrazky_GUI\napoveda_prace_s_obrazem_registrace_3.png"

    cesta_k_obrazku_prace = r"obrazky_GUI\napoveda_prace_s_obrazem.png"
    cesta_k_obrazku_prace_multifaze = r"obrazky_GUI\napoveda_prace_s_obrazem_multifaze.png"
    cesta_k_obrazku_prace_multifaze_2 = r"obrazky_GUI\napoveda_prace_s_obrazem_multifaze_2.png"

    cesta_k_obrazku_prace_manual_detekce = r"obrazky_GUI\napoveda_prace_s_obrazem_manual_detekce.png"
    cesta_k_obrazku_prace_manual_detekce_2 = r"obrazky_GUI\napoveda_prace_s_obrazem_manual_detekce_2.png"
    cesta_k_obrazku_prace_manual_detekce_3 = r"obrazky_GUI\napoveda_prace_s_obrazem_manual_detekce_3.png"
    cesta_k_obrazku_prace_manual_detekce_4 = r"obrazky_GUI\napoveda_prace_s_obrazem_manual_detekce_4.png"
    cesta_k_obrazku_prace_manual_detekce_5 = r"obrazky_GUI\napoveda_prace_s_obrazem_manual_detekce_5.png"
    cesta_k_obrazku_prace_manual_detekce_6 = r"obrazky_GUI\napoveda_prace_s_obrazem_manual_detekce_6.png"

    cesta_k_obrazku_postproces_upravy = r"obrazky_GUI\napoveda_postproces_upravy.png"
    cesta_k_obrazku_postproces_upravy_2 = r"obrazky_GUI\napoveda_postproces_upravy_2.png"
    cesta_k_obrazku_postproces_upravy_3 = r"obrazky_GUI\napoveda_postproces_upravy_3.png"
    cesta_k_obrazku_postproces_upravy_4 = r"obrazky_GUI\napoveda_postproces_upravy_4.png"
    cesta_k_obrazku_postproces_upravy_6 = r"obrazky_GUI\napoveda_postproces_upravy_6.png"

    cesta_k_obrazku_vyber_anatomic_roviny = r"obrazky_GUI\napoveda_vyber_anatomic_roviny.png"

    cesta_k_obrazku_faze_obrazu = r"obrazky_GUI\napoveda_faze_obrazu.png"

    cesta_k_obrazku_prepinani_rezu = r"obrazky_GUI\napoveda_prepinani_rezu.png"

    cesta_k_obrazku_info_panel = r"obrazky_GUI\napoveda_info_panel.png"
    cesta_k_obrazku_info_panel_2 = r"obrazky_GUI\napoveda_info_panel_2.png"
    cesta_k_obrazku_info_panel_3 = r"obrazky_GUI\napoveda_info_panel_3.png"

    cesta_k_obrazku_uzavreni_programu = r"obrazky_GUI\napoveda_uzavreni_programu.png"


    # Načítení obrázku do okna s nápovědou
    # Obrázek k přehledu uživatelského rozhraní
    obrazek_prehled = Image.open(cesta_k_obrazku_prehledu)
    obrazek_prehled_upraveny = obrazek_prehled.resize((450, 263))
    foto_prehled = ImageTk.PhotoImage(obrazek_prehled_upraveny)
    obrazek_prehled.image = foto_prehled

    # Obrázky k správě souborů
    obrazek_sprava = Image.open(cesta_k_obrazku_sprava)
    foto_sprava = ImageTk.PhotoImage(obrazek_sprava)
    obrazek_sprava.image = foto_sprava

    obrazek_sprava_nacist = Image.open(cesta_k_obrazku_sprava_nacist)
    obrazek_sprava_nacist_upraveny = obrazek_sprava_nacist.resize((450, 167))
    foto_sprava_nacist = ImageTk.PhotoImage(obrazek_sprava_nacist_upraveny)
    obrazek_sprava_nacist.image = foto_sprava_nacist

    obrazek_sprava_nacist_2 = Image.open(cesta_k_obrazku_sprava_nacist_2)
    foto_sprava_nacist_2 = ImageTk.PhotoImage(obrazek_sprava_nacist_2)
    obrazek_sprava_nacist_2.image = foto_sprava_nacist_2

    obrazek_sprava_ulozit = Image.open(cesta_k_obrazku_sprava_ulozit)
    obrazek_sprava_ulozit_upraveny = obrazek_sprava_ulozit.resize((450, 123))
    foto_sprava_ulozit = ImageTk.PhotoImage(obrazek_sprava_ulozit_upraveny)
    obrazek_sprava_ulozit.image = foto_sprava_ulozit

    # Obrázky k práci s obrazem
    obrazek_prace = Image.open(cesta_k_obrazku_prace)
    obrazek_prace_upraveny = obrazek_prace.resize((450, 63))
    foto_prace = ImageTk.PhotoImage(obrazek_prace_upraveny)
    obrazek_prace.image = foto_prace

    obrazek_prace_registrace = Image.open(cesta_k_obrazku_prace_registrace)
    obrazek_prace_registrace_upraveny = obrazek_prace_registrace.resize((450, 139))
    foto_prace_registrace = ImageTk.PhotoImage(obrazek_prace_registrace_upraveny)
    obrazek_prace_registrace.image = foto_prace_registrace

    obrazek_prace_registrace_2 = Image.open(cesta_k_obrazku_prace_registrace_2)
    obrazek_prace_registrace_2_upraveny = obrazek_prace_registrace_2.resize((450, 45))
    foto_prace_registrace_2 = ImageTk.PhotoImage(obrazek_prace_registrace_2_upraveny)
    obrazek_prace_registrace_2.image = foto_prace_registrace_2

    obrazek_prace_registrace_3 = Image.open(cesta_k_obrazku_prace_registrace_3)
    obrazek_prace_registrace_3_upraveny = obrazek_prace_registrace_3.resize((450, 73))
    foto_prace_registrace_3 = ImageTk.PhotoImage(obrazek_prace_registrace_3_upraveny)
    obrazek_prace_registrace_3.image = foto_prace_registrace_3

    obrazek_prace_multifaze = Image.open(cesta_k_obrazku_prace_multifaze)
    obrazek_prace_multifaze_upraveny = obrazek_prace_multifaze.resize((450, 172))
    foto_prace_multifaze = ImageTk.PhotoImage(obrazek_prace_multifaze_upraveny)
    obrazek_prace_multifaze.image = foto_prace_multifaze

    obrazek_prace_multifaze_2 = Image.open(cesta_k_obrazku_prace_multifaze_2)
    obrazek_prace_multifaze_2_upraveny = obrazek_prace_multifaze_2.resize((450, 53))
    foto_prace_multifaze_2 = ImageTk.PhotoImage(obrazek_prace_multifaze_2_upraveny)
    obrazek_prace_multifaze_2.image = foto_prace_multifaze_2

    obrazek_prace_manual_detekce = Image.open(cesta_k_obrazku_prace_manual_detekce)
    foto_prace_manual_detekce = ImageTk.PhotoImage(obrazek_prace_manual_detekce)
    obrazek_prace_manual_detekce.image = foto_prace_manual_detekce
    obrazek_prace_manual_detekce_2 = Image.open(cesta_k_obrazku_prace_manual_detekce_2)
    foto_prace_manual_detekce_2 = ImageTk.PhotoImage(obrazek_prace_manual_detekce_2)
    obrazek_prace_manual_detekce_2.image = foto_prace_manual_detekce_2
    obrazek_prace_manual_detekce_3 = Image.open(cesta_k_obrazku_prace_manual_detekce_3)
    foto_prace_manual_detekce_3 = ImageTk.PhotoImage(obrazek_prace_manual_detekce_3)
    obrazek_prace_manual_detekce_3.image = foto_prace_manual_detekce_3

    obrazek_prace_manual_detekce_4 = Image.open(cesta_k_obrazku_prace_manual_detekce_4)
    obrazek_prace_manual_detekce_4_upraveny = obrazek_prace_manual_detekce_4.resize((450, 451))
    foto_prace_manual_detekce_4 = ImageTk.PhotoImage(obrazek_prace_manual_detekce_4_upraveny)
    obrazek_prace_manual_detekce_4.image = foto_prace_manual_detekce_4

    obrazek_prace_manual_detekce_5 = Image.open(cesta_k_obrazku_prace_manual_detekce_5)
    obrazek_prace_manual_detekce_5_upraveny = obrazek_prace_manual_detekce_5.resize((450, 450))
    foto_prace_manual_detekce_5 = ImageTk.PhotoImage(obrazek_prace_manual_detekce_5_upraveny)
    obrazek_prace_manual_detekce_5.image = foto_prace_manual_detekce_5

    obrazek_prace_manual_detekce_6 = Image.open(cesta_k_obrazku_prace_manual_detekce_6)
    foto_prace_manual_detekce_6 = ImageTk.PhotoImage(obrazek_prace_manual_detekce_6)
    obrazek_prace_manual_detekce_6.image = foto_prace_manual_detekce_6

    # Obrázky k postrocessingovým úpravám (CT okno)
    obrazek_postproces_upravy = Image.open(cesta_k_obrazku_postproces_upravy)
    foto_postproces_upravy = ImageTk.PhotoImage(obrazek_postproces_upravy)
    obrazek_postproces_upravy.image = foto_postproces_upravy

    obrazek_postproces_upravy_2 = Image.open(cesta_k_obrazku_postproces_upravy_2)
    obrazek_postproces_upravy_2_upraveny = obrazek_postproces_upravy_2.resize((450, 228))
    foto_postproces_upravy_2 = ImageTk.PhotoImage(obrazek_postproces_upravy_2_upraveny)
    obrazek_postproces_upravy_2.image = foto_postproces_upravy_2

    obrazek_postproces_upravy_3 = Image.open(cesta_k_obrazku_postproces_upravy_3)
    foto_postproces_upravy_3 = ImageTk.PhotoImage(obrazek_postproces_upravy_3)
    obrazek_postproces_upravy_3.image = foto_postproces_upravy_3

    obrazek_postproces_upravy_4 = Image.open(cesta_k_obrazku_postproces_upravy_4)
    obrazek_postproces_upravy_4_upraveny = obrazek_postproces_upravy_4.resize((450, 175))
    foto_postproces_upravy_4 = ImageTk.PhotoImage(obrazek_postproces_upravy_4_upraveny)
    obrazek_postproces_upravy_4.image = foto_postproces_upravy_4

    obrazek_postproces_upravy_6 = Image.open(cesta_k_obrazku_postproces_upravy_6)
    foto_postproces_upravy_6 = ImageTk.PhotoImage(obrazek_postproces_upravy_6)
    obrazek_postproces_upravy_6.image = foto_postproces_upravy_6

    # Obrázek k výběru anatomických rovin
    obrazek_vyber_anatomic_roviny = Image.open(cesta_k_obrazku_vyber_anatomic_roviny)
    foto_vyber_anatomic_roviny = ImageTk.PhotoImage(obrazek_vyber_anatomic_roviny)
    obrazek_vyber_anatomic_roviny.image = foto_vyber_anatomic_roviny

    # Obrázek pro ryché přepínání mezi fázemi
    obrazek_faze_obrazu = Image.open(cesta_k_obrazku_faze_obrazu)
    foto_faze_obrazu = ImageTk.PhotoImage(obrazek_faze_obrazu)
    obrazek_faze_obrazu.image = foto_faze_obrazu

    # Obrázek pro přepínání řezů v obraze
    obrazek_prepinani_rezu = Image.open(cesta_k_obrazku_prepinani_rezu)
    obrazek_prepinani_rezu_upraveny = obrazek_prepinani_rezu.resize((450, 34))
    foto_prepinani_rezu = ImageTk.PhotoImage(obrazek_prepinani_rezu_upraveny)
    obrazek_prepinani_rezu.image = foto_prepinani_rezu

    # Obrázky pro informační panel
    obrazek_info_panel = Image.open(cesta_k_obrazku_info_panel)
    obrazek_info_panel_upraveny = obrazek_info_panel.resize((450, 32))
    foto_info_panel = ImageTk.PhotoImage(obrazek_info_panel_upraveny)
    obrazek_info_panel.image = foto_info_panel
    obrazek_info_panel_2 = Image.open(cesta_k_obrazku_info_panel_2)
    obrazek_info_panel_2_upraveny = obrazek_info_panel_2.resize((450, 30))
    foto_info_panel_2 = ImageTk.PhotoImage(obrazek_info_panel_2_upraveny)
    obrazek_info_panel_2.image = foto_info_panel_2
    obrazek_info_panel_3 = Image.open(cesta_k_obrazku_info_panel_3)
    obrazek_info_panel_3_upraveny = obrazek_info_panel_3.resize((450, 27))
    foto_info_panel_3 = ImageTk.PhotoImage(obrazek_info_panel_3_upraveny)
    obrazek_info_panel_3.image = foto_info_panel_3

    # Obrázky pro uzavírání programu
    obrazek_uzavreni_programu = Image.open(cesta_k_obrazku_uzavreni_programu)
    obrazek_uzavreni_programu_upraveny = obrazek_uzavreni_programu.resize((450, 190))
    foto_uzavreni_programu = ImageTk.PhotoImage(obrazek_uzavreni_programu_upraveny)
    obrazek_uzavreni_programu.image = foto_uzavreni_programu


    # Vytvoření a umístění textu s nadpisem do okna s nápovědou
    label_nadpis = tk.Label(vnitrni_scrollovatelny_ram, text=text_nadpis, font=("Arial", 20, "bold"), anchor="center")
    label_nadpis.grid(row=0, column=0, sticky=sticky_parametr_sloupec)
    label_nadpis_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_nadpis_2, font=("Arial", 12), anchor="center")
    label_nadpis_2.grid(row=1, column=0, sticky=sticky_parametr_sloupec)

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=2, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu s úvodem do okna s nápovědou
    label_text_uvod = tk.Label(vnitrni_scrollovatelny_ram, text=text_uvod, font=font_subnadpis)
    label_text_uvod.grid(row=3, column=0, sticky="w")
    label_text_uvod_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uvod_2, wraplength=sirka, justify="left")
    label_text_uvod_2.grid(row=4, column=0, sticky="w")
    label_text_uvod_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uvod_3, wraplength=sirka, justify="left")
    label_text_uvod_3.grid(row=5, column=0, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=6, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu a obrázků s přehledem uživatelského rozhraní do okna s nápovědou
    label_text_prehled = tk.Label(vnitrni_scrollovatelny_ram, text=text_prehled, font=font_subnadpis)
    label_text_prehled.grid(row=7, column=0, sticky="w")
    label_text_prehled_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prehled_2, wraplength=sirka, justify="left")
    label_text_prehled_2.grid(row=8, column=0, sticky="w")

    obrazek_prehled = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prehled)
    obrazek_prehled.grid(row=9, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=10, column=0, sticky=sticky_parametr_sloupec)

    # Umístění textu s výpisem seznamu, který obsahuje popisek GUI programu
    label_text_prehled_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prehled_3, wraplength=sirka, justify="left")
    label_text_prehled_3.grid(row=11, column=0, sticky="w")

    for index in range(0, len(seznam_bodu_prehled)):
        label_text_prehled_4 = tk.Label(vnitrni_scrollovatelny_ram, text=f"{index + 1}. " + f"{seznam_bodu_prehled[index]}",
                                        wraplength=(sirka - 20), justify="left")
        label_text_prehled_4.grid(row=(12 + index), column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=20, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu a obrázku se správou obrazu
    label_text_sprava_obrazu = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu, font=font_subnadpis)
    label_text_sprava_obrazu.grid(row=21, column=0, sticky="w")
    label_text_sprava_obrazu_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_2, wraplength=sirka, justify="left")
    label_text_sprava_obrazu_2.grid(row=22, column=0, sticky="w")

    obrazek_sprava = tk.Label(vnitrni_scrollovatelny_ram, image=foto_sprava)
    obrazek_sprava.grid(row=23, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=24, column=0, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění textu a obrázků o tlačítku Načíst
    label_text_sprava_obrazu_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_3, font=font_subsubnadpis)
    label_text_sprava_obrazu_3.grid(row=25, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_4, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_4.grid(row=26, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_5, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_5.grid(row=27, column=0, padx=20, sticky="w")

    obrazek_sprava_nacist = tk.Label(vnitrni_scrollovatelny_ram, image=foto_sprava_nacist)
    obrazek_sprava_nacist.grid(row=28, column=0, sticky="snew")

    label_text_sprava_obrazu_6 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_6, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_6.grid(row=29, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_7 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_7, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_7.grid(row=30, column=0, padx=20, sticky="w")

    obrazek_sprava_nacist_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_sprava_nacist_2)
    obrazek_sprava_nacist_2.grid(row=31, column=0, sticky="snew")

    label_text_sprava_obrazu_8 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_8, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_8.grid(row=32, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=33, column=0, sticky=sticky_parametr_sloupec)

    label_text_sprava_obrazu_9 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_9, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_9.grid(row=34, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=35, column=0, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění textu a obrázků o tlačítku Zobrazit
    label_text_sprava_obrazu_10 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_10, font=font_subsubnadpis)
    label_text_sprava_obrazu_10.grid(row=36, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_11 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_11, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_11.grid(row=37, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=38, column=0, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění textu a obrázků o tlačítku Uložit
    label_text_sprava_obrazu_12 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_12, font=font_subsubnadpis)
    label_text_sprava_obrazu_12.grid(row=39, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_13 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_13, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_13.grid(row=40, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_14 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_14, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_14.grid(row=41, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_15 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_15, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_15.grid(row=42, column=0, padx=20, sticky="w")

    obrazek_sprava_nacist_3 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_sprava_ulozit)
    obrazek_sprava_nacist_3.grid(row=43, column=0, sticky="snew")

    label_text_sprava_obrazu_16 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_16, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_16.grid(row=44, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=45, column=0, sticky=sticky_parametr_sloupec)

    # Vytvoření a umístění textu a obrázků o tlačítku Smazat
    label_text_sprava_obrazu_17 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_17, font=font_subsubnadpis)
    label_text_sprava_obrazu_17.grid(row=46, column=0, padx=20, sticky="w")
    label_text_sprava_obrazu_18 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_18, wraplength=(sirka - 20), justify="left")
    label_text_sprava_obrazu_18.grid(row=47, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=48, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu s úpravami a prací s načteným obrazem
    label_text_prace_s_obrazem = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem, font=font_subnadpis)
    label_text_prace_s_obrazem.grid(row=49, column=0, sticky="w")
    label_text_prace_s_obrazem_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_2, wraplength=sirka, justify="left")
    label_text_prace_s_obrazem_2.grid(row=50, column=0, sticky="w")
    label_text_prace_s_obrazem_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_3, wraplength=sirka, justify="left")
    label_text_prace_s_obrazem_3.grid(row=51, column=0, sticky="w")

    obrazek_prace = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace)
    obrazek_prace.grid(row=52, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=53, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda k registraci
    label_text_prace_s_obrazem_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_4, font=font_subsubnadpis)
    label_text_prace_s_obrazem_4.grid(row=54, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_5, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_5.grid(row=55, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_6 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_6, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_6.grid(row=56, column=0, padx=20, sticky="w")

    obrazek_prace_registrace = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_registrace)
    obrazek_prace_registrace.grid(row=57, column=0, sticky="snew")

    label_text_prace_s_obrazem_7 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_7, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_7.grid(row=58, column=0, padx=20, sticky="w")

    for index in range(0, 4):
        label_text_prace_s_obrazem_8 = tk.Label(vnitrni_scrollovatelny_ram, text=f"{index + 1}. " + f"{text_prace_s_obrazem_8[index]}", wraplength=(sirka - 40), justify="left")
        label_text_prace_s_obrazem_8.grid(row=(59 + index), column=0, padx=40, sticky="w")

    label_text_prace_s_obrazem_9 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_9, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_9.grid(row=63, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_10 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_10, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_10.grid(row=64, column=0, padx=20, sticky="w")

    obrazek_prace_registrace_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_registrace_2)
    obrazek_prace_registrace_2.grid(row=65, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=66, column=0, sticky=sticky_parametr_sloupec)

    label_text_prace_s_obrazem_11 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_11, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_11.grid(row=67, column=0, padx=20, sticky="w")

    obrazek_prace_registrace_3 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_registrace_3)
    obrazek_prace_registrace_3.grid(row=68, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=69, column=0, sticky=sticky_parametr_sloupec)

    label_text_prace_s_obrazem_12 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_12, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_12.grid(row=70, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_13 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_13, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_13.grid(row=71, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=72, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda k tvorbě obrazů časové projekce maximální intenzity
    label_text_prace_s_obrazem_14 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_14, font=font_subsubnadpis)
    label_text_prace_s_obrazem_14.grid(row=73, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_15 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_15, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_15.grid(row=74, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_16 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_16, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_16.grid(row=75, column=0, padx=20, sticky="w")

    obrazek_prace_multifaze = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_multifaze)
    obrazek_prace_multifaze.grid(row=76, column=0, sticky="snew")

    label_text_prace_s_obrazem_17 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_17, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_17.grid(row=77, column=0, padx=20, sticky="w")

    for index in range(0, 3):
        label_text_prace_s_obrazem_18 = tk.Label(vnitrni_scrollovatelny_ram, text=f"{index + 1}. " + f"{text_prace_s_obrazem_18[index]}", wraplength=(sirka - 40), justify="left")
        label_text_prace_s_obrazem_18.grid(row=(78 + index), column=0, padx=40, sticky="w")

    label_text_prace_s_obrazem_19 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_19, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_19.grid(row=81, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_20 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_20, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_20.grid(row=82, column=0, padx=20, sticky="w")

    label_text_prace_s_obrazem_21 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_21, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_21.grid(row=83, column=0, padx=20, sticky="w")

    obrazek_prace_multifaze_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_multifaze_2)
    obrazek_prace_multifaze_2.grid(row=84, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=85, column=0, sticky=sticky_parametr_sloupec)

    label_text_prace_s_obrazem_22 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_22, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_22.grid(row=86, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=87, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda k manuální detekci
    label_text_prace_s_obrazem_23 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_23, font=font_subsubnadpis)
    label_text_prace_s_obrazem_23.grid(row=88, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_24 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_24, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_24.grid(row=89, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_25 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_25, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_25.grid(row=90, column=0, padx=20, sticky="w")

    obrazek_prace_manual_detekce = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_manual_detekce)
    obrazek_prace_manual_detekce.grid(row=91, column=0, sticky="nsew")
    obrazek_prace_manual_detekce_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_manual_detekce_2)
    obrazek_prace_manual_detekce_2.grid(row=92, column=0, sticky="nsew")
    obrazek_prace_manual_detekce_3 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_manual_detekce_3)
    obrazek_prace_manual_detekce_3.grid(row=93, column=0, sticky="nsew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=94, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda při bílém stavu tlačítka MANUÁLNÍ DETEKCE
    label_text_prace_s_obrazem_26 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_26, font=font_subsubnadpis)
    label_text_prace_s_obrazem_26.grid(row=95, column=0, padx=40, sticky="w")
    label_text_prace_s_obrazem_27 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_27, wraplength=(sirka - 40), justify="left")
    label_text_prace_s_obrazem_27.grid(row=96, column=0, padx=40, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=97, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda při žlutém stavu tlačítka MANUÁLNÍ DETEKCE
    label_text_prace_s_obrazem_28 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_28, font=font_subsubnadpis)
    label_text_prace_s_obrazem_28.grid(row=98, column=0, padx=40, sticky="w")
    label_text_prace_s_obrazem_29 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_29, wraplength=(sirka - 40), justify="left")
    label_text_prace_s_obrazem_29.grid(row=99, column=0, padx=40, sticky="w")

    obrazek_prace_manual_detekce_4 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_manual_detekce_4)
    obrazek_prace_manual_detekce_4.grid(row=100, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=101, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda při oranžovém stavu tlačítka MANUÁLNÍ DETEKCE
    label_text_prace_s_obrazem_30 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_30, font=font_subsubnadpis)
    label_text_prace_s_obrazem_30.grid(row=102, column=0, padx=40, sticky="w")
    label_text_prace_s_obrazem_31 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_31, wraplength=(sirka - 40), justify="left")
    label_text_prace_s_obrazem_31.grid(row=103, column=0, padx=40, sticky="w")

    obrazek_prace_manual_detekce_5 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_manual_detekce_5)
    obrazek_prace_manual_detekce_5.grid(row=104, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=105, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítka ZOBRAZIT pod tlačítky REGISTRACE a ČASOVÁ PROJEKCE
    label_text_prace_s_obrazem_32 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_32, font=font_subsubnadpis)
    label_text_prace_s_obrazem_32.grid(row=106, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_33 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_33, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_33.grid(row=107, column=0, padx=20, sticky="w")

    label_text_prace_s_obrazem_34 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_34, wraplength=(sirka - 40), justify="left")
    label_text_prace_s_obrazem_34.grid(row=108, column=0, padx=40, sticky="w")
    label_text_prace_s_obrazem_35 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_35, wraplength=(sirka - 40), justify="left")
    label_text_prace_s_obrazem_35.grid(row=109, column=0, padx=40, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=110, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítko SMAZAT pod tlačítkem MANUÁLNÍ DETEKCE
    label_text_prace_s_obrazem_36 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_36, font=font_subsubnadpis)
    label_text_prace_s_obrazem_36.grid(row=111, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_37 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_37, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_37.grid(row=112, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=113, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítko ULOŽIT pod tlačítkem MANUÁLNÍ DETEKCE
    label_text_prace_s_obrazem_38 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_38, font=font_subsubnadpis)
    label_text_prace_s_obrazem_38.grid(row=114, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_39 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_39, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_39.grid(row=115, column=0, padx=20, sticky="w")
    label_text_prace_s_obrazem_40 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_40, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_40.grid(row=116, column=0, padx=20, sticky="w")

    for index in range(0, len(text_prace_s_obrazem_41)):
        label_text_prace_s_obrazem_41 = tk.Label(vnitrni_scrollovatelny_ram, text=f"{index + 1}. {text_prace_s_obrazem_41[index]}", wraplength=(sirka - 40), justify="left")
        label_text_prace_s_obrazem_41.grid(row=(117 + index), column=0, padx=40, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=121, column=0, sticky=sticky_parametr_sloupec)

    label_text_prace_s_obrazem_42 = tk.Label(vnitrni_scrollovatelny_ram, text=text_prace_s_obrazem_42, wraplength=(sirka - 20), justify="left")
    label_text_prace_s_obrazem_42.grid(row=122, column=0, padx=20, sticky="w")

    obrazek_prace_manual_detekce_6 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prace_multifaze_2)
    obrazek_prace_manual_detekce_6.grid(row=123, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=124, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu s postprocessingovými úpravami obrazu
    label_text_postproces_upravy = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy, font=font_subnadpis)
    label_text_postproces_upravy.grid(row=125, column=0, sticky="w")
    label_text_postproces_upravy_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_2, wraplength=sirka, justify="left")
    label_text_postproces_upravy_2.grid(row=126, column=0, sticky="w")

    obrazek_postproces_upravy = tk.Label(vnitrni_scrollovatelny_ram, image=foto_postproces_upravy)
    obrazek_postproces_upravy.grid(row=127, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=128, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítko CT OKNO
    label_text_postproces_upravy_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_3, font=font_subsubnadpis)
    label_text_postproces_upravy_3.grid(row=129, column=0, padx=20, sticky="w")
    label_text_postproces_upravy_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_4, wraplength=(sirka - 20), justify="left")
    label_text_postproces_upravy_4.grid(row=130, column=0, padx=20, sticky="w")
    label_text_postproces_upravy_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_5, wraplength=(sirka - 20), justify="left")
    label_text_postproces_upravy_5.grid(row=131, column=0, padx=20, sticky="w")
    label_text_postproces_upravy_6 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_6, wraplength=(sirka - 20), justify="left")
    label_text_postproces_upravy_6.grid(row=132, column=0, padx=20, sticky="w")

    obrazek_postproces_upravy_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_postproces_upravy_2)
    obrazek_postproces_upravy_2.grid(row=133, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=134, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítka předpřipravených CT oknen
    label_text_postproces_upravy_7 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_7, font=font_subsubnadpis)
    label_text_postproces_upravy_7.grid(row=135, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_8 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_8, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_8.grid(row=136, column=0, padx=40, sticky="w")

    # Tabulka s parametry předpřipravených CT oken
    styl = ttk.Style()
    styl.configure("Treeview.Heading", anchor="center")

    tabulka_postproces_upravy = ttk.Treeview(vnitrni_scrollovatelny_ram, columns=("okno", "stred", "sirka"), show="headings", height=len(text_postproces_upravy_9))
    tabulka_postproces_upravy.grid(row=137, column=0)

    tabulka_postproces_upravy.heading("okno", text="CT okno")
    tabulka_postproces_upravy.heading("stred", text="střed okna [HU]")
    tabulka_postproces_upravy.heading("sirka", text="šířka okna [HU]")

    tabulka_postproces_upravy.column("okno", anchor="center", width=100)
    tabulka_postproces_upravy.column("stred", anchor="center", width=100)
    tabulka_postproces_upravy.column("sirka", anchor="center", width=100)

    for radek in text_postproces_upravy_9:
        tabulka_postproces_upravy.insert("", tk.END, values=radek)
    # Tabulka s parametry předpřipravených CT oken - konec

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=138, column=0, sticky=sticky_parametr_sloupec)

    label_text_postproces_upravy_10 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_10, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_10.grid(row=139, column=0, padx=40, sticky="w")

    obrazek_postproces_upravy_3 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_postproces_upravy_3)
    obrazek_postproces_upravy_3.grid(row=140, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=141, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítko s vlastním CT oknem
    label_text_postproces_upravy_11 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_11, font=font_subsubnadpis)
    label_text_postproces_upravy_11.grid(row=142, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_12 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_12, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_12.grid(row=143, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_13 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_13, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_13.grid(row=144, column=0, padx=40, sticky="w")

    obrazek_postproces_upravy_4 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_postproces_upravy_4)
    obrazek_postproces_upravy_4.grid(row=145, column=0, sticky="snew")

    label_text_postproces_upravy_14 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_14, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_14.grid(row=146, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_15 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_15, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_15.grid(row=147, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_16 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_16, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_16.grid(row=148, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_17 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_17, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_17.grid(row=149, column=0, padx=40, sticky="w")

    obrazek_postproces_upravy_5 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_postproces_upravy_3)
    obrazek_postproces_upravy_5.grid(row=150, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=151, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítko s resetem CT okna
    label_text_postproces_upravy_18 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_18, font=font_subsubnadpis)
    label_text_postproces_upravy_18.grid(row=152, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_19 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_19, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_19.grid(row=153, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_20 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_20, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_20.grid(row=154, column=0, padx=40, sticky="w")
    label_text_postproces_upravy_21 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_21, wraplength=(sirka - 40), justify="left")
    label_text_postproces_upravy_21.grid(row=155, column=0, padx=40, sticky="w")

    obrazek_postproces_upravy_6 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_postproces_upravy_6)
    obrazek_postproces_upravy_6.grid(row=156, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=157, column=0, sticky=sticky_parametr_sloupec)

    label_text_postproces_upravy_22 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_22, wraplength=(sirka - 20), justify="left")
    label_text_postproces_upravy_22.grid(row=158, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=159, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro tlačítko ZOBRAZIT pod tlačítkem CT OKNO
    label_text_postproces_upravy_23 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_23, font=font_subsubnadpis)
    label_text_postproces_upravy_23.grid(row=160, column=0, padx=20, sticky="w")
    label_text_postproces_upravy_24 = tk.Label(vnitrni_scrollovatelny_ram, text=text_postproces_upravy_24, wraplength=(sirka - 20), justify="left")
    label_text_postproces_upravy_24.grid(row=161, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=162, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu s nápovědou k programu
    label_text_napoveda = tk.Label(vnitrni_scrollovatelny_ram, text=text_napoveda, font=font_subnadpis)
    label_text_napoveda.grid(row=163, column=0, sticky="w")
    label_text_napoveda_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_napoveda_2, wraplength=sirka, justify="left")
    label_text_napoveda_2.grid(row=164, column=0, sticky="w")
    label_text_napoveda_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_napoveda_3, wraplength=sirka, justify="left")
    label_text_napoveda_3.grid(row=165, column=0, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=166, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu s výběrem anatomické roviny
    label_text_vyber_anatomic_roviny = tk.Label(vnitrni_scrollovatelny_ram, text=text_anatomic_rovina, font=font_subnadpis)
    label_text_vyber_anatomic_roviny.grid(row=167, column=0, sticky="w")
    label_text_vyber_anatomic_roviny_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_anatomic_rovina_2, wraplength=sirka, justify="left")
    label_text_vyber_anatomic_roviny_2.grid(row=168, column=0, sticky="w")
    label_text_vyber_anatomic_roviny_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_anatomic_rovina_3, wraplength=sirka, justify="left")
    label_text_vyber_anatomic_roviny_3.grid(row=169, column=0, sticky="w")

    obrazek_vyber_anatomic_roviny = tk.Label(vnitrni_scrollovatelny_ram, image=foto_vyber_anatomic_roviny)
    obrazek_vyber_anatomic_roviny.grid(row=170, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=171, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu pro rychlý výběr fáze obrazu
    label_text_vyber_faze_obrazu = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu, font=font_subnadpis)
    label_text_vyber_faze_obrazu.grid(row=172, column=0, sticky="w")
    label_text_vyber_faze_obrazu_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_2, wraplength=sirka, justify="left")
    label_text_vyber_faze_obrazu_2.grid(row=173, column=0, sticky="w")

    for index in range(0, len(text_faze_obrazu_3)):
        label_text_vyber_faze_obrazu_3 = tk.Label(vnitrni_scrollovatelny_ram, text=f"{index + 1}. {text_faze_obrazu_3[index]}", wraplength=sirka, justify="left")
        label_text_vyber_faze_obrazu_3.grid(row=(174 + index), column=0, padx=20, sticky="w")

    label_text_vyber_faze_obrazu_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_4, wraplength=sirka, justify="left")
    label_text_vyber_faze_obrazu_4.grid(row=179, column=0, sticky="w")

    obrazek_faze_obrazu = tk.Label(vnitrni_scrollovatelny_ram, image=foto_faze_obrazu)
    obrazek_faze_obrazu.grid(row=180, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=181, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro rychlý výběr fáze obrazu (když program nenajde daný obraz)
    label_text_vyber_faze_obrazu_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_5, font=font_subsubnadpis)
    label_text_vyber_faze_obrazu_5.grid(row=182, column=0, padx=20, sticky="w")
    label_text_vyber_faze_obrazu_6 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_6, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_6.grid(row=183, column=0, padx=20, sticky="w")
    label_text_vyber_faze_obrazu_7 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_7, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_7.grid(row=184, column=0, padx=20, sticky="w")

    obrazek_faze_obrazu_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_sprava_nacist)
    obrazek_faze_obrazu_2.grid(row=185, column=0, sticky="snew")

    label_text_vyber_faze_obrazu_8 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_6, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_8.grid(row=186, column=0, padx=20, sticky="w")
    label_text_vyber_faze_obrazu_9 = tk.Label(vnitrni_scrollovatelny_ram, text=text_sprava_obrazu_7, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_9.grid(row=187, column=0, padx=20, sticky="w")

    obrazek_faze_obrazu_3 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_sprava_nacist_2)
    obrazek_faze_obrazu_3.grid(row=188, column=0, sticky="snew")

    label_text_vyber_faze_obrazu_10 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_8, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_10.grid(row=189, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=190, column=0, sticky=sticky_parametr_sloupec)

    label_text_vyber_faze_obrazu_11 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_9, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_11.grid(row=191, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=192, column=0, sticky=sticky_parametr_sloupec)

    # Nápověda pro rychlý výběr fáze obrazu (když program nenajde daný obraz)
    label_text_vyber_faze_obrazu_12 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_10, font=font_subsubnadpis)
    label_text_vyber_faze_obrazu_12.grid(row=193, column=0, padx=20, sticky="w")
    label_text_vyber_faze_obrazu_13 = tk.Label(vnitrni_scrollovatelny_ram, text=text_faze_obrazu_11, wraplength=(sirka - 20), justify="left")
    label_text_vyber_faze_obrazu_13.grid(row=194, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=195, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu popisující přepínání řezu v obraze
    label_text_prepinani_rezu = tk.Label(vnitrni_scrollovatelny_ram, text=text_zmena_rezu, font=font_subnadpis)
    label_text_prepinani_rezu.grid(row=196, column=0, sticky="w")
    label_text_prepinani_rezu_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_zmena_rezu_2, wraplength=sirka, justify="left")
    label_text_prepinani_rezu_2.grid(row=197, column=0, sticky="w")

    for index in range(0, len(text_zmena_rezu_3)):
        label_text_prepinani_rezu_3 = tk.Label(vnitrni_scrollovatelny_ram, text=f"- {text_zmena_rezu_3[index]}", wraplength=(sirka - 20), justify="left")
        label_text_prepinani_rezu_3.grid(row=(198 + index), column=0, padx=20, sticky="w")

    label_text_prepinani_rezu_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_zmena_rezu_4, wraplength=sirka, justify="left")
    label_text_prepinani_rezu_4.grid(row=201, column=0, sticky="w")
    label_text_prepinani_rezu_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_zmena_rezu_5, wraplength=sirka, justify="left")
    label_text_prepinani_rezu_5.grid(row=202, column=0, sticky="w")

    obrazek_prepinani_rezu = tk.Label(vnitrni_scrollovatelny_ram, image=foto_prepinani_rezu)
    obrazek_prepinani_rezu.grid(row=203, column=0, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=204, column=0, sticky=sticky_parametr_sloupec)

    label_text_prepinani_rezu_6 = tk.Label(vnitrni_scrollovatelny_ram, text=text_zmena_rezu_6, wraplength=sirka, justify="left")
    label_text_prepinani_rezu_6.grid(row=205, column=0, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=206, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu s informačním panelem
    label_text_informacni_panel = tk.Label(vnitrni_scrollovatelny_ram, text=text_info_panel, font=font_subnadpis)
    label_text_informacni_panel.grid(row=207, column=0, sticky="w")
    label_text_informacni_panel_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_info_panel_2, wraplength=sirka, justify="left")
    label_text_informacni_panel_2.grid(row=208, column=0, sticky="w")

    for index in range(0, len(text_info_panel_3)):
        label_text_informacni_panel_3 = tk.Label(vnitrni_scrollovatelny_ram, text=f"- {text_info_panel_3[index]}", wraplength=(sirka - 20), justify="left")
        label_text_informacni_panel_3.grid(row=(209 + index), column=0, padx=20, sticky="w")

    label_text_informacni_panel_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_info_panel_4, wraplength=sirka, justify="left")
    label_text_informacni_panel_4.grid(row=212, column=0, sticky="w")
    label_text_informacni_panel_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_info_panel_5, wraplength=sirka, justify="left")
    label_text_informacni_panel_5.grid(row=213, column=0, sticky="w")

    obrazek_info_panel = tk.Label(vnitrni_scrollovatelny_ram, image=foto_info_panel)
    obrazek_info_panel.grid(row=214, column=0, pady=2, sticky="snew")
    obrazek_info_panel_2 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_info_panel_2)
    obrazek_info_panel_2.grid(row=215, column=0, pady=2, sticky="snew")
    obrazek_info_panel_3 = tk.Label(vnitrni_scrollovatelny_ram, image=foto_info_panel_3)
    obrazek_info_panel_3.grid(row=216, column=0, pady=2, sticky="snew")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=217, column=0, sticky=sticky_parametr_sloupec)


    # Vytvoření a umístění textu o uzavíraní programu
    label_text_uzavreni_programu = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu, font=font_subnadpis)
    label_text_uzavreni_programu.grid(row=218, column=0, sticky="w")
    label_text_uzavreni_programu_2 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_2, wraplength=sirka, justify="left")
    label_text_uzavreni_programu_2.grid(row=219, column=0, sticky="w")
    label_text_uzavreni_programu_3 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_3, wraplength=sirka, justify="left")
    label_text_uzavreni_programu_3.grid(row=220, column=0, sticky="w")
    label_text_uzavreni_programu_4 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_4, wraplength=(sirka - 20), justify="left")
    label_text_uzavreni_programu_4.grid(row=221, column=0, padx=20, sticky="w")
    label_text_uzavreni_programu_5 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_5, wraplength=(sirka - 20), justify="left")
    label_text_uzavreni_programu_5.grid(row=222, column=0, padx=20, sticky="w")

    obrazek_uzavreni_programu = tk.Label(vnitrni_scrollovatelny_ram, image=foto_uzavreni_programu)
    obrazek_uzavreni_programu.grid(row=223, column=0, sticky="snew")

    label_text_uzavreni_programu_6 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_6, wraplength=(sirka - 20), justify="left")
    label_text_uzavreni_programu_6.grid(row=224, column=0, padx=20, sticky="w")
    label_text_uzavreni_programu_7 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_7, wraplength=(sirka - 20), justify="left")
    label_text_uzavreni_programu_7.grid(row=225, column=0, padx=20, sticky="w")
    label_text_uzavreni_programu_8 = tk.Label(vnitrni_scrollovatelny_ram, text=text_uzavreni_programu_8, wraplength=(sirka - 20), justify="left")
    label_text_uzavreni_programu_8.grid(row=226, column=0, padx=20, sticky="w")

    label_mezera = tk.Label(vnitrni_scrollovatelny_ram)
    label_mezera.grid(row=227, column=0, sticky=sticky_parametr_sloupec)


    # Hlavní smyčka okna pro nápovědu
    okno_napoveda.mainloop()
