import pygame
import time
import random
import io, contextlib
import re, pygame  # Importation du module pour manipuler les expressions régulières
from graphe_fonctions import *


# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projet Graphe - Algorithme de Floyd Warshall")


backgrounds = [
    pygame.image.load(resource_path("background/background1.png"))
]
backgrounds = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in backgrounds]

# Variables de gestion du fond
background_index = 0
change_time = pygame.time.get_ticks()

# Couleurs
WHITE = (255, 255, 255)
text_color = (0, 0, 0)
BLUE = (100, 100, 255)

# Police
font = pygame.font.Font(None, 50)
input_font = pygame.font.Font(None, 40)

# Modes de couleurs
MODES = {
    "Clair": {"background": (255, 255, 255), "text": (0, 0, 0)},
    "Sombre": {"background": (30, 30, 30), "text": (255, 255, 255)},
    "Bleu Nuit": {"background": (10, 10, 50), "text": (200, 200, 255)}
}


class State:
    def __init__(self):

        # Options du menu
        self.options = ["Choisir un graphe", "Options", "Aide", "Quitter"]
        self.selected = 0
        self.choosing_graphe = False
        self.chosen_graphe = None
        self.choosing_options = False
        self.input_text = ""
        self.showing_help = False
        self.clock = pygame.time.Clock()
        self.mode_options = list(MODES.keys())
        self.selected_mode = 0

        # Mode actuel
        self.default_mode = "Bleu Nuit"
        self.current_mode = self.default_mode
        self.current_background_color = MODES[self.current_mode]["background"]
        self.text_color = MODES[self.current_mode]["text"]
        self.running = True



def draw_menu(screen,state):
    #Affiche le menu avec le fond dynamique.
    global background_index, change_time

    # Vérifier si 5 secondes sont écoulées
    if pygame.time.get_ticks() - change_time >= 3000:
        background_index = (background_index + 1) % len(backgrounds)
        change_time = pygame.time.get_ticks()  # Mettre à jour le temps

    # Afficher l'image de fond
    screen.blit(backgrounds[background_index], (0, 0))

    # Afficher le titre
    title = font.render("Bienvenue!", True, state.text_color)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # Afficher les options du menu
    for i, option in enumerate(state.options):
        color = BLUE if i == state.selected else state.text_color
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

    pygame.display.flip()

def draw_help(screen, state):
    screen.fill(state.current_background_color)

    help_text = (
        "Ce code permet de manipuler des graphes en calculant les plus courts chemins entre toutes les paires de sommets. "
        "Il analyse la structure du graphe, détecte la présence de cycles de poids négatif "
        "et réalise différentes opérations telles que la construction de matrices de distance, "
        "l’optimisation des trajets ou la vérification de l’accessibilité entre nœuds."
    )

    # Utilisation de render_text_multiline pour gérer l'affichage proprement
    text = render_text_multiline(help_text, font, state.text_color, WIDTH - 40)

    y_offset = HEIGHT // 4  # Position de départ
    for line in text:
        rendered_text = font.render(line, True, state.text_color)
        screen.blit(rendered_text, (20, y_offset))  # Légère marge pour éviter d'être collé au bord
        y_offset += 35  # Espacement entre les lignes

    # Ajout du texte de retour en bas de l'écran
    back_text = font.render("Appuyez sur Supprimer (la croix) pour revenir", True, (0, 0, 255))
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

def render_text_multiline(text, font, color, max_width):
    #Découpe un texte trop long en plusieurs lignes.

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_surface = font.render(test_line, True, color)

        if test_surface.get_width() > max_width:
            lines.append(current_line)  # Ajoute la ligne précédente
            current_line = word + " "  # Commence une nouvelle ligne
        else:
            current_line = test_line  # Continue la ligne actuelle

    lines.append(current_line)  # Ajoute la dernière ligne
    return lines

