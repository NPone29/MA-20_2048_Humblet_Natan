# Function : Script qui gère tout les processus invisible du jeu
# Author : Natan Humblet
# Date : 02/04/2026
# Version : 1.0 RELEASE

# Importation des modules nécessaires
import random
import data
import sounds
import os
import sys

# Dictionnaire avec toutes les couleurs des nombres
color = {
    0: { "color": "#C5A0A0"},
    2: { "color": "#CAE2A8"},
    4: { "color": "#A9FC56"},
    8: { "color": "#61FA6C"},
    16: { "color": "#1BFFB7"},
    32: { "color": "#00E7F8"},
    64: { "color": "#437FFF"},
    128 : { "color": "#6358FF"},
    256: { "color": "#9C56FD"},
    512: { "color": "#E24DF9"},
    1024: { "color": "#FF326C"},
    2048: { "color": "#FF8F4A"},
    4096: { "color": "#FFE93F"},
    8192: { "color": "#FFFFFF"}
}

# Fonction pour faire apparaître une nouvelle case
def spawn_new_case(grid, long, larg):

    # 20% de chance d'avoir un 4 et 80 % un 2.
    if random.random() < 0.2:
        number = 4
    else:
        number = 2

    # Boucle pour trouver une case vide
    while True:
        x = random.randint(0, long-1)
        y = random.randint(0, larg-1)

        # Attribuer la valeur à la case vide
        if grid[x][y] == 0:
            grid[x][y] = number
            break

    return grid

# Fonction pour créer la grille avec les cases vides et les nombres
def create_grid(long,larg):
    grid = []

    # Création de la grille avec les valeurs long et larg
    for i in range(long):
        row = []
        for j in range(larg):
            row.append(0)
        grid.append(row)

    # Faire apparaître deux nouvelles cases
    for i in range(2):
        grid = spawn_new_case(grid, long, larg)

    return grid

# Fonction pour vérifier si le jeu est terminé
def is_game_over(grid):
    
    # Regarder si une case est vide
    for column in grid:
        for case in column:
            if case == 0:
                # Si il y a une case vide alors ce n'est pas la fin.
                return False
    
    for i in range(4):

        # Créer une nouvelle grid identique
        temp_grid = [list(row) for row in grid]

        # Tester chaque mouvement pour vérifier si il y a un mouvement possible.
        if i == 0:
            # Le False permet de ne pas calculer le score et la série lors de la vérification des mouvements possibles
            temp_grid = move.move_left(temp_grid, False, False)
        elif i == 1:
            temp_grid = move.move_right(temp_grid, False, False)
        elif i == 2:
            temp_grid = move.move_top(temp_grid, False, False)
        elif i == 3: 
            temp_grid = move.move_down(temp_grid, False, False)

        # Si la gride n'est pas égale à la gride qui a fait un mouvement
        # Alors la partie n'est pas fini.

        if grid != temp_grid:
            return False
    # La partie est terminé.
    return True

# Fonction pour voir si l'utilisateur a gagné.
def is_win(grid):
    # Une boucle for, pour regarder si une des valeurs est égale ou plus grand à 2048
    for column in grid:
        for case in column:
            if case >= 2048:
                return True
    # Sinon, la partie n'est pas gagnée
    return False

# Fonction pour regrouper les valeurs à gauche
def pack4(a, b, c, d, calculate_score=True):
    global score

    move = False
    new_streak = False
    
    # Bouger les cases si il n'y a pas de valeur
    if c == 0:
        if(d != 0):
            move = True

        c, d = d, 0
    if b == 0:
        if(d != 0 or c != 0): 
            move = True

        b, c, d = c, d, 0
    if a == 0:
        if(d != 0 or c != 0 or b != 0):
            move = True
        a, b, c, d = b, c, d, 0
    
    # Regrouper les valeurs
    if a == b:
        a = a * 2
        b = c
        c = d
        d = 0

        if a != 0:
            move = True
            new_streak = True
        # S'il faut calculer le score, alors ajouter la valeur.
        if calculate_score:
            score += a
    if b == c:
        b = b * 2
        c = d
        d = 0

        if b != 0:
            move = True
            new_streak = True
        # S'il faut calculer le score, alors ajouter la valeur.
        if calculate_score:
            score += b
    if c == d:
        c = c * 2
        d = 0

        if c != 0:
            move = True
            new_streak = True

        # S'il faut calculer le score, alors ajouter la valeur.
        if calculate_score:
            score += c

    # Retourner les nouvelles valeurs, le status de mouvement et la nouvelle série
    return(a, b, c, d, move, new_streak)

