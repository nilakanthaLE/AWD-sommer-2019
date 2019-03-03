import csv
import helper
import os
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
        string      = string.replace("(","").replace("[","").replace(")","").replace("]","")
    return (string,hasBrackets)

#Methode, die:
# Strings wenn möglich in floatValues konvertiert
# wo das nicht möglich ist, wird entweder ein leerstring zurück angegeben
# oder falls der Strings in der Liste erlaubter Strings ist, wird dieser zurückgegeben
# floatValues in Klammern werden als solche gekennzeichnet
#@param string: die zu bearbeitende Zeichenkette
#@param allowedStrings: erlaubte Zeichen in Daten - z.B. *
def convertToFloatAndFilterAllowedStrings(string,allowedStrings):
    stringBrackets  = deleteAndReplace(string,allowedStrings)
    string          = stringBrackets[0]
    hasBrackets     = stringBrackets[1]
    try:    return (float(string),"()") if hasBrackets else float(string)
    except: return string if string in allowedStrings else ""

#Methode, die:
# 1) die Daten einer übergebenen Reihe in Floats oder erlaubte strings konvertiert
def cleanRow(row,allowedStrings):
    return [convertToFloatAndFilterAllowedStrings(cell,allowedStrings) for cell in row]

#notwendige Helfermethoden für findLastDataCol(rows)
def convertToFloat(string):
    try:    return float(string)
    except: return(string)
def stringIsFloat(string):
    return isinstance(convertToFloat(string),float)
def helpFindLastDataCol(eins,zwei): #helper für Reduce (findLastDataCol)
    return zwei[0] if stringIsFloat(zwei[1]) else eins

#Methode,
# die ermittelt in welcher Spalte in allen Reihen sich der letzte (Zahlen)Wert befindet
# @param rows: das zu untersuchende Set an Rows
def findLastDataCol(rows):
    def lastDataColForRow(row): return reduce((lambda a,b:helpFindLastDataCol(a,b)),enumerate(row),0)
    lastDataCols = [lastDataColForRow(row) for row in rows]
    return reduce(lambda a,b : a if a>=b else b,lastDataCols)




CSVConfigList = []

#Methode,
# die alle leeren Strings in einer Reihe herausfiltert
# @param row: die zu filterende Reihe
def filterLeerIn(row):
    return [cell for cell in row if cell != ""]

def updateCSVConfigList(CSVConfig):
    for _CSVConfig in CSVConfigList:
        if _CSVConfig[0] == CSVConfig[0]:
            _CSVConfig = CSVConfig
            return
    CSVConfigList.append(CSVConfig)
    


def writeCSVConfigListToFile():
    with open("datenEinlesen.cfg","w") as datei:
        for line in [row[0] + "," + str(row[1]) + "," + str(row[2]) + "\n" for row in CSVConfigList]:
            datei.write(line)
        datei.close()



def readCSVConfigListFromFile():
    CSVConfigList = []
    try: datei= open("datenEinlesen.cfg","r")
    except: 
        return CSVConfigList

    try:
        for line in datei.readlines():
            csvFilename,cols,rows = line.split(",")
            CSVConfigList.append((csvFilename,int(cols),int(rows)))
    except: 
         print("Exception!!!")
    datei.close()
    return CSVConfigList
CSVConfigList = readCSVConfigListFromFile()

def getCSVConfigFor(csvFileName):
    for CSVConfig in CSVConfigList:
        if csvFileName == CSVConfig[0]:
            return CSVConfig
    return (csvFileName,0,0)


