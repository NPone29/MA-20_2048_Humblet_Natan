# Function : Script qui gère tout les processus visible du jeu
# Author : Natan Humblet
# Date : 01/04/2026
# Version : 1.7.1 DEV

# Importation des modules nécessaires
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import core
import sounds
import settings
import data

# Fonction pour gérer les touches pressées
def touche_pressee(event):
    global grid

    if event.keysym == "Up" or event.keysym == "w":
        print("Flèche du haut pressée !")
        grid = core.move.move_top(grid)
        reload_display(grid)

    elif event.keysym == "Down" or event.keysym == "s":
        print("Flèche du bas pressée !")
        grid = core.move.move_down(grid)
        reload_display(grid)

    elif event.keysym == "Left" or event.keysym == "a":
        print("Flèche de gauche pressée !")
        grid = core.move.move_left(grid)
        reload_display(grid)

    elif event.keysym == "Right" or event.keysym == "d":
        print("Flèche de droite pressée !")
        grid = core.move.move_right(grid)
        reload_display(grid)
    else:
        return
    
    if core.is_win(grid) and not core.win:
        data.save_win()
        root.unbind("<KeyPress>")

        sounds.stop_all_sounds()
        sounds.play_win_sound()

        end_frame.place(relx=0.5, rely=0.58, anchor="center")
        end_label.place(relx=0.5, rely=0.5, anchor="center")
        end_label.config(text="You Won!")
        button_continue.place(relx=0.5, rely=0.8, anchor="center")

    if core.is_game_over(grid):
        data.save_best_score()
        data.reset_win()
        root.unbind("<KeyPress>")
        if core.game_mode == "timeattack":
            data.delete_timeattack_time_remaining()
        
        sounds.stop_all_sounds()
        sounds.play_lose_sound()
        end_frame.place(relx=0.5, rely=0.58, anchor="center")
        end_label.place(relx=0.5, rely=0.5, anchor="center")
        end_label.config(text="Game Over")
        button_showgame.place(relx=0.5, rely=0.8, anchor="center")

def continue_game():
    end_frame.place_forget()
    root.bind("<KeyPress>", touche_pressee)

list_frame = []
list_label = []
timer_id = None

# Fonction pour démarrer le jeu
def start_game():
    global grid

    gamemode = data.get_game_mode()
    gap = 20 # space between labels
    x0=45 # horizontal beginning of labels
    y0=50 # vertical beginning of labels
    width=100 # horizontal distance between labels
    height=100 # vertical distance between labels

    last_played_grid = data.getgrid()
    if not last_played_grid:
        grid = core.create_grid(4, 4)
    else:
        if core.is_game_over(last_played_grid):
            data.deletegrid()
            data.reset_win()

            if gamemode == "timeattack":
                data.delete_timeattack_time_remaining()
            
            grid = core.create_grid(4, 4)
            core.score = 0
            label_score.config(text=f"Score: {core.score}")
            core.streak = 0
            label_streak.config(text=f"Streak: {core.streak}")  
        else:
            grid = last_played_grid
    #grid = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 4096], [8192, 0, 0, 0]]
    print(grid)

    core.best_streak = data.get_best_streak()
    label_streak_max.config(text=f"Best streak: {core.best_streak}")

    list_frame.clear()
    list_label.clear()
    for line in range(len(grid)):
        row_frames = []
        row_labels = []
        for col in range(len(grid[line])):
            value = grid[line][col]
            color = core.color[value]["color"]

            number_frame = Frame(main_frame, width=10, height=5, borderwidth=1, relief="solid", bg=color)
            number_frame.place(x=x0 + (width + gap) * col, y=y0 + (height + gap) * line, width=width, height=height)
            number = grid[line][col]
            if number == 0:
                number = None

            temp_label = Label(number_frame, text=number, font=("Arial", 24), bg=color)    
            temp_label.place(relx=0.5, rely=0.5, anchor="center")
           
            row_frames.append(number_frame)
            row_labels.append(temp_label)
        list_frame.append(row_frames)
        list_label.append(row_labels)
    
    sounds.stop_all_sounds()
    sounds.play_fluffy_song()

    if gamemode == "timeattack":
        timeattack_start()
    else: 
        frame_timeattack.pack_forget()

