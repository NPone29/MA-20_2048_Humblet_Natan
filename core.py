# Function : Script qui gère tout les processus invisible du jeu
# author : Natan Humblet
# Date : 19/03/2026
# Version : 1.3 MAIN (branche main)

# Importation des modules nécessaires
import random

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

# Définition des variable nécessaire pour le bon fonctionnement du jeu
score = 0
win = False

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
            temp_grid = move.move_left(temp_grid, False)
            # Le False permet de ne pas calculer le score lors de la vérification des mouvements possibles
        elif i == 1:
            temp_grid = move.move_right(temp_grid, False)
        elif i == 2:
            temp_grid = move.move_top(temp_grid, False)
        elif i == 3: 
            temp_grid = move.move_down(temp_grid, False)

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
    # Sinon, la partie n'est pas gagné
    return False

# Fonction pour regrouper les valeurs à gauche
def pack4(a, b, c, d, calculate_score=True):
    global score

    # Fonction pour savoir si il y a eu un mouvement
    move = False

    # Bouger les cases si il n'y a pas de valeur
    if c == 0 and d != 0:
        move = True
        c, d = d, 0
    if b == 0 and (d != 0 or c != 0):
        move = True
        b, c, d = c, d, 0

    if a == 0 and (d != 0 or c != 0 or b != 0):
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
        # S'il faut calculer le score, alors ajouter la valeur.
        if calculate_score:
            score += a

    if b == c:
        b = b * 2
        c = d
        d = 0

        if b != 0:
            move = True
        # S'il faut calculer le score, alors ajouter la valeur.
        if calculate_score:
            score += b

    if c == d:
        c = c * 2
        d = 0

        if c != 0:
            move = True
        # S'il faut calculer le score, alors ajouter la valeur.
        if calculate_score:
            score += c

    # Retourner les nouvelles valeurs et le statut de mouvement
    return(a, b, c, d, move)

# Classe avec tout les mouvements
class move:

    # Fonction pour bouger à gauche
    def move_left(grid, calculate_score = True):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        # Pour chaque ligne, executé la fonction pack 4 qui permet de regrouper les valeurs à gauche
        for column in range(len(grid)):
            a, b, c, d, move = pack4(grid[column][0], grid[column][1], grid[column][2], grid[column][3], calculate_score)
            grid[column] = [a, b, c, d]
            if move:
                moved = True

        # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
        if moved:
            spawn_new_case(grid, 4, 4)
        return grid

    # Fonction pour bouger à droite
    def move_right(grid, calculate_score = True):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        # Pour chaque ligne, executé la fonction pack 4 avec les nombres à l'envers ce qui permet de regrouper les valeurs à droite
        for column in range(len(grid)):
            a, b, c, d, move = pack4(grid[column][3], grid[column][2], grid[column][1], grid[column][0], calculate_score)
            grid[column] = [d, c, b, a]

            if move:
                moved = True

        # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
        if moved:
            spawn_new_case(grid, 4, 4)
        return grid
    
    # Fonction pour bouger en haut
    def move_top(grid, calculate_score = True):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        new_grid = [list(row) for row in grid]
        for column in range(0, 4):
            liste_number = []
            for row in range(len(grid)):
                liste_number.append(grid[row][column])
            a, b, c, d, move = pack4(liste_number[0], liste_number[1], liste_number[2], liste_number[3], calculate_score)
            if move:
                moved = True

            # Remettre dans l'ordre (de haut à en bas)
            column_values = [a, b, c, d]
            for row in range(4):
                new_grid[row][column] = column_values[row]
        
        # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
        if moved:
           spawn_new_case(new_grid, 4, 4)
        return new_grid

    # Fonction pour bouger en bas
    def move_down(grid, calculate_score = True):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        # Créer une nouvelle grille
        new_grid = [list(row) for row in grid]

        # Pour chaque colonne, créer une liste des nombres
        for column in range(0, 4):
            liste_number = []

            # Pour chaque ligne, ajouter la valeur de la case à la liste
            for row in range(len(grid)):
                liste_number.append(grid[row][column])
            a, b, c, d, move = pack4(liste_number[3], liste_number[2], liste_number[1], liste_number[0], calculate_score)

            if move:
                moved = True

            # Remettre dans l'ordre (de haut à en bas)
            column_values = [d, c, b, a]
            for row in range(4):
                new_grid[row][column] = column_values[row]
       
       # Si il y a eu un mouvement, alors faire apparaître une nouvelle case
        if moved:
            spawn_new_case(new_grid, 4, 4)
        return new_grid
