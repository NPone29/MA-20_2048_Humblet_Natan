# Function : Menu du jeu 2048
# author : Natan Humblet
# Date : 26/03/2026
# Version : 1.1 DEV

from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import json
from tkinter import messagebox


def valide():
    status = messagebox.askyesnocancel("Settings confirmation", "Here are the current settings:\n\n"
                                   f"Game Mode: {'Classic' if gamemode.get() == 1 else 'Time Attack'}"
                                   f"{f"\nTime Attack Duration: {timeattack_duration.get()} seconds" if gamemode.get() == 2 else ""}\n\nDo you want to save it?")
    if not status:
        return

    if status:
        try:
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            data["game_mode"] = "classic" if gamemode.get() == 1 else "timeattack"
            if gamemode.get() == 2:
                data["timeattack_duration"] = timeattack_duration.get()
            elif "timeattack_duration" in data:
                del data["timeattack_duration"]

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
            print("Settings saved to data.json")
        except Exception as e:
            print("Erreur lors de la sauvegarde :", e)
    root.destroy()
    import gfx

root = Tk()

root.title("2048 Settings")
root.geometry("400x400")

frame_settings = Frame(root)
frame_settings.pack(pady=20)

label_title = Label(frame_settings, text="2048 Game", font=("Helvetica", 24))
label_title.pack(pady=20)

label_gamemode = Label(frame_settings, text="Choose a gamemode", font=("Helvetica", 14))
label_gamemode.pack(pady=10)

gamemode = IntVar(value=1)
timeattack_duration = IntVar(value=120)

radiobutton_classic = Radiobutton(frame_settings, text="Classic", variable=gamemode, value=1, font=("Helvetica", 12), fg="black", command=lambda: update_timeattack_input())
radiobutton_classic.pack()
radiobutton_timeattack = Radiobutton(frame_settings, text="Time Attack", variable=gamemode, value=2, font=("Helvetica", 12), fg="black", command=lambda: update_timeattack_input())
radiobutton_timeattack.pack()

# Champ pour la durée du Time Attack (caché par défaut)
label_timeattack = Label(frame_settings, text="Time Attack duration (seconds):", font=("Helvetica", 12))
spinbox_timeattack = Spinbox(frame_settings, from_=30, to=600, increment=10, textvariable=timeattack_duration, font=("Helvetica", 12), width=8)

def update_timeattack_input():
    if gamemode.get() == 2:
        label_timeattack.pack(pady=5)
        spinbox_timeattack.pack()
    else:
        label_timeattack.pack_forget()
        spinbox_timeattack.pack_forget()

update_timeattack_input()

frame_validate = Frame(root)
frame_validate.pack(pady=20)

button_validate = Button(frame_validate, text="Validate", font=("Helvetica", 12), bg="lightblue", activebackground="lightgreen", command=valide)
button_validate.pack(pady=20)

root.mainloop()