# Fonction pour redémarrer le jeu
def restart_game():
    global timer_id
    
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None
    data.delete_timeattack_time_remaining()

    end_frame.place_forget()
    button_continue.place_forget()
    button_showgame.place_forget()
    data.save_best_score()
    best_score = data.get_best_score()
    core.score = 0
    data.deletegrid()
    data.reset_win()

    data.save_best_streak(core.streak)
    core.best_streak = data.get_best_streak()
    data.reset_streak()
    core.streak = 0

    label_score.config(text=f"Score: {core.score}")
    label_score_max.config(text=f"Best score: {best_score}")

    label_streak.config(text=f"Streak: {core.streak}")
    label_streak_max.config(text=f"Best streak: {core.best_streak}")

    for line in range(len(list_frame)):
        for col in range(len(list_frame[line])):
            list_frame[line][col].destroy()
    list_frame.clear()
    list_label.clear()
    root.bind("<KeyPress>", touche_pressee)
    start_game()

# Fonction pour recharger l'affichage
def reload_display(grid):
    for line in range(len(grid)):
        for col in range(len(grid[line])):
            color = core.color[grid[line][col]]["color"]
            list_frame[line][col].config(bg=color)
            grid_number = grid[line][col]

            if grid_number == 0:
                grid_number = ""
            list_label[line][col].config(text=grid_number, bg=color)

    label_score.config(text=f"Score: {core.score}")
    label_streak.config(text=f"Streak: {core.streak}")

    core.best_streak = data.get_best_streak()
    label_streak_max.config(text=f"Best streak: {core.best_streak}")

def on_close():
    data.save_best_score()
    response = messagebox.askyesnocancel("Save your game?", "Do you want to save your game?")
    if response == True:
        data.save_game(grid, core.score)
        if core.game_mode == "timeattack":
            data.save_timeattack_time_remaining(core.get_time_remaining())
        root.destroy()
    elif response == False:
        data.deletegrid()
        data.reset_win()
        root.destroy()
    else:
        pass

def open_settings():
    global settings_frame
    core.pause_timer()
    settings_frame = settings.run_settings(root)
    end_frame.place_forget()
    menu_frame.pack_forget()
    main_frame.pack_forget()
    settings_frame.pack(pady=20)

    sounds.stop_all_sounds()
    sounds.play_settings_song()

def open_main_menu():
    global timer_id
    
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None
    
    if settings_frame:
        settings_frame.pack_forget()
    menu_frame.pack(side=TOP, fill=X)
    main_frame.pack(fill=BOTH, expand=True)

def timeattack_start():
    duration = data.get_timeattack_duration()
    core.start_timer(duration)
    frame_timeattack.pack(side=TOP, fill=X)
    label_timeattack.place(relx=0.5, rely=0.5, anchor="center")
    update_timeattack_label()

def update_timeattack_label():
    global timer_id
    
    label_timeattack.config(text=f"Time left: {core.get_time_remaining_str()}")
    elapsed_time = core.get_time_remaining()
    
    # Mettre en pause le timer si la partie est perdue
    if core.is_game_over(grid):
        core.pause_timer()
        return
    
    if elapsed_time <= 0:
        data.save_best_score()
        data.reset_win()
        root.unbind("<KeyPress>")

        sounds.stop_30_seconds()
        sounds.play_win_sound()
        data.delete_timeattack_time_remaining()

        end_frame.place(relx=0.5, rely=0.58, anchor="center")
        end_label.place(relx=0.5, rely=0.5, anchor="center")
        end_label.config(text="Game Over, final score: " + str(core.score))
        button_showgame.place(relx=0.5, rely=0.8, anchor="center")
        timer_id = None
    else:
        core.update_time()
        timer_id = root.after(1000, update_timeattack_label)

