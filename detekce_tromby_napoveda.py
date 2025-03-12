# Knihovny potřebné pro chod nápovědy GUI
import tkinter as tk


# Funkce, která vytváří okno s nápovědou k aplikaci pro uživatele
def napoveda():
    # Základní parametry pro vytvoření okna s nápovědou
    okno_napoveda = tk.Tk()
    okno_napoveda.title("Nápověda k programu")
    okno_napoveda.geometry("350x100")

    # Text, který bude nápověda obsahovat
    text_napovedy = "Toto okno bude obsahovat nápovědu k programu."

    # Vytvoření a umístění textu nápovědy do okna s nápovědou
    text_napovedy = tk.Label(okno_napoveda, text=text_napovedy)
    text_napovedy.pack()

    # Hlavní smyčka okna s nápovědou
    okno_napoveda.mainloop()
