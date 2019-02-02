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

def replaceMultiple(string,toReplace,_with):
    for rep in toReplace : string = string.replace(rep,_with)
    return string
