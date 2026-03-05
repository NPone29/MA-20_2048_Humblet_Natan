# Function : Script qui gère tout les processus invisible du jeu
# author : Natan Humblet
# Date : 26/02/2026
# Version : 1.2 DEV

# Importation des modules nécessaires
import random
import math

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

score = 0

def spawn_new_case(grid, long, larg):
        
    empty_case = False
    for line in range(long):
        for col in range(larg):
            if grid[line][col] == 0:
                empty_case=True

        if not empty_case:
            return grid

        if random.random() < 0.1:
            number = 4
        else:
            number = 2

        while True:
            x = random.randint(0, long-1)
            y = random.randint(0, larg-1)

            if grid[x][y] == 0:
                grid[x][y] = number
                break

        return grid

# Fonction pour créer la grille avec les cases vides et les nombres
def create_grid(long,larg):
    grid = []
    for i in range(long):
        row = []
        for j in range(larg):
            row.append(0)
        grid.append(row)

    for i in range(2):
        grid = spawn_new_case(grid, long, larg)

    return grid

def pack4(a, b, c, d):
    global score

    if c == 0:
        c, d = d, 0
    if b == 0:
        b, c, d = c, d, 0
    if a == 0:
        a, b, c, d = b, c, d, 0
    
    if a == b:
        a = a * 2
        b = c
        c = d
        d = 0
        score += a
    if b == c:
        b = b * 2
        c = d
        d = 0
        score += b
    if c == d:
        c = c * 2
        d = 0
        score += c

    return(a, b, c, d)

class move:

    def move_left(grid):
        for column in range(len(grid)):
            grid[column] = pack4(grid[column][0], grid[column][1], grid[column][2], grid[column][3])
        return grid
    
    def move_right(grid):
        for column in range(len(grid)):
            temp = pack4(grid[column][3], grid[column][2], grid[column][1], grid[column][0])
            grid[column] = [temp[3], temp[2], temp[1], temp[0]]
        return grid
    
    def move_top(grid):

        new_grid = [list(row) for row in grid]

        for column in range(0, 4):
            liste_number = []
            for row in range(len(grid)):
                liste_number.append(grid[row][column])

            temp = pack4(liste_number[0], liste_number[1], liste_number[2], liste_number[3])
            temp = (temp[0], temp[1], temp[2], temp[3])

            for row in range(len(grid)):
                new_grid[row][column] = temp[row]
        return new_grid
            
    def move_down(grid):
        
        new_grid = [list(row) for row in grid]

        for column in range(0, 4):
            liste_number = []
            for row in range(len(grid)):
                liste_number.append(grid[row][column])
            print(liste_number)

            temp = pack4(liste_number[3], liste_number[2], liste_number[1], liste_number[0])
            temp = (temp[3], temp[2], temp[1], temp[0])  # on remet dans l'ordre (de haut à en bas)

            for row in range(len(grid)):
                new_grid[row][column] = temp[row]
        return new_grid

#print(move.move_down([[2, 0, 2, 0], [4, 4, 4, 0], [0, 2, 2, 4], [2, 2, 0, 2]]))