# Function : Script qui gère tout les sons du jeu
# Author : Natan Humblet
# Date : 02/04/2026
# Version : 1.0 RELEASE

# Importation des modules nécessaires
import pygame
import os
import data

# Initialisation de pygame mixer
pygame.mixer.init()

# Chemins des fichiers audio
sound_30_seconds = "./assets/sounds/30_seconds.mp3"
music_30_seconds = "./assets/sounds/30_seconds_music.mp3"
fluffy_song_path = "./assets/sounds/fluffy_song.mp3"
win_sound_path = "./assets/sounds/winner_sound.mp3"
lose_sound_path = "./assets/sounds/lose_sound.mp3"
settings_song_path = "./assets/sounds/settings_song.mp3"
move_sound_path = "./assets/sounds/move_sound.mp3"

# Fonction pour charger les sons
def load_sounds():
    global sound_30, music_30, fluffy_song, win_sound, lose_sound, song_channel, sound_30_channel, music_30_channel, win_lose_channel, settings_song, move_sound, move_channel

    # Valeur par défaut : None
    sound_30, music_30, fluffy_song, win_sound, lose_sound, settings_song, move_sound = None, None, None, None, None, None, None

    # Définition des canaux
    move_channel = pygame.mixer.Channel(0)
    song_channel = pygame.mixer.Channel(1)
    sound_30_channel = pygame.mixer.Channel(2)
    music_30_channel = pygame.mixer.Channel(3)
    win_lose_channel = pygame.mixer.Channel(4)

    # Définition des sons
    if os.path.exists(sound_30_seconds):
        sound_30 = pygame.mixer.Sound(sound_30_seconds)
        sound_30 = volume_sounds(sound_30)
    if os.path.exists(music_30_seconds):
        music_30 = pygame.mixer.Sound(music_30_seconds)
        music_30 = volume_sounds(music_30)
    if os.path.exists(fluffy_song_path):
        fluffy_song = pygame.mixer.Sound(fluffy_song_path)
        fluffy_song = volume_sounds(fluffy_song)
    if os.path.exists(win_sound_path):
        win_sound = pygame.mixer.Sound(win_sound_path)
        win_sound = volume_sounds(win_sound)
    if os.path.exists(lose_sound_path):
        lose_sound = pygame.mixer.Sound(lose_sound_path)
        lose_sound = volume_sounds(lose_sound)
    if os.path.exists(settings_song_path):
        settings_song = pygame.mixer.Sound(settings_song_path)
        settings_song = volume_sounds(settings_song)
    if os.path.exists(move_sound_path):
        move_sound = pygame.mixer.Sound(move_sound_path)
        move_sound = volume_sounds(move_sound)

# Fonction pour régler le volume des sons
def volume_sounds(sound):

    volume = data.get_volume_value()

    sound.set_volume(volume)
    return sound

# Fonction pour jouer le son de 30 secondes
def play_30_seconds():
    if sound_30 is None or music_30 is None:
        print("Error: Sound files not loaded.")
        return

    if sound_30_channel.get_busy() or music_30_channel.get_busy():
        return

    # Si les sons sont activés
    if data.get_sounds():
        sound_30_channel.play(sound_30)
    # Si la musique est activée
    if data.get_music():
        music_30_channel.play(music_30)

# Fonction pour arrêter le son de 30 secondes
def stop_30_seconds():
    global sound_30_channel, music_30_channel
    sound_30_channel.stop()
    music_30_channel.stop()

# Fonction pour jouer le son de déplacement
def play_move_sound():
    if move_sound is None:
        print("Error: Move sound file not loaded.")
        return
    
    # Si les sons sont activés
    if data.get_sounds():
        move_channel.play(move_sound)

# Fonction pour jouer la fluffy song
def play_fluffy_song():
    if fluffy_song is None:
        print("Error: Fluffy song file not loaded.")
        return
    
    if song_channel.get_busy():
        return
    
    # Si la musique est activée
    if data.get_music():
        song_channel.play(fluffy_song, loops=-1)

# Fonction pour jouer la musique des paramètres
def play_settings_song():
    if settings_song is None:
        print("Error: Settings song file not loaded.")
        return
    
    if song_channel.get_busy():
        return
    
    # Si la musique est activée
    if data.get_music():
        song_channel.play(settings_song, loops=-1)

# Fonction pour arrêter la musique
def stop_song():
    global song_channel
    song_channel.stop()

# Fonction pour jouer le son de victoire
def play_win_sound():
    if win_sound is None:
        print("Error: Win sound file not loaded.")
        return

    # Si les sons sont activés
    if data.get_sounds():
        win_lose_channel.play(win_sound)

# Fonction pour jouer le son de défaite
def play_lose_sound():
    if lose_sound is None:
        print("Error: Lose sound file not loaded.")
        return
    
    # Si les sons sont activés
    if data.get_sounds():
        win_lose_channel.play(lose_sound)

# Fonction pour arrêter le son de victoire
def stop_win_lose_sound():
    global win_lose_channel
    win_lose_channel.stop()

def stop_all_sounds():
    stop_30_seconds()
    stop_song()
    stop_win_lose_sound()