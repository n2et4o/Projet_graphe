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
        print("\n Circuit absorbant détecté dans le graphe.")
    else:
        print("\n Aucun circuit absorbant détecté.")

    return L, P, has_cycle

def interface_chemins(L, P):
    n = len(L)

    while True:
        rep = input("\nChemin ? (o/n) : ").strip().lower()
        if rep != "o":
            print("Arrêt.")
            break

        try:
            s = int(input(f"Sommet de départ (0..{n-1}) : "))
            t = int(input(f"Sommet d'arrivée (0..{n-1}) : "))
        except ValueError:
            print("Veuillez entrer des entiers.")
            continue

        if not (0 <= s < n and 0 <= t < n):
            print("Sommets invalides.")
            continue

        afficher_chemin(s, t, L, P)


def afficher_chemin(s, t, L, P):
    n = len(L)

    # Aucun chemin possible
    if L[s][t] == INF:
        print(f"Pas de chemin de {s} à {t}.")
        return

    # Cas trivial : même sommet
    if s == t:
        print(f"Chemin trivial : {s} (longueur = 0)")
        return

    # Reconstruction du chemin via P
    chemin = [t]
    v = t
    while v != s:
        v = P[s][v]
        if v == -1:  # sécurité si jamais P est incohérent
            print("Erreur : impossible de reconstruire le chemin.")
            return
        chemin.append(v)

    # On remet dans le bon sens
    chemin.reverse()

    # Affichage
    print(f"Chemin le plus court {s} → {t} : " + " -> ".join(map(str, chemin)))
    print(f"Longueur totale = {L[s][t]}")

# ========================= Amine's parts ===========================

def afficher_matrice(matrice, titre="Matrice d'adjacence"):
    # Gérer différents formats d'entrée
    if isinstance(matrice, dict):
        if 'matrice' in matrice:
            mat = matrice['matrice']
            n = matrice.get('n', len(mat))
        elif 'C' in matrice:
            mat = matrice['C']
            n = matrice.get('n', len(mat))
        else:
            mat = matrice
            n = len(mat)
    else:
        mat = matrice
        n = len(mat)

    # Affichage du titre
    print(f"\n{'=' * 50}")
    print(f"{titre}")
    print(f"{'=' * 50}")

    # En-tête des colonnes
    print("     ", end="")
    for j in range(n):
        print(f"  [{j}]  ", end="")
    print()
    print("     " + "-" * (n * 8))

    # Affichage de chaque ligne
    for i in range(n):
        print(f"[{i}] |", end="")
        for j in range(n):
            valeur = mat[i][j]

            # Gestion des différentes représentations de l'infini
            if valeur is None or valeur == float('inf') or (isinstance(valeur, (int, float)) and valeur >= 999999):
                print("  INF  ", end="")
            else:
                print(f"  {valeur:3}  ", end="")
        print()

    print(f"{'=' * 50}\n")
