import math


def premier(n: int):
    diviseurs = []
    for k in range(2, int(math.sqrt(n) + 1)):
        if n % k == 0:
            diviseurs.append(k)
    return len(diviseurs) == 0


def plus_grand_nombre_premier(n: int):
    plus_petit = 0
    for i in range(1, n + 1):
        if premier(i):
            plus_petit = i
    return plus_petit



