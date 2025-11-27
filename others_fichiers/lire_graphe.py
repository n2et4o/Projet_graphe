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
    INF = 10**9
    
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
        print(f"Erreur : le fichier '{path}' contient {len(lignes_nettoyees)-2} lignes d'arcs, mais {m} étaient attendues.")
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
            print(f"Erreur : ligne d'arc {idx+1} invalide : '{ligne}'.")
            print("Format attendu : 'u v poids'")
            exit(1)
        
        # Convertir les valeurs en nombres
        try:
            u = int(elements[0])
            v = int(elements[1])
            poids = int(float(elements[2]))  # Gère les décimaux (ex: 2.5 → 2)
        except:
            print(f"Erreur : dans l'arc {idx+1}, on ne peut pas convertir '{elements[2]}' en nombre.")
            exit(1)
        
        # Vérifier que les sommets sont valides
        if u < 0 or u >= n or v < 0 or v >= n:
            print(f"Erreur : sommets hors limites (n={n}) dans l'arc '{ligne}'.")
            exit(1)
        
        # Mettre à jour la matrice
        matrice[u][v] = poids
    
    return matrice, n