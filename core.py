# Function : Script qui gère tout les processus invisible du jeu
# Author : Natan Humblet
# Date : 01/04/2026
# Version : 1.7 DEV

# Importation des modules nécessaires
import random
import data
import sounds

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
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            sounds.play_move_sound()

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
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            sounds.play_move_sound()

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
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            sounds.play_move_sound()

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
                data.save_best_streak(streak)
                data.reset_streak()
                streak = 0
            sounds.play_move_sound()

        return new_grid

win = data.get_win()
score = data.getscore()
streak = data.get_streak()
best_streak = data.get_best_streak()
game_mode = data.get_game_mode()

time_remain = 0
time_paused = False
time_30_started = False

def start_timer(seconds):
    global time_remain, time_paused, time_30_started
    time_remain = seconds
    time_paused = False
    time_30_started = False

def pause_timer():
    global time_paused
    time_paused = True

def resume_timer():
    global time_paused
    time_paused = False

def get_time_remaining():
    global time_remain
    return time_remain  # en secondes

def get_time_remaining_str():
    global time_remain
    mins, secs = divmod(time_remain, 60)
    return f"{mins:02d}:{secs:02d}"

def update_time():
    global time_remain, time_30_started

    if time_remain <= 30 and not time_30_started:
        sounds.stop_song()
        sounds.play_30_seconds()
        time_30_started = True
    
    if not time_paused:
      time_remain -= 1



#print(move.move_down([[2, 0, 2, 0], [4, 4, 4, 0], [0, 2, 2, 4], [2, 2, 0, 2]]))