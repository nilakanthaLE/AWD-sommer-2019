import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#helper
def einrueckung():
    print("  ", end="")
def printTabs(anzahl):
    _str = "\r"
    for _ in range(0,anzahl):
        _str += "\t"
    print(_str,end="")

#Counter
# eine Klasse, die ein integer enthält
# dient zur Speicherung der Anzahl von Iterationen über die Fibonacci-Funktionen
class Counter:
    i = 0
    def count(self):
        self.i += 1
        #für Zeitmessung auskommentieren
        # zeigt, dass die (naive) Berechnung bei n>40  sehr lange läuft
        self.printCounter()

    def printCounter(self):
        print("count: ",end="")
        print(str(self.i) +"\r",end="")

counter = Counter()

#fibNaiv
# die naive Implementierung der Berechnung der nten Fibonacci Zahl
# @param n: welche Stelle in der Fibonacci-Reihe ist gesucht?
def fibNaiv(n):
    # Counter
    counter.count()

    if n==0: return 0
    if n==1: return 1
    return fibNaiv(n-1) + fibNaiv(n-2)

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


class FibFuncTest:
    #init Objekt mit Funktion und n
    def __init__(self,func,n):
        self.n = n
        self.func = func
    def funcName(self):
        return self.func.__name__

    #Berechnung, sowie Erfassung von Schritten und Dauer
    def calc(self):
        counter.i = 0
        counter.dauer = 0
        self.start          = time.time()
        self.ergebnis       = self.func(self.n)
        self.ende           = time.time()
        self.iterationen    = counter.i
        #self.dauer          = counter.dauer

    #Ausdruck der Ergebnis Zeilen
    def printHeadline(self):
        print("\nCounter für " + self.funcName() + "(%s)"%str(self.n))
    def dauer(self):
        return self.ende - self.start
    def printDauer(self):
        einrueckung()
        print("dauer: " + str(self.dauer()) + "s")
    def printIterationen(self):
        einrueckung()
        print("Anzahl Schritte: " + str(self.iterationen))
    def printErgebnis(self):
        einrueckung()
        print("%s. Stelle der Fibonacci-Reihe ist: "%self.n  + str(self.ergebnis))

    #HauptFunktion 1 - gibt vollständiges Ergebnis aus
    def printTestErgebnis(self):
        self.printHeadline()
        self.printErgebnis()
        self.printIterationen()
        self.printDauer()
        print("\n")

    #HauptFunktion 2 - berechnet und gibt vollständiges Ergebnis aus
    def calcAndPrintErgebnis(self):
        self.calc()
        self.printTestErgebnis()




def vergleich(funcs,n):
    cls()
    funcTests = []
    for func in funcs:
        funcTest = FibFuncTest(func,n)
        funcTests.append(funcTest)
        funcTest.calcAndPrintErgebnis()

    print("Unterschiede zwischen den Funktionen\n")
    print("Funktion",end="")
    printTabs(2)
    print("Schritte",end="")
    printTabs(4)
    print("Dauer")
    for funcTest in funcTests:
        print(funcTest.funcName(),end="")
        printTabs(2)
        print(str(funcTest.iterationen),end="")
        printTabs(4)
        print(str(funcTest.dauer()))

vergleich([fibNaiv,fibBesser],7)

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
    schritte = str(calcFibNaivCount(n))
    print("\nfibNaiv benötigt %s Schritte zur Berechnung der %s.Stelle der Fibanacci-Reihe\n\n"%(schritte,n))

printCalcFibNaivCount(5)
