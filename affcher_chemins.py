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