class move:

    # Fonction pour bouger à gauche
    def move_left(grid, calculate_score=True, calculate_streak=True):
        global streak

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False
        # Variable qui permet de savoir si la streak est continuée ou alors réinitialisée.
        new_streak = False

        # Pour chaque ligne, executé la fonction pack 4 qui permet de regrouper les valeurs à gauche
        for column in range(len(grid)):
            a, b, c, d, move, streak_status = pack4(grid[column][0], grid[column][1], grid[column][2], grid[column][3], calculate_score=calculate_score)
            grid[column] = [a, b, c, d]
            if move:
                moved = True
            if streak_status:
                new_streak = True

        # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
        if moved:
            spawn_new_case(grid, 4, 4)

            # Si le joueur continue sa série alors augmenter la série, sinon réinitialiser la série
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                # Sauvegarder la meilleure série
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            # Jouer le son du mouvement
            sounds.play_move_sound()

        return grid
    
    # Fonction pour bouger à droite
    def move_right(grid, calculate_score=True, calculate_streak=True):
        global streak

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False
        # Variable qui permet de savoir si la streak est continuée ou alors réinitialisée.
        new_streak = False

        # Pour chaque ligne, executé la fonction pack 4 avec les nombres à l'envers ce qui permet de regrouper les valeurs à droite
        for column in range(len(grid)):
            a, b, c, d, move, streak_status = pack4(grid[column][3], grid[column][2], grid[column][1], grid[column][0], calculate_score=calculate_score)
            grid[column] = [d, c, b, a]

            if move:
                moved = True
            if streak_status:
                new_streak = True
        # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
        if moved:
            spawn_new_case(grid, 4, 4)

            # Si le joueur continue sa série alors augmenter la série, sinon réinitialiser la série
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                # Sauvegarder la meilleure série
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            # Jouer le son du mouvement
            sounds.play_move_sound()

        return grid

    def move_top(grid, calculate_score=True, calculate_streak=True):
        global streak

        # Variable qui permet de dire si un mouvement a été fait.
        move_flag = False
        # Variable qui permet de savoir si la streak est continuée ou alors réinitialisée.
        new_streak = False
        # Créer une nouvelle grille
        new_grid = [list(row) for row in grid]

        # Pour chaque colonne, créer une liste des nombres
        for column in range(0, 4):
            liste_number = []

            # Pour chaque ligne, ajouter la valeur de la case à la liste
            for row in range(len(grid)):
                liste_number.append(grid[row][column])

            a, b, c, d, moved, streak_status = pack4(liste_number[0], liste_number[1], liste_number[2], liste_number[3], calculate_score=calculate_score)
            if moved:
                move_flag = True

            if streak_status:
                new_streak = True
            # Remettre dans l'ordre (de haut à en bas)
            for row, val in enumerate([a, b, c, d]):
                new_grid[row][column] = val
        if move_flag:
             # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
            spawn_new_case(new_grid, 4, 4)

             # Si le joueur continue sa série alors augmenter la série, sinon réinitialiser la série
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                # Sauvegarder la meilleure série
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            # Jouer le son du mouvement
            sounds.play_move_sound()

        return new_grid

    def move_down(grid, calculate_score=True, calculate_streak=True):
        global streak

        # Variable qui permet de dire si un mouvement a été fait.
        move_flag = False
        # Variable qui permet de savoir si la streak est continuée ou alors réinitialisée.
        new_streak = False

        # Créer une nouvelle grille
        new_grid = [list(row) for row in grid]

        # Pour chaque colonne, créer une liste des nombres
        for column in range(0, 4):
            liste_number = []

            # Pour chaque ligne, ajouter la valeur de la case à la liste
            for row in range(len(grid)):
                liste_number.append(grid[row][column])
            a, b, c, d, moved, streak_status = pack4(liste_number[3], liste_number[2], liste_number[1], liste_number[0], calculate_score=calculate_score)
            if moved:
                move_flag = True
            if streak_status:
                new_streak = True
            # Remettre dans l'ordre (de haut à en bas)
            for row, val in enumerate([d, c, b, a]):
                new_grid[row][column] = val
        if move_flag:
            spawn_new_case(new_grid, 4, 4)

             # Si le joueur continue sa série alors augmenter la série, sinon réinitialiser la série
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                # Sauvegarder la meilleure série
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            # Jouer le son du mouvement
            sounds.play_move_sound()

        return new_grid

# Variables globales pour le suivi du jeu
win = data.get_win()
score = data.getscore()
streak = data.get_streak()
best_streak = data.get_best_streak()
game_mode = data.get_game_mode()

time_remain = 0
time_paused = False
time_30_started = False

# Fonction pour démarrer le minuteur
def start_timer(seconds):
    global time_remain, time_paused, time_30_started
    time_remain = seconds
    time_paused = False
    time_30_started = False

# Fonction pour mettre en pause le minuteur
def pause_timer():
    global time_paused
    time_paused = True

# Fonction pour reprendre le minuteur
def resume_timer():
    global time_paused
    time_paused = False

# Fonction pour obtenir le temps restant
def get_time_remaining():
    global time_remain
    return time_remain  # en secondes

# Fonction pour obtenir le temps restant sous forme de chaîne
def get_time_remaining_str():
    global time_remain
    mins, secs = divmod(time_remain, 60)
    return f"{mins:02d}:{secs:02d}"

# Fonction pour mettre à jour le temps
def update_time():
    global time_remain, time_30_started

    if time_remain <= 30 and not time_30_started:
        sounds.stop_song()
        sounds.play_30_seconds()
        time_30_started = True
    
    if not time_paused:
      time_remain -= 1

def resource_path(rel_path):
    """
    Retourne le chemin absolu utilisable à l'exécution.
    Fonctionne normalement et dans les bundles PyInstaller (--onefile) via sys._MEIPASS.
    """
    # Cette fonction a été reprise de mon précédent projet MA-24
    try:
        # Récupérer le chemin du dossier temporaire
        base = sys._MEIPASS
    except Exception:
        # Récupérer le chemin du dossier de l'application
        base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, rel_path)



#print(move.move_down([[2, 0, 2, 0], [4, 4, 4, 0], [0, 2, 2, 4], [2, 2, 0, 2]]))