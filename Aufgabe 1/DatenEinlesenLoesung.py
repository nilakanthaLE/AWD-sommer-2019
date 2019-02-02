import csv
import helper
from functools import reduce

#dritter Ansatz
# Datenblock wird durch explizite Angabe der Anzahl von cols und rows für die Beschreibung eingegrenzt

#Der dritte Ansatz hat sich als der effizienteste herausgestellt
# Leider sind die Daten der verschiedenen Tabellen so unterschiedlich, dass eine rein automatisierte Transformation kaum möglich erschien
# deshalb habe ich mich entschlossen, mindestens die Anzahl der Reihen und Spalten vor dem Datenblock "manuell" zu erfassen

#Methode,
# die Kommas in Strings durch Punkt ersetzt
# falls Klammern vorhanden sind, werden diese entfernt und dies im Rückgabetupel markiert
# @param string: der zu transformierende string
# @param allowedStrings: eine Liste erlaubter Strings
def deleteAndReplace(string,allowedStrings):
    string      = string.replace(",",".")
    hasBrackets = False
    if ("(" in string) or ("[" in string):
        hasBrackets = True
        string = string.replace("(","").replace("[","").replace(")","").replace("]","")
    return (string,hasBrackets)

#Methode, die:
# Strings wenn möglich in floatValues konvertiert
# wo das nicht möglich ist, wird entweder ein leerstring zurück angegeben
# oder falls der Strings in der Liste erlaubter Strings ist, wird dieser zurückgegeben
# floatValues in Klammern werden als solche gekennzeichnet
#@param string: die zu bearbeitende Zeichenkette
#@param allowedStrings: erlaubte Zeichen in Daten - z.B. *
def convertToFloatAndFilterAllowedStrings(string,allowedStrings):
    stringBrackets = deleteAndReplace(string,allowedStrings)
    string = stringBrackets[0]
    hasBrackets = stringBrackets[1]
    try:
        value = float(string)
        return (value,"()") if hasBrackets else value
    except:
        return string if string in allowedStrings else ""

#Methode, die:
# 1) die Daten einer übergebenen Reihe in Floats oder erlaubte strings konvertiert
def cleanRow(row,allowedStrings):
    row = list(map(lambda cell:convertToFloatAndFilterAllowedStrings(cell,allowedStrings),row))
    return row

#notwendige Helfermethoden für findLastDataCol(rows)
def convertToFloat(string):
    try:return float(string)
    except: return(string)
def stringIsFloat(string):
    return isinstance(convertToFloat(string),float)
def helpFindLastDataCol(eins,zwei):
    return zwei[0] if stringIsFloat(zwei[1]) else eins

#Methode,
# die ermittelt in welcher Spalte in allen Reihen sich der letzte (Zahlen)Wert befindet
# @param rows: das zu untersuchende Set an Rows
def findLastDataCol(rows):
    def lastDataColForRow(row):
        return reduce((lambda a,b:helpFindLastDataCol(a,b)),enumerate(row),0)
    lastDataCols = list(map(lambda row: lastDataColForRow(row),rows))
    return reduce(lambda a,b : a if a>=b else b,lastDataCols)

#Methode,
# die alle leeren Strings in einer Reihe herausfiltert
# @param row: die zu filterende Reihe
def filterLeerIn(row):
    return list(filter(lambda cell: cell != "",row))

#Methode,
# die den Datenblock isoliert, ihn säubert (nur floats,erlaubteStrings,floats in Klammern, leerStrings) und zurück gibt
# @param allowedStrings: erlaubte Strings, die im Datenblock auftauchen dürfen, die keine Floats stringsToDelete
# @param descCols: Anzahl der Spalten in der css für Beschreibung (Reihenbeschriftung)
# @param descRows: Anzahl der Reihen in der css für Beschreibung (Spaltenbeschriftung)
# @param rows: das Set an Datenreihen aus der css
def getData(allowedStrings,descCols,descRows,rows):
    rows    = list(map(lambda row:row[descCols:],rows))                        # die Spalten für die Beschreibung der Reihen herausschneiden
    rows    = list(map(lambda row:cleanRow(row,allowedStrings),rows))   # die Reihen säubern -> nur Werte oder erlaubte Strings, rest leere Strings
    rows    = list(map(lambda row:row[:findLastDataCol(rows)+1],rows))  # die Spalten hinter dem letzten Wert im Datenblock herausschneiden
    rows    = rows[descRows:]                                           # die Reihen vor der ersten Datenreihe herausschneiden
    rows    = list(filter(lambda row:len(filterLeerIn(row)) > 0,rows))  # Reihen in denen nur leere Strings vorkommen herausschneiden (hinter der letzten Datenreihe)
    return rows

#Methode,
# die in allen Strings eines Sets von Reihen unerwünschte (Teil)Strings löscht
# @param rows: Set von Reihen, die gesäubert werden sollen
# @param stringsToDelete: Liste von Strings, die gelöscht werden sollen
def deleteStringsToDelete(rows,stringsToDelete):
    return list(map(lambda row: list(map(lambda cell: helper.replaceMultiple(cell,stringsToDelete,""),row)),rows))

def getRowDescription():
    return [[""]]
def getColDescription():
    return [[""]]

# csv öffnen und ein Set von Reihen für die weitere Bearbeitung zurückgeben
def csvImport(param):
    _csv_ = param[0]
    toDelete = param[1]
    allowedStrings = param[2]
    descCols = param[3]
    descRows = param[4]
    with open(_csv_) as lines:
        rows = list(csv.reader(lines, delimiter=";"))
        rows = deleteStringsToDelete(rows,toDelete) #säubern
    return getData(allowedStrings,descCols,descRows,rows)

#Parameter für Testaufruf
pendler = "pendler.csv"
pendlerToDelete = [" "]  #komisches Zeichen in Zahlen
pendlerAllowed = ["..."]
pendlerDescCols = 2
pendlerDescRows = 6
pendlerParam = (pendler,pendlerAllowed,pendlerToDelete,pendlerDescCols,pendlerDescRows)

staatsbuergerschaft = "staatsbuergerschaft.csv"
staatsbuergerschaftToDelete = []
staatsbuergerschaftAllowed = ["X","*"]  # enthält relevante Zellen mit "X" oder "*"
staatsbuergerschaftDescCols = 2
staatsbuergerschaftDescRows = 0 #keine Angabe notwendig (keine Beschreibung, die in floats umgewandelt würden [Bsp.: Jahreszahlen])
staatsbuergerschaftParam = (staatsbuergerschaft,staatsbuergerschaftAllowed,staatsbuergerschaftToDelete,staatsbuergerschaftDescCols,staatsbuergerschaftDescRows)

geburten = "geburten_kantone.csv"
geburtenToDelete = []
geburtenAllowed = []
geburtenDescCols = 1
geburtenDescRows = 5
geburtenParam   = (geburten,geburtenAllowed,geburtenToDelete,geburtenDescCols,geburtenDescRows)



#Testaufruf
helper.cls()
data = csvImport(geburtenParam)
for row in data:
    print(row)