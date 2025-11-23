INF = 10**9


def lire_graphe(path):
    """
    Lit un fichier de graphe au format strict :
      Ligne 1 : n (nombre de sommets, étiquetés de 0 à n-1)
      Ligne 2 : m (nombre d'arcs)
      Lignes suivantes : u v poids (sommets source, destination et poids de l'arc)
    Les lignes vides et les commentaires (après '#') sont ignorés.
    Retour : (matrice, n) où matrice est une matrice n x n (entiers),
             la diagonale vaut 0 et les arcs absents sont marqués par INF.
    En cas d'erreur, le programme s'arrête avec un message d'erreur clair.
    """
    INF = 10 ** 9

    # Fonction pour nettoyer une ligne (enlever les commentaires et espaces)
    def nettoyer(ligne):
        # On supprime tout après '#' et on retire les espaces inutiles
        ligne_sans_commentaire = ligne.split('#', 1)[0]
        return ligne_sans_commentaire.strip()

    # Lecture du fichier ligne par ligne
    lignes_nettoyees = []
    with open(path, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            ligne_propre = nettoyer(ligne)
            if ligne_propre != "":  # On garde seulement les lignes non vides
                lignes_nettoyees.append(ligne_propre)

    # Vérification des lignes minimales (n et m)
    if len(lignes_nettoyees) < 2:
        print(f"Erreur : le fichier '{path}' doit avoir au moins 2 lignes (pour n et m).")
        exit(1)

    # Lire le nombre de sommets (n)
    try:
        n = int(lignes_nettoyees[0])
    except:
        print(f"Erreur : la première ligne '{lignes_nettoyees[0]}' n'est pas un nombre entier.")
        exit(1)

    if n <= 0:
        print("Erreur : le nombre de sommets 'n' doit être supérieur à 0.")
        exit(1)

    # Lire le nombre d'arcs (m)
    try:
        m = int(lignes_nettoyees[1])
    except:
        print(f"Erreur : la deuxième ligne '{lignes_nettoyees[1]}' n'est pas un nombre entier.")
        exit(1)

    if m < 0:
        print("Erreur : le nombre d'arcs 'm' ne peut pas être négatif.")
        exit(1)

    # Vérifier qu'il y a suffisamment de lignes pour les arcs
    if len(lignes_nettoyees) < 2 + m:
        print(
            f"Erreur : le fichier '{path}' contient {len(lignes_nettoyees) - 2} lignes d'arcs, mais {m} étaient attendues.")
        exit(1)

    # Initialiser la matrice (tous les arcs = INF, diagonale = 0)
    matrice = []
    for i in range(n):
        ligne_matrice = []
        for j in range(n):
            if i == j:
                ligne_matrice.append(0)  # Diagonale = 0
            else:
                ligne_matrice.append(INF)  # Arc absent = INF
        matrice.append(ligne_matrice)

    # Lire chaque arc
    for idx in range(m):
        ligne = lignes_nettoyees[2 + idx]
        elements = ligne.split()  # Découper la ligne en mots

        # Vérifier qu'il y a 3 éléments (u, v, poids)
        if len(elements) < 3:
            print(f"Erreur : ligne d'arc {idx + 1} invalide : '{ligne}'.")
            print("Format attendu : 'u v poids'")
            exit(1)

        # Convertir les valeurs en nombres
        try:
            u = int(elements[0])
            v = int(elements[1])
            poids = int(float(elements[2]))  # Gère les décimaux (ex: 2.5 → 2)
        except:
            print(f"Erreur : dans l'arc {idx + 1}, on ne peut pas convertir '{elements[2]}' en nombre.")
            exit(1)

        # Vérifier que les sommets sont valides
        if u < 0 or u >= n or v < 0 or v >= n:
            print(f"Erreur : sommets hors limites (n={n}) dans l'arc '{ligne}'.")
            exit(1)

        # Mettre à jour la matrice
        matrice[u][v] = poids

    return matrice, n


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
