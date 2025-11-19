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
