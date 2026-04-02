# Function : Script qui gère les données du jeu (json)
# Author : Natan Humblet
# Date : 02/04/2026
# Version : 1.0 RELEASE

# Importation des modules nécessaires
import json
import core

# Fonction pour sauvegarder le meilleur score
def save_best_score():
    with open("data.json", "r") as f:
        data = json.load(f)
    if core.score > data["best_score"]:
        data["best_score"] = core.score
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour récupérer le meilleur score
def get_best_score():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data["best_score"]

# Fonction pour sauvegarder l'état du jeu
def save_game(grid):
    with open("data.json", "r") as f:
        data = json.load(f)
    data["grid"] = grid
    data["score"] = core.score
    data["streak"] = core.streak
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour récupérer la grille
def getgrid():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("grid", None)

# Fonction pour récupérer le score
def getscore():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("score", 0)

# Fonction pour supprimer la grille et ses éléments
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

# Fonction pour sauvegarder l'état de la victoire
def save_win():
    global win
    with open("data.json", "r") as f:
        data = json.load(f)
    data["win"] = True
    with open("data.json", "w") as f:
        json.dump(data, f)
    win = True

# Fonction pour récupérer l'état de la victoire
def get_win():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("win", False)

# Fonction pour réinitialiser l'état de la victoire
def reset_win():
    with open("data.json", "r") as f:
        data = json.load(f)
    data["win"] = False
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour récupérer la série actuelle
def get_streak():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("streak", 0)

# Fonction pour réinitialiser la série
def reset_streak():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "streak" in data:
        del data["streak"]
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour récupérer la meilleure série
def get_best_streak():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("best_streak", 0)

# Fonction pour sauvegarder la meilleure série
def save_best_streak(streak):
    with open("data.json", "r") as f:
        data = json.load(f)
    if streak > data.get("best_streak", 0):
        data["best_streak"] = streak
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour récupérer le mode de jeu
def get_game_mode():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("game_mode", "classic")

# Fonction pour récupérer la durée du mode timeattack
def get_timeattack_duration():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "timeattack_time_remaining" in data:
        return data["timeattack_time_remaining"]
    else:
        return data.get("timeattack_duration", 120)

# Fonction pour sauvegarder la durée du mode timeattack
def save_timeattack_time_remaining(duration):
    with open("data.json", "r") as f:
        data = json.load(f)
    data["timeattack_time_remaining"] = duration
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour supprimer la durée du mode timeattack
def delete_timeattack_time_remaining():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "timeattack_time_remaining" in data:
        del data["timeattack_time_remaining"]
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour récupérer la valeur du volume
def get_volume_value():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("volume", 0.5)

# Fonction pour récupérer l'état des sons
def get_sounds():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("sounds", True)

# Fonction pour récupérer l'état de la musique
def get_music():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("music", True)

# Fonction pour sauvegarder les paramètres
def save_settings(game_mode, timeattack_duration, sounds_enabled, music_enabled, volume):
    with open("data.json", "r") as f:
        data = json.load(f)
    data["game_mode"] = game_mode
    data["timeattack_duration"] = timeattack_duration
    data["sounds"] = sounds_enabled
    data["music"] = music_enabled
    data["volume"] = volume
    with open("data.json", "w") as f:
        json.dump(data, f)

# Fonction pour réinitialiser la progression
def reset_progress():
    with open("data.json", "r") as f:
        data = json.load(f)
    data["best_score"] = 0
    data["win"] = False
    data["best_streak"] = 0
    if "grid" in data:
        del data["grid"]
    if "score" in data:
        del data["score"]
    if "streak" in data:
        del data["streak"]
    with open("data.json", "w") as f:
        json.dump(data, f)