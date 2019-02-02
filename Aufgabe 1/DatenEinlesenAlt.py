# alternative Lösungsansätze für Aufgabe Dateneinlesen


#erster Ansatz
data = []
def convertToFloat(string):
    try:return float(string)
    except: return(string)

def clean(rows):
    return list(filter(lambda _: not(_[-2:][0] == "" and _[-1:][0] == ""),rows))

def convertRowToFloats(row):
    if row[0] == "": return row
    row = list(map(lambda _:_.replace(",","."),row))
    row = list(map(lambda _: convertToFloat(_),row))
    return row

class CsvData:
    def __init__(self,colDes,rowDes,data):
        self.data   = data
        self.colDes = colDes
        self.rowDes = rowDes

    def printCellData(self,row,col):
        print(self.rowDes[row] + " " + self.colDes[col] + ": " + str(self.data[row][col])+"\n")

with open('geburten_kantone.csv') as lines:
    rows = csv.reader(lines, delimiter=";")
    rows = clean(rows)
    rows = list(map(lambda row: convertRowToFloats(row),rows))

    colDescription = rows.pop(0)
    colDescription.pop(0)

    rowDescription = []
    for row in rows:
        rowDescription.append(row.pop(0))



#print(colDescription)
#print(rowDescription)
#print(rows)

#helper.cls()
csvData = CsvData(colDescription,rowDescription,rows)
csvData.printCellData(1,8)








## zweiter Ansatz

def deleteAndReplace(string,allowedStrings):
    string      = string.replace(",",".")
    hasBrackets = False
    if ("(" in string) or ("[" in string):
        hasBrackets = True
        string = string.replace("(","").replace("[","").replace(")","").replace("]","")
    return (string,hasBrackets)

#Methode, die:
# 1) Kommas in Werten durch punkt ersetzt
# 2) Werte in Float umwandelt
# 3) floats zurückgibt
# 4) anderes als float gegen Liste an erlaubten Strings abgleicht
# 5) erlaubte Strings zurückgibt
# 6) Werte mit Klammern in Werte umwandelt und markiert
# 7) alle übrigen Werte durch leerStrings ersetzt
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


def filterLeerIn(row):
    return list(filter(lambda cell: cell != "",row))

#Methode, die:
# 1) die Daten einer übergebenen row in Floats oder erlaubte strings konvertiert
# 2) alle (übrigen) leeren Strings aus der row herausfiltert
def cleanRow(row,allowedStrings):
    row = list(map(lambda cell:convertToFloatAndFilterAllowedStrings(cell,allowedStrings),row))
    return filterLeerIn(row)

#Methode, die:
# 1) den Datenblock aus dem Array von rows herausfiltert
# 2) die Daten des Datenblocks in Floats oder erlaubte strings konvertiert
#@param rows: ungefiltere Zeilen des css-Files mit Rohdaten
#@param allowedStrings: erlaubte Zeichen in Daten - z.B. *
def getData(allowedStrings,rows):
    rows  = list(map(lambda row:cleanRow(row,allowedStrings),rows))
    return list(filter(lambda row:len(row) > 0 ,rows))

def cleanOnlyDescription(row,allowedStrings):
    return list(map(lambda cell:"" if convertToFloatAndFilterAllowedStrings(cell,allowedStrings) != "" else cell,row))

def getRowDescription(allowedStrings,rows):
    dataRows = list(map(lambda row:cleanRow(row,allowedStrings),rows))

    dataRows    = enumerate(dataRows)
    filtered    = list(filter(lambda row:len(row[1]) > 0,dataRows))
    filtered    = list(map(lambda row:row[0],filtered))
    descriptions    = list(filter(lambda row:row[0] in filtered,enumerate(rows)))
    descriptions    = list(map(lambda row:row[1],descriptions))
    descriptions    = list(map(lambda row:cleanOnlyDescription(row,allowedStrings),descriptions))

    last = "" #letzte 1.Spalte
    for row in descriptions:
        if row[0] == "": row[0] = last
        else: last = row[0]

    return list(map(lambda row:filterLeerIn(row),descriptions))









with open(_csv_) as lines:
    rows = list(csv.reader(lines, delimiter=";"))
    rows = deleteStringsToDelete(rows,toDelete) #säubern


    rowDescriptions = getRowDescription(allowedStrings,rows)
    data            = getData(allowedStrings,rows)



#print("rowDescriptions")
#for row in rowDescriptions:
#    print(row)

#print("\ndata")
#for row in data:
#    print(row)