root = Tk()
root.title("2048 Game")
icon_img = Image.open("assets/icon.ico")
icon_img = icon_img.resize((32, 32), Image.LANCZOS)  # Redimensionner pour l'icône
icon_photo = ImageTk.PhotoImage(icon_img)
root.iconphoto(True, icon_photo)
root.geometry("550x665")
root.resizable(width=0,height=0)

menu_frame = Frame(root, height=125, bg="#493F66")
menu_frame.pack(side=TOP, fill=X)

label_gamemode = Label(menu_frame, text=f"Gamemode: {'Classic' if core.game_mode == 'classic' else 'Time Attack'}", font=("Helvetica", 10), bg="#493F66", fg="white")
label_gamemode.place(relx=0.0, rely=0.0)

label_2048 = Label(menu_frame, text="2048 Game", font=("Helvetica", 24), bg="#493F66", fg="white")
label_2048.place(relx=0.35, rely=0.1)

label_score = Label(menu_frame, text=f"Score: {core.score}", font=("Helvetica", 14), bg="#493F66", fg="white")
label_score.place(relx=0.66, rely=0.45)

bestscore = data.get_best_score()

label_score_max = Label(menu_frame, text=f"Best score: {bestscore}", font=("Helvetica", 14), bg="#493F66", fg="white")
label_score_max.place(relx=0.66, rely=0.7)

label_streak = Label(menu_frame, text=f"Streak: {core.streak}", font=("Helvetica", 14), bg="#493F66", fg="white")
label_streak.place(relx=0.05, rely=0.45)

label_streak_max = Label(menu_frame, text=f"Best streak: {core.best_streak}", font=("Helvetica", 14), bg="#493F66", fg="white")
label_streak_max.place(relx=0.05, rely=0.7)

button_restart = Button(menu_frame, text="Restart", font=("Helvetica", 12),
                        bg="deep sky blue", activebackground="dodger blue", command=restart_game)
button_restart.place(relx=0.5, rely=0.9, anchor="s")

# Chargement de l'image de fond (ciel étoilé)
astro_img = os.path.join(core.resource_path("assets/astro.jpg"))

original_image = Image.open(astro_img)

# Redimensionnement de l'image de fond
bg_resized = original_image.resize((550, 550), Image.LANCZOS)
bg = ImageTk.PhotoImage(bg_resized)

# Créer la Frame ou l'image de fond s'affichera
main_frame = Frame(root, bg="", bd=0)
main_frame.pack(fill=BOTH, expand=True)

canvas = Canvas(main_frame, width=500, height=600, highlightthickness=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

# Attribuer l'image de fond à la Frame
canvas.create_image(0, 0, image=bg, anchor="nw")
main_frame._bg_image = bg

settings_img = Image.open(core.resource_path("assets/settings.png"))
settings_img = settings_img.resize((20, 20), Image.LANCZOS)
settings_photo = ImageTk.PhotoImage(settings_img)

button_settings = Button(menu_frame, image=settings_photo, bg="light gray", command=open_settings)
button_settings.place(relx=0.95, rely=0)

end_frame = Frame(root, height=150, width=600, bg="white")
end_label = Label(end_frame, text="", font=("Helvetica", 24), bg="white", fg="black")

button_continue = Button(end_frame, text="Continue", font=("Helvetica", 12), bg="light green", command=continue_game)
button_showgame = Button(end_frame, text="Show Game", font=("Helvetica", 12), bg="light blue", command=lambda: end_frame.place_forget())

frame_timeattack = Frame(main_frame, height=45, bg="mediumpurple2")
label_timeattack = Label(frame_timeattack, text=f"Time left: 0", font=("Helvetica", 14), bg="mediumpurple2", fg="white")

def run_gfx():
    start_game()
    root.bind("<KeyPress>", touche_pressee)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()