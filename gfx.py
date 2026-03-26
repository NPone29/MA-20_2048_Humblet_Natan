# Function : Script qui gère tout les processus visible du jeu
# author : Natan Humblet
# Date : 26/03/2026
# Version : 1.3.1 MAIN (branche main)

# Importation des modules nécessaires
from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import core

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
    # Vérifier si le joueur a gagné
    if core.is_win(grid) and not core.win:
        core.win = True
        # Désactiver l'événement keypress et afficher le message de victoire
        root.unbind("<KeyPress>")
        end_frame.place(relx=0.5, rely=0.58, anchor="center")
        end_label.place(relx=0.5, rely=0.5, anchor="center")
        end_label.config(text="You Won!")
        button_continue.place(relx=0.5, rely=0.8, anchor="center")

    # Vérifier si le jeu est terminé
    if core.is_game_over(grid):

        # Désactiver l'événement keypress et afficher le message de fin de jeu
        root.unbind("<KeyPress>")
        end_frame.place(relx=0.5, rely=0.58, anchor="center")
        end_label.place(relx=0.5, rely=0.5, anchor="center")
        end_label.config(text="Game Over")
        button_showgame.place(relx=0.5, rely=0.8, anchor="center")

# Fonction pour continuer de jouer quand l'utilisateur a gagné.
def continue_game():
    end_frame.place_forget()
    root.bind("<KeyPress>", touche_pressee)

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
    #grid = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 4096], [8192, 0, 0, 0]]
    print(grid)

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

# Fonction pour redémarrer le jeu
def restart_game():
    # Oublier la frame avec le message de victoire/fin de jeu si elle existe
    end_frame.place_forget()
    button_continue.place_forget()
    button_showgame.place_forget()

    # Réinitialiser le score et l'état de victoire
    core.score = 0
    core.win = False

    label_score.config(text=f"Score: {core.score}")

    # Détruire les frames et labels existants
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
            # Configurer la couleur de fond de la case (frame)
            list_frame[line][col].config(bg=color)
            grid_number = grid[line][col]

            if grid_number == 0:
                grid_number = ""
                # Configurer le texte de la case (label), la couleur  et le centrer
            list_label[line][col].config(text=grid_number, bg=color)

    label_score.config(text=f"Score: {core.score}")

root = Tk()
root.title("2048 Game")
root.geometry("550x650")
root.resizable(width=0,height=0)

menu_frame = Frame(root, height=100, bg="#493F66")
menu_frame.pack(side=TOP, fill=X)

label_2048 = Label(menu_frame, text="2048 Game", font=("Helvetica", 24), bg="#493F66", fg="white")
label_2048.place(relx=0.05, rely=0.1)

label_score = Label(menu_frame, text=f"Score: 0", font=("Helvetica", 14), bg="#493F66", fg="white")
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

# Définir la frame de fin de jeu/victoire
end_frame = Frame(root, height=150, width=600, bg="white")
end_label = Label(end_frame, text="", font=("Helvetica", 24), bg="white", fg="black")

button_continue = Button(end_frame, text="Continue", font=("Helvetica", 12), bg="light green", command=continue_game)
button_showgame = Button(end_frame, text="Show Game", font=("Helvetica", 12), bg="light blue", command=lambda: end_frame.place_forget())

start_game()

root.bind("<KeyPress>", touche_pressee)
root.mainloop()