INF = 10**9

def floyd(C):
    n = len(C)

    # Copie initiale de C dans L
    L = [[C[i][j] for j in range(n)] for i in range(n)]

    # Matrice des prédécesseurs P
    P = [[-1 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and C[i][j] != INF:
                P[i][j] = i

    # État initial
    afficher_matrice(L, "L (initial)")
    afficher_matrice(P, "P (initial)")

    has_cycle = False

    # Triple boucle de Floyd
    for k in range(n):
        for i in range(n):
            if L[i][k] == INF:
                continue
            for j in range(n):
                if L[k][j] == INF:
                    continue

                cand = L[i][k] + L[k][j]
                if cand < L[i][j]:
                    L[i][j] = cand
                    P[i][j] = P[k][j]

        # Affichage intermédiaire après ce k
        afficher_matrice(L, f"L après k = {k}")
        afficher_matrice(P, f"P après k = {k}")

        # On regarde si un circuit absorbant apparaît
        for i in range(n):
            if L[i][i] < 0:
                has_cycle = True

    if has_cycle:
        print("\n⚠️  Circuit absorbant détecté dans le graphe.")
    else:
        print("\n✅ Aucun circuit absorbant détecté.")

    return L, P, has_cycle
