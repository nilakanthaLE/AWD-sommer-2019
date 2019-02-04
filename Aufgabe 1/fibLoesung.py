import time
import helper

#Counter
# eine Klasse, die ein integer enthält
# dient zur Speicherung der Anzahl von Iterationen über die Fibonacci-Funktionen
class Counter:
    i = 0
    displayCounter = False
    def count(self):
        self.i += 1

        #verfälscht Zeitmessung!
        # zeigt, dass die (naive) Berechnung bei n>40  sehr lange läuft
        if displayCounter : self.printCounter()

    def printCounter(self):
        print("count: ",end="")
        print(str("{:,d}".format(self.i)) +"\r",end="")
counter = Counter()

#fibNaiv
# die naive Implementierung der Berechnung der nten Fibonacci Zahl
# @param n: welche Stelle in der Fibonacci-Reihe ist gesucht?
def fibNaiv(n):
    counter.count()
    return n if (n<2) else fibNaiv(n-1) + fibNaiv(n-2)

#fibBesser
# optimierte Berechnung der nten Fibonacci Zahl
# @param n: welche Stelle in der Fibonacci-Reihe ist gesucht?
def fibBesser(n):
    counter.count()
    if n==0: return 0
    ergebnis = (1,0)
    for _ in range(1,n):
        # Counter
        counter.count()
        ergebnis = (ergebnis[0]+ergebnis[1],ergebnis[0])
    return ergebnis[0]

#FibFuncTest
# dient zur Berechnung der gesuchten Fibonacci Zahl einer Funktion
# ermittelt Testwerte (Dauer, Anzahl Iterationen)
# erzeugt Ausdruck der Werte auf der Konsole
# @init func: die verwendete Funktion
# @init n: die gesuchte Stelle in der Fibonacci-Reihe
class FibFuncTest:
    #init Objekt mit Funktion und n
    def __init__(self,func,n):
        self.n = n
        self.func = func
    def funcName(self):
        return self.func.__name__

    #Berechnung, sowie Erfassung von Schritten und Dauer
    def calc(self,displayCounter):
        counter.i = 0
        counter.dauer = 0
        counter.displayCounter = displayCounter
        self.start          = time.time()
        self.ergebnis       = self.func(self.n)
        self.ende           = time.time()
        self.iterationen    = counter.i

    #Methoden für den Ausdruck der Ergebnis Zeilen
    def printHeadline(self): print("\nCounter für " + self.funcName() + "(%s)"%str(self.n))
    def dauer(self): return self.ende - self.start
    def printDauer(self):
        helper.einrueckung()
        print("dauer: " + str(self.dauer()) + "s")
    def printIterationen(self):
        helper.einrueckung()
        print("Anzahl Schritte: " + str(self.iterationen))
    def printErgebnis(self):
        helper.einrueckung()
        print("%s. Stelle der Fibonacci-Reihe ist: "%self.n  + str(self.ergebnis))

    #HauptFunktion 1 - gibt vollständiges Ergebnis aus
    def printTestErgebnis(self):
        self.printHeadline()
        self.printErgebnis()
        self.printIterationen()
        self.printDauer()
        print("\n")

    #HauptFunktion 2 - berechnet und gibt vollständiges Ergebnis aus
    def calcAndPrintErgebnis(self,displayCounter):
        self.calc(displayCounter)
        self.printTestErgebnis()


def printUeberschrift():
    
    print("#Programm zur Berechnung von Stellen der Fibonacci Reihe")
    print("#\tVergleicht Effizienz verschiedener Berechnungsmethoden\n")


# Methode für den Vergleich von Funktionen
# 1) zeigt Testergebnis jeder Funktion
# 2) erstellt Tabelle mit Schritten und Dauer, sortiert nach Dauer
def vergleich(funcs,n,displayCounter):
    #printUeberschrift()
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
        print(str(funcTest.dauer()))

# Methode zur Ermittlung der Rechenschritte der naiven Funktion für die Fibonacci Berechnung
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

def printCalcFibNaivCount(n):
    print("\nfibNaiv benötigt %i Schritte zur Berechnung der %i.Stelle der Fibanacci-Reihe\n\n"%(calcFibNaivCount(n),n))


#Aufruf der zu testenden Funktionen und der gesuchten Stelle der Fibonacci-Reihe
# Berechnung der Iterationen für naive Implementierung der Fibonacci-Funktion
#vergleich([fibNaiv,fibBesser],20)
#printCalcFibNaivCount(20)
stop = ""
while(stop != "stop"):
    helper.cls()
    printUeberschrift()

    fibN            = helper.inputTillInt("Welche Stelle der Fibonacci-Reihe soll berechnet werden? [Ganzzahl]: ")
    displayCounter  = helper.inputTillAllowed(["j","n"], "Soll der Counter angezeigt werden? (verfälscht die Zeiterfassung!) [j/n] :"  )
    displayCounter = True if displayCounter == "j" else False

    printCalcFibNaivCount(fibN)
    vergleich([fibNaiv,fibBesser],fibN,displayCounter)
    
    stop = input("weiter? [stop]: ")