from random import random as rd

def moneda(p):
    if rd() < p:
        return "Hola"
    else:
        return "Adiós"

if __name__ == '__main__':
    print("")