def draw_input_box(screen, state):
    # Liste dynamique des fichiers .txt dans le dossier graphes_Projet
    dossier = resource_path("graphes_tests")
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".txt")]
    fichiers.sort()  # Optionnel : trie les fichiers
    total = len(fichiers)

    # Affichage de l'instruction dynamique
    screen.fill(state.current_background_color)
    if total > 0:
        text = f"Entrez un numéro entre 0 et {total-1}:"
    elif total > 13:
        text = f"Le(s) fichier(s) que vous avez creer commence à partir de 0.\n Entrez un numéro entre 1 et {total}:"
    else:
        text = "Aucun fichier .txt trouvé dans graphes_Projet"

    A_text = font.render(text, True, state.text_color)
    screen.blit(A_text, (WIDTH // 2 - A_text.get_width() // 2, HEIGHT // 3))

    input_surface = input_font.render(state.input_text, True, BLUE)
    screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

def draw_graphe_menu(screen,state):
    screen.fill(state.current_background_color)
    title = font.render(f"Graphe {state.chosen_graphe}", True, state.text_color)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    sub_options = ["Afficher le graphe", "floydifier le graphe", "Aide",
                   "Retour au menu principal", "Quitter"]

    for i, option in enumerate(sub_options):
        color = BLUE if i == state.selected else state.text_color
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

    pygame.display.flip()

def print_f(func, *args, **kwargs):
    #Capture tout ce que la fonction affiche via print() et le retourne.
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        func(*args, **kwargs)
    return output.getvalue().strip()

def draw_options_menu(screen,state):
    screen.fill(state.current_background_color)
    title = font.render("Choisir un Mode:", True, state.text_color)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    for i, mode in enumerate(state.mode_options):
        color = (100, 100, 255) if i == state.selected_mode else state.text_color
        text = font.render(mode, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

    pygame.display.flip()

def afficher_graphe_pygame(screen, n, m, arcs, matrice, nb):
    """
    Affiche les informations du graphe (n, m, arcs + matrice)
    avec défilement vertical/horizontal.
    Quitter : ENTER ou ESC
    """

    font = pygame.font.SysFont("consolas", 22)

    # Offsets pour le défilement
    x_offset = 0
    y_offset = 0

    base_x = 20
    base_y = 20

    clock = pygame.time.Clock()
    running = True

    # ============================================================
    # Convertir la matrice en lignes de texte (IMPORTANT)
    # ============================================================
    texte_matrice = afficher_matrice_text(matrice, "Matrice des valeurs")
    lignes_matrice = texte_matrice.split("\n")

    while running:

        # ------------------ ÉVÉNEMENTS ------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    running = False

                elif event.key == pygame.K_DOWN:
                    y_offset -= 20     # vers le bas
                elif event.key == pygame.K_UP:
                    y_offset += 20
                    y_offset = min(y_offset, 0)     # vers le haut
                elif event.key == pygame.K_RIGHT:
                    x_offset += 20     # droite
                elif event.key == pygame.K_LEFT:
                    x_offset = max(0, x_offset - 20)    # gauche

        # ------------------ AFFICHAGE ------------------
        screen.fill((0, 0, 0))

        x = base_x + x_offset
        y = base_y + y_offset

        # ---- TITRE ----
        screen.blit(font.render(f"Graphe n°{nb}", True, (255, 255, 0)), (x, y))
        y += 40

        # ---- INFOS ----
        screen.blit(font.render(f"Nombre de sommets : {n}", True, (255, 255, 255)), (x, y))
        y += 30

        screen.blit(font.render(f"Nombre d'arcs : {m}", True, (255, 255, 255)), (x, y))
        y += 40

        # ---- LISTE DES ARCS ----
        screen.blit(font.render("Liste des arcs :", True, (0, 200, 255)), (x, y))
        y += 30

        for (u, v, poids) in arcs:
            screen.blit(font.render(f"{u} -> {v} : {poids}", True, (200, 200, 200)), (x, y))
            y += 25

        y += 30

        # ---- MATRICE FORMATTÉE ----
        for ligne in lignes_matrice:
            screen.blit(font.render(ligne, True, (180, 180, 180)), (x, y))
            y += 25

        pygame.display.flip()
        clock.tick(60)

def afficher_floyd_pygame(screen, historique, has_cycle,sommets_absorbants):
    font = pygame.font.SysFont("consolas", 22)
    running = True
    index = 0           # index de l’étape affichée
    y_offset = 0        # scroll vertical
    go = False          # True => on affiche le message d’erreur
    # (et on n'affiche plus les matrices)

    while running:
        # ---------- 1) GESTION DES ÉVÉNEMENTS AVANT LE DESSIN ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # ESC
                if event.key == pygame.K_ESCAPE:
                    if has_cycle:
                        # 1er ESC : afficher le message
                        if not go:
                            go = True
                        # 2ᵉ ESC : quitter
                        else:
                            running = False
                    else:
                        # pas de circuit → ESC quitte directement
                        running = False

                # Navigation seulement si on n'est PAS en mode message d'erreur
                elif not (has_cycle and go):

                    # Étape suivante
                    if event.key == pygame.K_RIGHT:
                        index = min(index + 1, len(historique) - 1)
                        y_offset = 0

                    # Étape précédente
                    elif event.key == pygame.K_LEFT:
                        index = max(index - 1, 0)
                        y_offset = 0

                    # Aller à la dernière étape
                    elif event.key == pygame.K_l:
                        index = len(historique) - 1
                        y_offset = 0

                    # Scroll bas/haut (page)
                    elif event.key == pygame.K_DOWN:
                        y_offset -= 40
                    elif event.key == pygame.K_UP:
                        y_offset += 40
                        y_offset = min(y_offset, 0)

        # Si on a demandé de quitter dans les events
        if not running:
            break
        # ---------- 2) DESSIN DE L'ÉCRAN ----------
        screen.fill((0, 0, 0))
        y = 20 + y_offset

        # Ligne info
        info = font.render(
            f"Étape {index + 1}/{len(historique)}  |  ←/→ étapes  |  L dernière  |  ESC quitter",
            True, (200, 200, 0)
        )
        screen.blit(info, (20, 10))
        y = 50 + y_offset

        # --- MODE "MESSAGE D'ERREUR" SI CIRCUIT ABSORBANT ---
        if has_cycle and go:
            msg = (f"Impossible d'afficher les chemins : circuit absorbant détecté. "
                   f"\n-> Sommets impliqués : {sommets_absorbants}")
            for ligne in msg.split("\n"):
                text = font.render(ligne, True, (255, 100, 100))
                screen.blit(text, (20, y))
                y += 35

        # --- MODE NORMAL : AFFICHAGE DES MATRICES ---
        else:
            etape_texte = historique[index]
            lignes = etape_texte.split("\n")
            for ligne in lignes:
                text = font.render(ligne, True, (255, 255, 255))
                screen.blit(text, (20, y))
                y += 25

        pygame.display.flip()

def floyd(C):
    n = len(C)

    # Copie initiale de C dans L
    L = [[C[i][j] for j in range(n)] for i in range(n)]

    historique = []  # <<=== IMPORTANT

    # Matrice des prédécesseurs P
    P = [[-1 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and C[i][j] != INF:
                P[i][j] = i

    # Ajouter l’état initial
    texte = ""
    texte += afficher_matrice_text(L, "L (initial)") + "\n\n"
    texte += afficher_matrice_text(P, "P (initial)")
    historique.append(texte)

    afficher_matrice(L, "L (initial)")
    afficher_matrice(P, "P (initial)")

    has_cycle = False
    sommets_absorbants = []    # <<=== NOUVEAU

    # Triple boucle
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

        # Ajouter historique
        texte = ""
        texte += f"Étape k = {k}\n"
        texte += afficher_matrice_text(L, f"L après k = {k}") + "\n\n"
        texte += afficher_matrice_text(P, f"P après k = {k}")
        historique.append(texte)

        # Détection des cycles absorbants
        for i in range(n):
            if L[i][i] < 0:
                has_cycle = True
                if i not in sommets_absorbants:
                    sommets_absorbants.append(i)     # <<=== NOUVEAU

    # Affichage final
    if has_cycle:
        print("\n Circuit absorbant détecté.")
        print("-> Sommets impliqués :", sommets_absorbants)
    else:
        print("\n Aucun circuit absorbant détecté.")

    return historique, L, P, has_cycle, sommets_absorbants

def afficher_matrice_text(M, titre):
    lignes = []
    n = len(M)

    # Largeur d'une cellule (vraiment important)
    W = 6

    # Barres horizontales
    lignes.append("=" * (10 + W * n))
    lignes.append(titre)
    lignes.append("=" * (10 + W * n))

    # En-têtes
    header = "      " + "".join(f"[{j}]".center(W) for j in range(n))
    lignes.append(header)

    lignes.append("      " + "-" * (W * n))

    # Lignes du tableau
    for i in range(n):
        row = f"[{i}] | "
        for j in range(n):
            val = "INF" if M[i][j] >= 999999 else str(M[i][j])
            row += val.center(W)
        lignes.append(row)

    lignes.append("=" * (10 + W * n))
    return "\n".join(lignes)

def interface_chemins_pygame(screen, L, P,chemins_log):
    font = pygame.font.SysFont("consolas", 28)

    phase = 0           # 0 = saisie départ, 1 = saisie arrivée, 2 = affichage résultat
    saisie = ""
    s = None
    t = None
    resultat_texte = []

    running = True
    while running:
        screen.fill((0, 0, 0))

        # --- PHASE 0 : saisie départ ---
        if phase == 0:
            screen.blit(font.render("Sommet de DÉPART (ENTER pour valider)", True, (255,255,0)), (20, 20))
            screen.blit(font.render(f"0 .. {len(L)-1}", True, (255,255,255)), (20, 60))
            screen.blit(font.render(saisie, True, (100,200,255)), (20, 120))

        # --- PHASE 1 : saisie arrivée ---
        elif phase == 1:
            screen.blit(font.render("Sommet d’ARRIVÉE (ENTER pour valider)", True, (255,255,0)), (20, 20))
            screen.blit(font.render(f"0 .. {len(L)-1}", True, (255,255,255)), (20, 60))
            screen.blit(font.render(saisie, True, (100,200,255)), (20, 120))

        # --- PHASE 2 : affichage résultat ---
        elif phase == 2:
            y = 20
            for ligne in resultat_texte:
                screen.blit(font.render(ligne, True, (255,255,255)), (20, y))
                y += 35

            screen.blit(font.render("ENTER : nouveau chemin | ESC : quitter", True, (200,200,0)), (20, y + 20))
        pygame.display.flip()
        # ----------------- GESTION CLAVIER -----------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # Quitter
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Effacer caractère
                elif event.key == pygame.K_BACKSPACE:
                    saisie = saisie[:-1]

                # Valider
                elif event.key == pygame.K_RETURN:

                    # --- Phase 0 : valider départ ---
                    if phase == 0:
                        if saisie.isdigit():
                            s = int(saisie)
                            if 0 <= s < len(L):
                                saisie = ""
                                phase = 1
                            else:
                                saisie = ""

                    # --- Phase 1 : valider arrivée ---
                    elif phase == 1:
                        if saisie.isdigit():
                            t = int(saisie)
                            if 0 <= t < len(L):

                                # --- Récupération via print_f ---
                                texte = print_f(afficher_chemin, s, t, L, P)
                                resultat_texte = texte.split("\n")
                                chemins_log.append(texte)
                                phase = 2
                                saisie = ""
                            else:
                                saisie = ""

                    # --- Phase 2 : recommencer ---
                    elif phase == 2:
                        phase = 0
                        saisie = ""
                        resultat_texte = []

                # Ajouter chiffre
                else:
                    if event.unicode.isdigit():
                        saisie += event.unicode

def trace_execution_floyd(numero_graphe, n, m, arcs, matrice, historique, chemins_log):
    """
    Enregistre dans un fichier texte :
        - le graphe initial (n, m, arcs, matrice)
        - toutes les étapes de Floyd (L et P)
        - les chemins calculés par l'utilisateur
    """

    # ========= 1) Création dossier ===========
    dossier = "Trace_Floyd"
    os.makedirs(dossier, exist_ok=True)

    # Nom du fichier
    filename = os.path.join(dossier, f"Graphe_{numero_graphe}_trace.txt")

    # ========= 2) Construction du texte du graphe (intégré ici) ===========
    lignes = []
    lignes.append(f"Graphe n°{numero_graphe}")
    lignes.append(f"Nombre de sommets : {n}")
    lignes.append(f"Nombre d'arcs : {m}")
    lignes.append("")

    lignes.append("Liste des arcs :")
    for (u, v, poids) in arcs:
        lignes.append(f"  {u} -> {v} : {poids}")
    lignes.append("")

    # Matrice initiale
    lignes.append(afficher_matrice_text(matrice, "Matrice initiale"))

    graphe_log = "\n".join(lignes)

    # ========= 3) Écriture dans le fichier ===========
    with open(filename, "w", encoding="utf-8") as f:

        # --- GRAPHE INITIAL ---
        f.write("===== GRAPHE INITIAL =====\n")
        f.write(graphe_log + "\n\n")

        # --- ETAPES DE FLOYD ---
        f.write("===== ETAPES DE FLOYD =====\n")
        for i, etape in enumerate(historique):
            f.write(f"\n--- Étape {i} ---\n")
            f.write(etape + "\n")

        # --- CHEMINS ---
        f.write("\n===== CHEMINS CALCULES =====\n")
        if chemins_log:
            for ligne in chemins_log:
                f.write(ligne + "\n")
        else:
            f.write("Aucun chemin demandé.\n")

    print(f"Trace enregistrée dans : {filename}")
