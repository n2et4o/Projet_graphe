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


def afficher_chemin(s, t, L, P):
n = len(L)

if L[s][t] == INF:
    print(f"Pas de chemin de {s} à {t}.")
    return

if s == t:
    print(f"Chemin trivial : {s} (longueur = 0)")
    return

chemin = [t]
v = t
while v != s:
    v = P[s][v]
    if v == -1:  # sécurité si jamais P est incohérent
        print("Erreur : impossible de reconstruire le chemin.")
        return
    chemin.append(v)

chemin.reverse()
print(f"Chemin le plus court {s} → {t} : " + " -> ".join(map(str, chemin)))
print(f"Longueur totale = {L[s][t]}")

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