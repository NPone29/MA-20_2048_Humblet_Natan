# Function : Script qui gère tout les processus visible du jeu
# author : Natan Humblet
# Date : 26/02/2026
# Version : 1.1

# Importation des modules nécessaires
from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import core

# Fonction pour gérer les touches pressées
def touche_pressee(event):
    if event.keysym == "Up" or event.keysym == "w":
        print("Flèche du haut pressée !")
    elif event.keysym == "Down" or event.keysym == "s":
        print("Flèche du bas pressée !")
    elif event.keysym == "Left" or event.keysym == "a":
        print("Flèche de gauche pressée !")
    elif event.keysym == "Right" or event.keysym == "d":
        print("Flèche de droite pressée !")

list_frame = []
list_label = []

# Fonction pour démarrer le jeu
def start_game():
    global grid

    gap = 20 # space between labels
    x0=45 # horizontal beginning of labels
    y0=50 # vertical beginning of labels
    width=100 # horizontal distance between labels
    height=100 # vertical distance between labels

    grid = core.create_grid(4, 4)
    #grid = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 4096], [8192, None, None, None]]
    print(grid)

    list_frame.clear()
    list_label.clear()
    for line in range(len(grid)):
        row_frames = []
        row_labels = []
        for col in range(len(grid[line])):
            number_exposant = core.get_number_exposant(grid[line][col])
            color = core.color[number_exposant]["color"] if number_exposant is not None else "#C5A0A0"

            number_frame = Frame(main_frame, width=10, height=5, borderwidth=1, relief="solid", bg=color)
            number_frame.place(x=x0 + (width + gap) * col, y=y0 + (height + gap) * line, width=width, height=height)
            number = grid[line][col]
            temp_label = None
            temp_label = Label(number_frame, text=number, font=("Arial", 24), bg=color)
            try:
                if number is not None and int(number) < 10:
                    temp_label.place(relx=0.4, rely=0.3)
                else:
                    temp_label.place(relx=0.5, rely=0.5, anchor="center")
            except:
                temp_label.place(relx=0.5, rely=0.5, anchor="center")
            row_frames.append(number_frame)
            row_labels.append(temp_label)
        list_frame.append(row_frames)
        list_label.append(row_labels)

# Fonction pour redémarrer le jeu
def restart_game():
    for line in range(len(list_frame)):
        for col in range(len(list_frame[line])):
            list_frame[line][col].destroy()
    list_frame.clear()
    list_label.clear()
    start_game()

# Fonction pour recharger l'affichage
def reload_display(grid):
    for line in range(len(grid)):
        for col in range(len(grid[line])):
            color = core.color[core.get_number_exposant(grid[line][col])]["color"] if core.get_number_exposant(grid[line][col]) is not None else "#C5A0A0"
            list_frame[line][col].config(bg=color)
            grid_number = grid[line][col]
            list_label[line][col].config(text=grid_number)

root = Tk()
root.title("2048 Game")
root.geometry("550x650")

menu_frame = Frame(root, height=100, bg="#493F66")
menu_frame.pack(side=TOP, fill=X)

label_2048 = Label(menu_frame, text="2048 Game", font=("Helvetica", 24), bg="#493F66", fg="white")
label_2048.place(relx=0.05, rely=0.1)

label_score = Label(menu_frame, text="Score: 0", font=("Helvetica", 14), bg="#493F66", fg="white")
label_score.place(relx=0.66, rely=0.2)

button_restart = Button(menu_frame, text="Restart", font=("Helvetica", 12), 
                        bg="deep sky blue", activebackground="dodger blue", command=restart_game)
button_restart.place(relx=0.5, rely=0.9, anchor="s")

# Chargement de l'image de fond (ciel étoilé)
try:
    base = sys._MEIPASS
except Exception:
    base = os.path.abspath(os.path.dirname(__file__))
astro_img = os.path.join(base, "img/astro.jpg")

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

start_game()

root.bind("<KeyPress>", touche_pressee)
root.mainloop()