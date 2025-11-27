from Interface_utilisateur import *


state = State()  # Crée un objet contenant les états

# Boucle principale
running = True
while running:
    if state.choosing_options:  # Affichage des options
        draw_options_menu(screen, state)
    elif state.showing_help:  # Affichage de l'aide
        draw_help(screen, state)
    elif state.choosing_graphe:  # Affichage du choix du graphe
        draw_input_box(screen, state)

    elif state.chosen_graphe is not None:  # menu du graphe
        draw_menu(screen, state)
    else:
        draw_menu(screen, state)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if state.showing_help:
                if event.key == pygame.K_BACKSPACE:
                    state.showing_help = False

            # Gestion du choix du graphe
            elif state.choosing_graphe:
                if event.key == pygame.K_RETURN:
                    try:
                        state.chosen_graphe = int(state.input_text)
                        if 0 <= state.chosen_graphe <= 13:
                            state.choosing_graphe = False
                            fichier_test = f"graphes_tests/G{state.chosen_graphe}.txt"
                            print(f"Affichage du graphe {state.chosen_graphe}")
                            nb = state.chosen_graphe
                            Matrice, n, m, arcs = lire_graphe(fichier_test)
                            historique = []
                            chemins_log = []
                            trace_execution_floyd(nb, n, m, arcs, Matrice, historique, chemins_log)
                            afficher_matrice(Matrice)
                            afficher_graphe_pygame(screen, n, m, arcs, Matrice,nb)


                            state.options = [
                                "Afficher le graphe",
                                "floydifier le graphe",
                                "Aide",
                                "Retour au menu principal",
                                "Quitter",
                            ]
                            state.selected = 0
                            state.input_text = ""
                        else:
                            state.input_text = ""
                    except ValueError:
                        state.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    state.input_text = state.input_text[:-1]
                else:
                    state.input_text += event.unicode

            # Gestion des options
            elif state.choosing_options:
                if event.key == pygame.K_DOWN:
                    state.selected_mode = (state.selected_mode + 1) % len(state.mode_options)
                elif event.key == pygame.K_UP:
                    state.selected_mode = (state.selected_mode - 1) % len(state.mode_options)
                elif event.key == pygame.K_RETURN:
                    state.current_mode = state.mode_options[state.selected_mode]
                    state.current_background_color = MODES[state.current_mode]["background"]
                    state.text_color = MODES[state.current_mode]["text"]
                    state.choosing_options = False
                elif event.key == pygame.K_BACKSPACE:
                    state.choosing_options = False

            # Gestion de la floydification du graphe
            # elif state.choosing_floydification:

            # Gestion du menu principal
            else:
                if event.key == pygame.K_DOWN:
                    state.selected = (state.selected + 1) % len(state.options)
                elif event.key == pygame.K_UP:
                    state.selected = (state.selected - 1) % len(state.options)
                elif event.key == pygame.K_RETURN:
                    if state.chosen_graphe is None:  # Menu principal
                        if state.selected == 0:
                            state.choosing_graphe = True
                        elif state.selected == 1:
                            state.choosing_options = True
                        elif state.selected == 2:
                            state.showing_help = True
                        elif state.selected == 3:  # Quitter
                            running = False

                    elif state.chosen_graphe is not None:
                            if state.selected == 0:
                                print(f"Affichage du graphe {state.chosen_graphe}")
                                afficher_graphe_pygame(screen, n, m, arcs, Matrice,nb)

                            elif state.selected == 1:
                                print(f"floydification du graphe {state.chosen_graphe}")
                                # 1) Lancer Floyd sur la matrice
                                historique, L, P, has_cycle = floyd(Matrice)
                                afficher_floyd_pygame(screen, historique,has_cycle)
                                # 2) Si pas de circuit absorbant, lancer l’interface Chemins
                                if not has_cycle:
                                    print("\n=== Interface Chemins ===")
                                    # interface_chemins(L, P)
                                    # liste vide : sera remplie par interface_chemins_pygame
                                    interface_chemins_pygame(screen, L, P, chemins_log)
                                else:
                                    print("\nImpossible d'afficher les chemins : circuit absorbant détecté.")

                                # Pour revenir au menu Pygame
                                trace_execution_floyd(state.chosen_graphe, n, m, arcs, Matrice, historique, chemins_log)
                                state.choosing_floydification = False
                                state.selected = 0 # Réinitialisation pour afficher le graphe floydifier

                            elif state.selected == 2:
                                state.showing_help = True
                            elif state.selected == 3:
                                state.chosen_graphe = None
                                state.showing_graph = False
                                state.options = ["Choisir un graphe", "Options", "Aide", "Quitter"]
                            elif state.selected == 4:  # Quitter depuis le sous-menu
                                running = False

    state.clock.tick(60)  # Limite à 60 FPS


pygame.quit()
exit()
