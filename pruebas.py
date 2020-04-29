from random import random as rd

def moneda(p):
    if rd() < p:
        return "Mandame tu video"
    else:
        return "Perdí, te mando mi foto :c"

if __name__ == '__main__':
    print("")