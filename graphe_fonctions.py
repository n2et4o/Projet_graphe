import sys, os #pour intérargir avec syst d'exploitation - manipuler les répertoires et fichiers

INF = 10**9


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # dossier temporaire PyInstaller
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def lire_graphe(relative_path):
    """
    Lecture d'un fichier de graphe compatible EXE + mode normal.
    Gère automatiquement les chemins via resource_path().
    """

    # === FONCTION INTERNE POUR GÉRER LES CHEMINS (fusionnée) ===
    try:
        base_path = sys._MEIPASS   # dossier temporaire PyInstaller
    except:
        base_path = os.path.abspath(".")
    path = os.path.join(base_path, relative_path)

    INF = 10 ** 9

    # Fonction interne pour nettoyer chaque ligne
    def nettoyer(ligne):
        ligne_sans_commentaire = ligne.split('#', 1)[0]
        return ligne_sans_commentaire.strip()

    # Lecture du fichier
    lignes_nettoyees = []
    with open(path, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            ligne_propre = nettoyer(ligne)
            if ligne_propre != "":
                lignes_nettoyees.append(ligne_propre)

    # Vérification n et m
    if len(lignes_nettoyees) < 2:
        print(f"Erreur : le fichier '{relative_path}' doit avoir au moins 2 lignes.")
        exit(1)

    # Lecture n
    try:
        n = int(lignes_nettoyees[0])
    except:
        print(f"Erreur : n n'est pas un entier dans '{relative_path}'.")
        exit(1)

    if n <= 0:
        print("Erreur : le nombre de sommets doit être > 0.")
        exit(1)

    # Lecture m
    try:
        m = int(lignes_nettoyees[1])
    except:
        print(f"Erreur : m n'est pas un entier dans '{relative_path}'.")
        exit(1)

    if m < 0:
        print("Erreur : m ne peut pas être négatif.")
        exit(1)

    print(f"Nombre de sommets : {n}")
    print(f"Nombre d'arcs : {m}")
    print("Liste des arcs :")

    # Vérification du nombre d'arcs
    if len(lignes_nettoyees) < 2 + m:
        print(f"Erreur : fichier incomplet ({len(lignes_nettoyees)-2}/{m} arcs).")
        exit(1)

    # Création de la matrice
    matrice = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    arcs = []

    # Lecture des arcs
    for idx in range(m):
        ligne = lignes_nettoyees[2 + idx]
        elements = ligne.split()

        if len(elements) < 3:
            print(f"Erreur : ligne d'arc invalide : '{ligne}'")
            exit(1)

        try:
            u = int(elements[0])
            v = int(elements[1])
            poids = int(float(elements[2]))
        except:
            print(f"Erreur conversion '{ligne}' → entier impossible.")
            exit(1)

        if u < 0 or u >= n or v < 0 or v >= n:
            print(f"Erreur : sommets hors limites dans '{ligne}'.")
            exit(1)

        print(f"{u} -> {v} : {poids}")
        arcs.append((u, v, poids))
        matrice[u][v] = poids

    return matrice, n, m, arcs

#===================================


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

def afficher_matrice(matrice, titre="Matrice de valeurs"):
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


