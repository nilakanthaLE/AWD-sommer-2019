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


def inputTillInt(text):
    userInput = ""
    while not isinstance(userInput, int):
        try:userInput = int(input(text))
        except:userInput = ""
    return userInput

def inputTillAllowed(allowed,text):
    userInput = ""
    while userInput not in allowed:
        userInput = input(text)
    return userInput

def floatStringWithPrecision(_float,precision):
    return '%.*f' % (precision, _float) 

# string.center(15) --> 15 Zeichen langer String,bei dem der stringInhalt zentriert ist
# string.ljust(15) string.rjust(15) --> 15 Zeichen langer String,bei dem der stringInhalt rechts bzw. linksbündig ist
# string.endswith("a") // startswith("a")
# string.find("a") --> Rückgabe index
# string.lower() .upper() .islower() .isupper()
# string.split(".") - zerteilt in Teilstrings - zwischen "."

# a,b,c,d = string.split(".") --> weist a,b,c,d die Teilstrings zu
