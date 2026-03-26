# Function : Script qui gère tout les processus invisible du jeu
# author : Natan Humblet
# Date : 26/03/2026
# Version : 1.5 DEV

# Importation des modules nécessaires
import random
import json

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

def spawn_new_case(grid, long, larg):
        
    #empty_case = False
    #for line in range(long):
    #    for col in range(larg):
    #        if grid[line][col] == 0:
    #            empty_case=True
#
    #    if not empty_case:
    #        return grid

        if random.random() < 0.2:
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

def is_game_over(grid):

    for column in grid:
        for case in column:
            if case == 0:
                return False
    
    for i in range(4):

        temp_grid = [list(row) for row in grid]

        if i == 0:
            temp_grid = move.move_left(temp_grid, False, False)
        elif i == 1:
            temp_grid = move.move_right(temp_grid, False, False)
        elif i == 2:
            temp_grid = move.move_top(temp_grid, False, False)
        elif i == 3: 
            temp_grid = move.move_down(temp_grid, False, False)

        if grid != temp_grid:
            return False
        
    return True

def is_win(grid):
    for column in grid:
        for case in column:
            if case >= 2048:
                return True
    return False

def pack4(a, b, c, d, calculate_score=True):
    global score

    move = False
    new_streak = False
    

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
    
    if a == b:
        a = a * 2
        b = c
        c = d
        d = 0

        if a != 0:
            move = True
            new_streak = True
        if calculate_score:
            score += a
    if b == c:
        b = b * 2
        c = d
        d = 0

        if b != 0:
            move = True
            new_streak = True
        if calculate_score:
            score += b
    if c == d:
        c = c * 2
        d = 0

        if c != 0:
            move = True
            new_streak = True

        if calculate_score:
            score += c

    return(a, b, c, d, move, new_streak)

class move:

    def move_left(grid, calculate_score=True, calculate_streak=True):
        global streak

        moved = False
        new_streak = False

        for column in range(len(grid)):
            a, b, c, d, move, streak_status = pack4(grid[column][0], grid[column][1], grid[column][2], grid[column][3], calculate_score=calculate_score)
            grid[column] = [a, b, c, d]
            if move:
                moved = True
            if streak_status:
                new_streak = True

        if moved:
            spawn_new_case(grid, 4, 4)
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                save_best_streak(streak)
                reset_streak()
                streak = 0

        return grid

    def move_right(grid, calculate_score=True, calculate_streak=True):
        global streak

        moved = False
        new_streak = False

        for column in range(len(grid)):
            a, b, c, d, move, streak_status = pack4(grid[column][3], grid[column][2], grid[column][1], grid[column][0], calculate_score=calculate_score)
            grid[column] = [d, c, b, a]

            if move:
                moved = True
            if streak_status:
                new_streak = True
        if moved:
            spawn_new_case(grid, 4, 4)

            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                save_best_streak(streak)
                reset_streak()
                streak = 0

        return grid

    def move_top(grid, calculate_score=True, calculate_streak=True):
        global streak

        move_flag = False
        new_streak = False

        new_grid = [list(row) for row in grid]
        for column in range(0, 4):
            liste_number = []
            for row in range(len(grid)):
                liste_number.append(grid[row][column])
            a, b, c, d, moved, streak_status = pack4(liste_number[0], liste_number[1], liste_number[2], liste_number[3], calculate_score=calculate_score)
            if moved:
                move_flag = True
            if streak_status:
                new_streak = True
            for row, val in enumerate([a, b, c, d]):
                new_grid[row][column] = val
        if move_flag:
            spawn_new_case(new_grid, 4, 4)
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                save_best_streak(streak)
                reset_streak()
                streak = 0

        return new_grid

    def move_down(grid, calculate_score=True, calculate_streak=True):
        global streak

        move_flag = False
        new_streak = False

        new_grid = [list(row) for row in grid]
        for column in range(0, 4):
            liste_number = []
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
            if new_streak and calculate_streak:
                streak += 1
            elif not new_streak and calculate_streak:
                save_best_streak(streak)
                reset_streak()
                streak = 0

        return new_grid

def save_best_score():
        with open("data.json", "r") as f:
            data = json.load(f)
        if score > data["best_score"]:
            data["best_score"] = score
        with open("data.json", "w") as f:
            json.dump(data, f)


def get_best_score():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data["best_score"]

def save_game(grid, score):
    with open("data.json", "r") as f:
        data = json.load(f)
    data["grid"] = grid
    data["score"] = score
    data["streak"] = streak
    with open("data.json", "w") as f:
        json.dump(data, f)

def getgrid():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("grid", None)

def getscore():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("score", 0)


def deletegrid():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "grid" in data:
        del data["grid"]
    if "score" in data:
        del data["score"]
    if "streak" in data:
        del data["streak"]
    with open("data.json", "w") as f:
        json.dump(data, f)

def save_win():
    global win
    with open("data.json", "r") as f:
        data = json.load(f)
    data["win"] = True
    with open("data.json", "w") as f:
        json.dump(data, f)
    win = True

def get_win():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("win", False)

def reset_win():
    with open("data.json", "r") as f:
        data = json.load(f)
    data["win"] = False
    with open("data.json", "w") as f:
        json.dump(data, f)

def get_streak():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("streak", 0)

def reset_streak():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "streak" in data:
        del data["streak"]
    with open("data.json", "w") as f:
        json.dump(data, f)

def get_best_streak():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("best_streak", 0)

def save_best_streak(streak):
    with open("data.json", "r") as f:
        data = json.load(f)
    if streak > data.get("best_streak", 0):
        data["best_streak"] = streak
    with open("data.json", "w") as f:
        json.dump(data, f)

win = get_win()
score = getscore()
streak = get_streak()
best_streak = get_best_streak()

#print(move.move_down([[2, 0, 2, 0], [4, 4, 4, 0], [0, 2, 2, 4], [2, 2, 0, 2]]))