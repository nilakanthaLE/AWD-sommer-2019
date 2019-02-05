from time import time
import helper

##################################
# Primäre Methoden (Berechnungen)
##################################

#fibNaiv
# naive Implementierung der Berechnung der nten Fibonacci Zahl
# @param n: die gesuchte Stelle in der Fibonacci-Folge
def fibNaiv(n):
    counter.count()
    return n if (n<2) else fibNaiv(n-1) + fibNaiv(n-2)

#fibBesser
# optimierte Methode für die Berechnung der nten Fibonacci Zahl
# @param n: die gesuchte Stelle in der Fibonacci-Folge
def fibBesser(n):
    counter.count()
    if n==0: return 0
    ergebnis = (1,0)
    for _ in range(1,n):
        # Counter
        counter.count()
        ergebnis = (ergebnis[0]+ergebnis[1],ergebnis[0])
    return ergebnis[0]

#fibDirekt
# direkte Berechnung des n. Gliedes per expliz. Bildungsgesetz (Formel von Moivre-Binet)
# https://de.wikipedia.org/wiki/Fibonacci-Folge#Formel_von_Moivre-Binet
def fibDirekt(n):
    counter.count()
    wurzel5 = 5.0**(1/2)
    return int(1.0/wurzel5 * ( ((1.0+wurzel5)/2.0)**n - ((1.0-wurzel5)/2.0)**n)) # int() wegen Rundunsfehler

#Methode zur Ermittlung der Rechenschritte der naiven Funktion für die Fibonacci Berechnung
# Die Vorschrift für die Berechnung lautet:
# f(0) = 1
# f(1) = 1
# f(n) = f(n-1) + f(n-2) + 1 ( ab n>= 2 )
def calcFibNaivCount(n):
    if n==0 or n==1: return 1
    ergebnis = (1,1)
    for _ in range(2,n+1):
        ergebnis = (ergebnis[0]+ergebnis[1] + 1,ergebnis[0])
    return ergebnis[0]

###########
# Counter 
###########

#class Counter
# eine Klasse, die ein integer enthält
#   dient zur Speicherung der Anzahl von Iterationen über die Fibonacci-Funktionen
#   displayCounter bestimmt, ob bei der Berechnung ein Counter angezeigt werden soll 
#       die Anzeige des Counters verfälscht die Zeitmessung!
#       zeigt aber, dass die (naive) Berechnung bei n>40 (einfach nur) sehr lange läuft
class Counter:
    i = 0
    displayCounter = False
    def count(self):
        self.i += 1
        #die Anzeige des Counters verfälscht Zeitmessung!
        # zeigt aber, dass die (naive) Berechnung bei n>40 (einfach nur) sehr lange läuft
        if self.displayCounter : self.printCounter()
    def printCounter(self):
        print("count: ",end="")
        print("{:,d}".format(self.i) + "\r",end="")

####################################################
# Vergleich der Effizienz der Berechnungsfunktionen
####################################################

