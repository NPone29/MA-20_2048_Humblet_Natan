# Function : Script qui gère tout les processus invisible du jeu
# author : Natan Humblet
# Date : 05/03/2026
# Version : 1.2 MAIN

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

# Fonction pour regrouper les valeurs à gauche
def pack4(a, b, c, d):

    # Fonction pour savoir si il y a eu un mouvement
    move = False

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
    if b == c:
        b = b * 2
        c = d
        d = 0

        if b != 0:
            move = True

    if c == d:
        c = c * 2
        d = 0

        if c != 0:
            move = True

    # Retourner les nouvelles valeurs et le statut de mouvement
    return(a, b, c, d, move)

# Classe avec tout les mouvements
class move:

    # Fonction pour bouger à gauche
    def move_left(grid):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        # Pour chaque ligne, executé la fonction pack 4 qui permet de regrouper les valeurs à gauche
        for column in range(len(grid)):
            a, b, c, d, move = pack4(grid[column][0], grid[column][1], grid[column][2], grid[column][3])
            grid[column] = [a, b, c, d]
            if move:
                moved = True

        return grid

    # Fonction pour bouger à droite
    def move_right(grid):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        # Pour chaque ligne, executé la fonction pack 4 avec les nombres à l'envers ce qui permet de regrouper les valeurs à droite
        for column in range(len(grid)):
            a, b, c, d, move = pack4(grid[column][3], grid[column][2], grid[column][1], grid[column][0])
            grid[column] = [d, c, b, a]

            if move:
                moved = True
        return grid
    
    # Fonction pour bouger en haut
    def move_top(grid):

        # Variable qui permet de dire si un mouvement a été fait.
        moved = False

        new_grid = [list(row) for row in grid]
        for column in range(0, 4):
            liste_number = []
            for row in range(len(grid)):
                liste_number.append(grid[row][column])
            a, b, c, d, move = pack4(liste_number[0], liste_number[1], liste_number[2], liste_number[3])
            if move:
                moved = True

            # Remettre dans l'ordre (de haut à en bas)
            column_values = [a, b, c, d]
            for row in range(4):
                new_grid[row][column] = column_values[row]
        
        return new_grid

    # Fonction pour bouger en bas
    def move_down(grid):

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
            a, b, c, d, move = pack4(liste_number[3], liste_number[2], liste_number[1], liste_number[0])

            if move:
                moved = True

            # Remettre dans l'ordre (de haut à en bas)
            column_values = [d, c, b, a]
            for row in range(4):
                new_grid[row][column] = column_values[row]
       
        return new_grid

#print(move.move_down([[2, 0, 2, 0], [4, 4, 4, 0], [0, 2, 2, 4], [2, 2, 0, 2]]))