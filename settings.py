# Function : Script qui gère les paramètres du jeu
# Author : Natan Humblet
# Date : 02/04/2026
# Version : 1.0 RELEASE

# Importation des modules nécessaires
from tkinter import *
from tkinter import messagebox
import gfx
import core
import sounds
import data

# Fonction pour retourner la frame des paramètres
def run_settings(parent=None):
    global frame_settings

    # Fonction pour valider les paramètres
    def valide():
        # Vérifier si l'utilisateur veut vraiment enregistrer les paramètres
        status = messagebox.askyesnocancel("Settings confirmation", "Here are the current settings:\n\n"
                                    f"Game Mode: {'Classic' if gamemode.get() == 1 else 'Time Attack'}"
                                    + (f"\nTime Attack Duration: {timeattack_duration.get()} seconds" if gamemode.get() == 2 else "")
                                    + f"\nSounds: {'Enabled' if sounds_enabled.get() else 'Disabled'}"
                                    + f"\nMusic: {'Enabled' if music_enabled.get() else 'Disabled'}"
                                    + f"\nVolume: {volume_scale.get() / 100:.2%}\n\nDo you want to save it?")

        # Si l'utilisateur ne veut pas enregistrer les paramètres
        if not status and status is not None:
            settings_cancel()

        # Si l'utilisateur veut enregistrer les paramètres
        if status:

            # Enregistrer les paramètres
            data.save_settings("classic" if gamemode.get() == 1 else "timeattack", timeattack_duration.get() if gamemode.get() == 2
                               else None, sounds_enabled.get(), music_enabled.get(), volume_scale.get() / 100)

            # Recharger les sons et redémarrer le jeu
            sounds.stop_song()
            sounds.load_sounds()
            frame_settings.forget()
            gfx.open_main_menu()
            gfx.restart_game()

    # Fonction pour réinitialiser les progrès
    def reset_progress():
        # Vérifier si l'utilisateur veut vraiment réinitialiser les progrès
        if messagebox.askyesno("Reset progress", "Are you sure you want to reset your progress? This action cannot be undone."):
            # Réinitialiser les progrès, recharger les sons et redémarrer le jeu
            data.reset_progress()
            sounds.stop_song()
            sounds.load_sounds()
            frame_settings.forget()
            gfx.open_main_menu()
            gfx.restart_game()
            # Afficher un message de confirmation
            messagebox.showinfo("Progress reset", "Your progress has been reset.")
        else:
            # Si l'utilisateur ne veut pas réinitialiser les progrès
            messagebox.showinfo("Progress reset", "Your progress has not been reset.")

    # Fonction pour revenir en jeu
    def settings_cancel():
        frame_settings.forget()
        gfx.menu_frame.pack(side=TOP, fill=X)
        gfx.main_frame.pack(fill=BOTH, expand=True)

        # Reprendre le minuteur si le mode de jeu est "timeattack"
        if core.game_mode == "timeattack":
            core.resume_timer()

        # Reprendre la musique
        sounds.stop_song()
        if core.time_remain and core.time_remain <= 30:
            sounds.play_30_seconds()
        elif core.time_remain and core.time_remain <= 0:
            pass
        else:
            sounds.play_fluffy_song()

    frame_settings = Frame(parent)
    frame_settings.pack(pady=20)

    frame_gamemode = Frame(frame_settings)
    frame_gamemode.pack(pady=10)

    label_title = Label(frame_gamemode, text="2048 Game", font=("Helvetica", 24))
    label_title.pack(pady=20)

    # Choix du mode de jeu
    label_gamemode = Label(frame_gamemode, text="Choose a gamemode", font=("Helvetica", 14))
    label_gamemode.pack(pady=10)

    current_gamemode = core.game_mode
    if current_gamemode == "classic":
        gamemode_value = 1
    elif current_gamemode == "timeattack":
        gamemode_value = 2
    gamemode = IntVar(value=gamemode_value)

    current_timeattack_duration = data.get_timeattack_duration()
    timeattack_duration = IntVar(value=current_timeattack_duration)

    radiobutton_classic = Radiobutton(frame_gamemode, text="Classic", variable=gamemode, value=1, font=("Helvetica", 12), fg="black", command=lambda: update_timeattack_input())
    radiobutton_classic.pack()
    radiobutton_timeattack = Radiobutton(frame_gamemode, text="Time Attack", variable=gamemode, value=2, font=("Helvetica", 12), fg="black", command=lambda: update_timeattack_input())
    radiobutton_timeattack.pack()

    # Champ pour la durée du Time Attack (caché par défaut)
    label_timeattack = Label(frame_gamemode, text="Time Attack duration (seconds):", font=("Helvetica", 12))
    spinbox_timeattack = Spinbox(frame_gamemode, from_=30, to=600, increment=10, textvariable=timeattack_duration, font=("Helvetica", 12), width=8)

    # Fonction pour mettre à jour l'input de durée du Time Attack
    def update_timeattack_input():
        if gamemode.get() == 2:
            label_timeattack.pack(pady=5)
            spinbox_timeattack.pack()
        else:
            label_timeattack.pack_forget()
            spinbox_timeattack.pack_forget()

    # Appeler la fonction pour mettre à jour l'input de durée du Time Attack
    update_timeattack_input()

    # Réglages des sons
    frame_sounds = Frame(frame_settings)
    frame_sounds.pack(pady=10)

    # Récupération des paramètres audio
    is_sounds_enabled = data.get_sounds()
    sounds_enabled = BooleanVar(value=is_sounds_enabled)
    is_music_enabled = data.get_music()
    music_enabled = BooleanVar(value=is_music_enabled)

    label_sounds = Label(frame_sounds, text="Sounds settings", font=("Helvetica", 14))
    label_sounds.pack(pady=10)

    checkbutton_sounds = Checkbutton(frame_sounds, text="Enable sounds", variable=sounds_enabled, font=("Helvetica", 12), fg="black")
    checkbutton_sounds.pack()
    
    checkbutton_music = Checkbutton(frame_sounds, text="Enable music", variable=music_enabled, font=("Helvetica", 12), fg="black")
    checkbutton_music.pack()

    label_volume_value = Label(frame_sounds, text="Sound: 0")
    label_volume_value.pack()

    # Fonction qui va afficher le volume du son
    def show_volume_value(valeur):
        label_volume_value.config(text=f"Sound: {int(float(valeur))} %")

    volume_scale = Scale(frame_sounds, from_=0, to=100, 
                         orient="horizontal", length=300,
                         command=show_volume_value)

    current_volume_level = int(data.get_volume_value() * 100)
    volume_scale.set(current_volume_level)
    volume_scale.pack(pady=10)

    frame_validate = Frame(frame_settings)
    frame_validate.pack(pady=20)

    button_cancel = Button(frame_validate, text="Cancel", font=("Helvetica", 12), bg="lightgray", activebackground="gray", command=settings_cancel)
    button_cancel.pack(side=LEFT, padx=10)

    button_validate = Button(frame_validate, text="Validate", font=("Helvetica", 12), bg="lightblue", activebackground="lightgreen", command=valide)
    button_validate.pack(side=LEFT, padx=10)

    button_reset = Button(frame_validate, text="Reset Progress", font=("Helvetica", 12), bg="lightcoral", activebackground="red", command=reset_progress)
    button_reset.pack(side=LEFT, padx=10)

    # retourne la frame des paramètres
    return frame_settings