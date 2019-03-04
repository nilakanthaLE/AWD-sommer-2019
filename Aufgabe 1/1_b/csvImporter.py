import csv
import helper
import os
from functools import reduce

#################################
## 1.b CSV-Importer 04.03.2019 ##
## Matthias Pochmann           ##
## für: AWD 2019               ##
## Dozent: Jörg Osterrieder    ##
#################################

#dritter Ansatz
# Datenblock wird durch explizite Angabe der Anzahl von cols und rows für die Beschreibung eingegrenzt

#Der dritte Ansatz hat sich als der effizienteste herausgestellt
# Leider sind die Daten der verschiedenen Tabellen so unterschiedlich, dass eine rein automatisierte Transformation kaum möglich erschien
# deshalb habe ich mich entschlossen, mindestens die Anzahl der Reihen und Spalten vor dem Datenblock "manuell" zu erfassen


###############################################
## Methoden zur Speicherung von Usereingaben ##
###############################################

CSVConfigList = []
# Methode,
# die die CSVConfigList aktualisiert
# (neuer Eintrag oder modifiziert bestehenden Eintrag)
# @param CSVConfig: Usereingaben bzgl. einer CSV-Datei 
def updateCSVConfigList(CSVConfig):
    for _CSVConfig in CSVConfigList:
        if _CSVConfig[0] == CSVConfig[0]:
            _CSVConfig = CSVConfig
            return
    CSVConfigList.append(CSVConfig)

# Methode,
# die die CSVConfigList in eine configdatei schreibt
def writeCSVConfigListToFile():
    with open("datenEinlesen.cfg","w") as datei:
        for line in [row[0] + "," + str(row[1]) + "," + str(row[2]) + "\n" for row in CSVConfigList]:
            datei.write(line)
        datei.close()

# Methode,
# die die CSVConfigList aus der configdatei liest
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

# Methode,
# die in der CSVConfigList einen Eintrag zu einem CSV-Filenamen herausfinden
# erzeugt einen neuen Eintrag, falls kein Eintrag vorhanden ist
# @param csvFileName: der Name der CSV
def getCSVConfigFor(csvFileName):
    for CSVConfig in CSVConfigList:
        if csvFileName == CSVConfig[0]:
            return CSVConfig
    return (csvFileName,0,0)

###################################################
## Hilfesmethoden für die Aufbereitung der Daten ##
###################################################

#Methode,
# die Kommas in Strings durch Punkt ersetzt ("deutsche" Zahlen mit Komma)
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
# Strings wenn möglich in floatValues konvertiert.
# Wenn das nicht möglich ist, wird entweder ein leerstring zurück gegeben
# oder falls der String in der Liste erlaubter Strings enthalten ist, wird dieser zurückgegeben.
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
# die Daten einer übergebenen Reihe in Floats oder erlaubte strings konvertiert
def convertRow(row,allowedStrings):
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

#Methode,
# die alle leeren Strings in einer Reihe herausfiltert
# @param row: die zu filterende Reihe
def filterLeerIn(row):
    return [cell for cell in row if cell != ""]


#####################################
## zentrale Methoden der Anwendung ##
#####################################

#Methode,
# die den Datenblock isoliert, ihn säubert (nur floats,erlaubteStrings,floats in Klammern, leerStrings) und zurück gibt
# steuert die Interaktion mit dem User, der die Anzahl von Beschreibungspalten und -reihen angeben soll.
# @param csvFileName: der Name der CSV
# @param allowedStrings: erlaubte Strings, die im Datenblock auftauchen dürfen, die keine Floats stringsToDelete
# @param rows: das Set an Datenreihen aus der css
def getCleanDataRows(csvFilename,allowedStrings,rows):
    rows    = [convertRow(row,allowedStrings) for row in rows]          # die Reihen säubern -> nur Werte oder erlaubte Strings, rest leere Strings
    rows    = [row[:findLastDataCol(rows)+1] for row in rows]           # die Spalten hinter dem letzten Wert im Datenblock herausschneiden
    rows    = [row for row in rows if len(filterLeerIn(row)) > 0]       # Reihen in denen nur leere Strings vorkommen herausschneiden (hinter der letzten Datenreihe) mit [ for in if ]
    
    
    ende = False
    csvConfig = getCSVConfigFor(csvFilename)
    descCols = csvConfig[1]                                             # anzahl der Beschreibungsspalten
    descRows = csvConfig[2]                                             # anzahl der Beschreibungszeilen

    while not ende:                                                     # der User wird solange in deinem Dialog gehalten, bis er angibt, dass die Daten korrekt isoliert wurden.
        helper.cls()
        #Überschrift
        headLine = "# Datenimport von " + csvFilename + " #"
        print("#"*len(headLine))
        print(headLine )
        print("#"*len(headLine))
        print()

        # Datenblock mit Userangaben "zurechtschneiden" und ausgeben
        _rows    = [row[descCols:] for row in rows]                     # die Spalten für die Beschreibung der Reihen herausschneiden
        _rows    = _rows[descRows:]                                     # die Reihen vor der ersten Datenreihe herausschneiden
        for row in _rows: print(row)
        
        # Dialog mit dem User
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

#Methode,
# die eine csv öffnet und ein Ergebnisset von Reihen für die weitere Bearbeitung zurückgibt.
# Ist Anfang und Ende der Anwendung
# @param param: ein Tupel von Parametern für die BEarbeitung der CSV
def csvImport(param):
    csvFilename     = param[0]
    allowedStrings  = param[1]
    toDelete        = param[2]
    with open(os.path.dirname(os.path.abspath(__file__)) + "/csv/" +csvFilename) as lines:
        rows = list(csv.reader(lines, delimiter=";"))
        rows = deleteStringsToDelete(rows,toDelete) #säubern
    data = getCleanDataRows(csvFilename,allowedStrings,rows)
    updateCSVConfigList(data[1])
    writeCSVConfigListToFile()
    return data[0]

##############################
## Parameter für Testaufruf ##
##############################

# der Name der csv-Datei
# toDelete: störende Zeichen, die eine Konvertierung von string in float behindern
# allowed: Zeichen im Datenblock, die erhalten bleiben sollten
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

#Testaufruf (ein Parametertupel übergeben)
data = csvImport(staatsbuergerschaftParam)