# Function : Script qui gère tout les processus invisible du jeu
# author : Natan Humblet
# Date : 26/02/2026
# Version : 1.1

# Importation des modules nécessaires
import random
import math

# Dictionnaire avec toutes les couleurs des nombres
color = {
    1:{ "color": "#CAE2A8"},
    2: { "color": "#A9FC56"},
    3: { "color": "#61FA6C"},
    4: { "color": "#1BFFB7"},
    5: { "color": "#00E7F8"},
    6: { "color": "#437FFF"},
    7: { "color": "#6358FF"},
    8: { "color": "#9C56FD"},
    9: { "color": "#E24DF9"},
    10: { "color": "#FF326C"},
    11: { "color": "#FF8F4A"},
    12: { "color": "#FFE93F"},
    13: { "color": "#FFFFFF"}
}

# Fonction pour créer la grille avec les cases vides et les nombres
def create_grid(long,larg):
    grid = []
    for i in range(long):
        row = []
        for j in range(larg):
            row.append(None)
        grid.append(row)

    for i in range(2):

        if random.random() < 0.1:
            number = 4
        else:
            number = 2

        while True:
            x = random.randint(0, long-1)
            y = random.randint(0, larg-1)

            if grid[x][y] is None:
                grid[x][y] = number
                break

    return grid

# Fonction pour obtenir l'exposant d'un nombre
def get_number_exposant(number):

    if number is None:
        return None

    if number > 0 and (number & (number -1 )) == 0:
        exposant = int(math.log2(number))
        return exposant
    else:
        return None
