#helper
import os

# erzeugt eine Einrückung für die Darstellung
def einrueckung():
    print("  ", end="")

# erzeugt Tabs für die Darstellung einer Tabelle
def printTabs(anzahl):
    _str = "\r"
    for _ in range(0,anzahl):
        _str += "\t"
    print(_str,end="")

# löscht die Anzeige im Terminal
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# ersetzt in eienr Zeichenkette eine Liste von Strings durch eine definierte Zeichenkette
def replaceMultiple(string,toReplace,_with):
    for rep in toReplace : string = string.replace(rep,_with)
    return string

# erfragt vom Anwender eine Zahl
# hält ihn bis zur korrekten Eingabe in einer Schleife
def inputTillInt(text):
    userInput = ""
    while not isinstance(userInput, int):
        try:userInput = int(input(text))
        except:userInput = ""
    return userInput

# erfragt vom Anwender eine erlaubte Zeichenkette 
# hält ihn bis zur korrekten Eingabe in einer Schleife
def inputTillAllowed(allowed,text):
    userInput = ""
    while userInput not in allowed:
        userInput = input(text)
    return userInput

# konvertiert einen Float Wert in einen String mit vorgegebener Genauigkeit
def floatStringWithPrecision(_float,precision):
    return '%.*f' % (precision, _float) 





# string.center(15) --> 15 Zeichen langer String,bei dem der stringInhalt zentriert ist
# string.ljust(15) string.rjust(15) --> 15 Zeichen langer String,bei dem der stringInhalt rechts bzw. linksbündig ist
# string.endswith("a") // startswith("a")
# string.find("a") --> Rückgabe index
# string.lower() .upper() .islower() .isupper()
# string.split(".") - zerteilt in Teilstrings - zwischen "."

# a,b,c,d = string.split(".") --> weist a,b,c,d die Teilstrings zu
