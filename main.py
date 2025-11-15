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
                        if 1 <= state.chosen_graphe <= 44:
                            state.choosing_graphe = False
                            fichier_test = f"graphe_projet/G{state.chosen_graphe}.txt"

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

                    elif state.chosen_graphe is not None:  # Menu après choix d'un graphe
                        if state.selected == 0:
                            print(f"Affichage du graphe {state.chosen_graphe}")

                        elif state.selected == 1:
                            print(f"floydification du graphe {state.chosen_graphe}")
                            state.choosing_floydification = True
                            state.selected = 0  # Réinitialisation pour afficher le graphe floydifier
                        #elif state.selected == 2:
                         #   print("Graphe Multiple") # Pour plustard lorsqu'on aura tout fait

                        elif state.selected == 2:
                            state.showing_help = True
                        elif state.selected == 3:
                            state.chosen_graphe = None
                            state.options = ["Choisir un graphe", "Options", "Aide", "Quitter"]
                        elif state.selected == 4:  # Quitter depuis le sous-menu
                            running = False

    state.clock.tick(60)  # Limite à 60 FPS


pygame.quit()
exit()