# class FibFuncTest
#Klasse für den Test der Effizienz der Berechnung der gesuchten Fibonacci Zahl einer Funktion
#   ermittelt Testwerte (Dauer, Anzahl Iterationen)
#   erzeugt Ausdruck der Werte auf der Konsole
#   @init func: die verwendete Funktion
#   @init n: die gesuchte Stelle in der Fibonacci-Folge
class FibFuncTest:
    def __init__(self,func,n):
        self.n = n          # Stelle in der Fibonacci-Folge
        self.func = func    # zu testende Funktion (fibNaiv,fibBesser,...)

    #den Namen der Funktion ermitteln   
    def funcName(self):
        return self.func.__name__

    #Berechnung, sowie Erfassung von Schritten und Dauer
    def calc(self,displayCounter):
        counter.i = 0
        counter.dauer = 0
        counter.displayCounter = displayCounter
        self.start          = time()
        self.ergebnis       = self.func(self.n)
        self.ende           = time()
        self.iterationen    = counter.i

    #Methoden für den Ausdruck der Ergebnis Zeilen
    def printHeadline(self): print("Ergebnisse für " + self.funcName() + "(%s)"%str(self.n))
    def dauer(self): return self.ende - self.start
    def printDauer(self):
        helper.einrueckung()
        print("dauer: " + helper.floatStringWithPrecision(self.dauer() *1000,5) + " ms")
    def printIterationen(self):
        helper.einrueckung()
        print("Anzahl Schritte: " + str(self.iterationen))
    def printErgebnis(self):
        helper.einrueckung()
        print("%s. Stelle der Fibonacci-Folge ist: "%self.n  + str(self.ergebnis))

    #HauptFunktion 1 - gibt vollständiges Ergebnis aus
    def printTestErgebnis(self):
        self.printHeadline()
        self.printErgebnis()
        self.printIterationen()
        self.printDauer()
        print()

    #HauptFunktion 2 - berechnet und gibt vollständiges Ergebnis aus
    def calcAndPrintErgebnis(self,displayCounter):
        self.calc(displayCounter)
        self.printTestErgebnis()

# Methode für den Vergleich von Funktionen
# 1) zeigt Testergebnis jeder Funktion
# 2) erstellt Tabelle mit Schritten und Dauer, sortiert nach Dauer
# @param funcs: Liste zu testender Funktionen
# @param n: die gesuchte Stelle in der Fibonacci-Folge
def vergleich(funcs,n,displayCounter):
    funcTests = []
    for func in funcs:
        funcTest = FibFuncTest(func,n)
        funcTests.append(funcTest)
        funcTest.calcAndPrintErgebnis(displayCounter)

    print("Unterschiede zwischen den Funktionen\n")
    print("Funktion",end="")
    helper.printTabs(2)
    print("Schritte",end="")
    helper.printTabs(4)
    print("Dauer")
    funcTests.sort(key=lambda _:_.dauer())
    for funcTest in funcTests:
        print(funcTest.funcName(),end="")
        helper.printTabs(2)
        print(str(funcTest.iterationen),end="")
        helper.printTabs(4)
        print(helper.floatStringWithPrecision(funcTest.dauer() *1000,5) + " ms")


################
# Hauptprogramm
################

# helper für main()
def printCalcFibNaivCount(n):
    print("\nfibNaiv benötigt "+ "{:,d}".format(calcFibNaivCount(n)) + " Schritte zur Berechnung der %i.Stelle der Fibanacci-Folge\n"%n)
def printUeberschrift():
    print("#Programm zur Berechnung von Stellen der Fibonacci Folge")
    print("#\tVergleicht Effizienz verschiedener Berechnungsmethoden\n")

## Programmaufruf mit Userinteraktion
# 1) Fragt User, welche Stelle der Fibanacci-Folge berechnet werden soll.
# 2) Fragt, ob der Counter angezeigt werden soll.
# 3) Informiert den User, wie viele Schritte die naive Implementierung der Fiboncci-Berechnung benötigen wird.
# 4) Testet die (beiden) Berechnungsfunktionen. 
# 5) Stellt die Ergebnisse in einer Tabelle dar.
counter = Counter()
def main():
    stop = ""
    while(stop != "stop"):
        helper.cls()
        printUeberschrift()
        fibN            = helper.inputTillInt("Welche Stelle der Fibonacci-Folge soll berechnet werden? [Ganzzahl]: ")
        displayCounter  = helper.inputTillAllowed(["j","n"], "Soll der Counter angezeigt werden? (verfälscht die Zeiterfassung!) [j/n] :"  )
        displayCounter = True if displayCounter == "j" else False
        printCalcFibNaivCount(fibN)
        vergleich([fibNaiv,fibBesser,fibDirekt],fibN,displayCounter)
        stop = input("\nweiter? [stop]: ")
main()