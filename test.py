def rechercher(x, L):
    if len(L) == 1:
        return L[0] == x
    else:
        if L[0] == x:
            return True
        else:
            return rechercher(x, L[1:])


print(rechercher(4, [1, 4]))