#Methode,
# die den Datenblock isoliert, ihn säubert (nur floats,erlaubteStrings,floats in Klammern, leerStrings) und zurück gibt
# @param allowedStrings: erlaubte Strings, die im Datenblock auftauchen dürfen, die keine Floats stringsToDelete
# @param descCols: Anzahl der Spalten in der css für Beschreibung (Reihenbeschriftung)
# @param descRows: Anzahl der Reihen in der css für Beschreibung (Spaltenbeschriftung)
# @param rows: das Set an Datenreihen aus der css
def getCleanDataRows(csvFilename,allowedStrings,rows):
    rows    = [cleanRow(row,allowedStrings) for row in rows]            # die Reihen säubern -> nur Werte oder erlaubte Strings, rest leere Strings
    rows    = [row[:findLastDataCol(rows)+1] for row in rows]           # die Spalten hinter dem letzten Wert im Datenblock herausschneiden
    rows    = [row for row in rows if len(filterLeerIn(row)) > 0]       # Reihen in denen nur leere Strings vorkommen herausschneiden (hinter der letzten Datenreihe) mit [ for in if ]
    
    
    ende = False
    csvConfig = getCSVConfigFor(csvFilename)
    descCols = csvConfig[1] 
    descRows = csvConfig[2]
    while not ende:
        headLine = "# Datenimport von " + csvFilename + " #"
        print("#"*len(headLine))
        print(headLine )
        print("#"*len(headLine))
        print()
        _rows    = [row[descCols:] for row in rows]                     # die Spalten für die Beschreibung der Reihen herausschneiden
        _rows    = _rows[descRows:]                                     # die Reihen vor der ersten Datenreihe herausschneiden
        for row in _rows: print(row)
        print()
        print("Es werden "+ str(descRows) + " Zeile(n) und " + str(descCols) + " Spalte(n) für die Beschreibung abgetrennt" )
        ende = helper.inputTillAllowed(["j","n"],"Ist der Datenblock OK? [j/n] ") == "j"   # Beenden mit Eingabe 'j', wenn der Datenblock korrekt isoliert wurde
        if not ende:
            descCols = helper.inputTillInt("Anzahl Spalten für Beschreibung: ")
            descRows = helper.inputTillInt("Anzahl Zeilen für Beschreibung: ")
    return (_rows,(csvFilename,descCols,descRows))

#Methode,
# die in allen Strings eines Sets von Reihen unerwünschte (Teil)Strings löscht
# @param rows: Set von Reihen, die gesäubert werden sollen
# @param stringsToDelete: Liste von Strings, die gelöscht werden sollen
def deleteStringsToDelete(rows,stringsToDelete):
    return [[helper.replaceMultiple(cell,stringsToDelete,"") for cell in row] for row in rows]



# csv öffnen und ein Set von Reihen für die weitere Bearbeitung zurückgeben
def csvImport(param):
    csvFilename = param[0]
    allowedStrings = param[1]
    toDelete = param[2]
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "/csv/" +csvFilename) as lines:
        rows = list(csv.reader(lines, delimiter=";"))
        rows = deleteStringsToDelete(rows,toDelete) #säubern
    dataRows = getCleanDataRows(csvFilename,allowedStrings,rows)
    updateCSVConfigList(dataRows[1])
    writeCSVConfigListToFile()
    return dataRows[0]

#Parameter für Testaufruf

pendler = "pendler.csv"
pendlerToDelete = [" "]  #komisches Zeichen in Zahlen
pendlerAllowed = ["..."]
pendlerParam = (pendler,pendlerAllowed,pendlerToDelete)

staatsbuergerschaft = "staatsbuergerschaft.csv"
staatsbuergerschaftToDelete = []
staatsbuergerschaftAllowed = ["X","*"]  # enthält relevante Zellen mit "X" oder "*"
staatsbuergerschaftParam = (staatsbuergerschaft,staatsbuergerschaftAllowed,staatsbuergerschaftToDelete)

geburten = "geburten_kantone.csv"
geburtenToDelete = []
geburtenAllowed = []
geburtenParam   = (geburten,geburtenAllowed,geburtenToDelete)


#Testaufruf
helper.cls()
data = csvImport(staatsbuergerschaftParam)