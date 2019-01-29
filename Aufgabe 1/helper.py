#helper
import os

def einrueckung():
    print("  ", end="")
def printTabs(anzahl):
    _str = "\r"
    for _ in range(0,anzahl):
        _str += "\t"
    print(_str,end="")
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
