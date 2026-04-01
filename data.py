# Function : Script qui gère les données du jeu (json)
# Author : Natan Humblet
# Date : 01/04/2026
# Version : 1.7 DEV

import json
import core

def save_best_score():
        with open("data.json", "r") as f:
            data = json.load(f)
        if core.score > data["best_score"]:
            data["best_score"] = core.score
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
    data["score"] = core.score
    data["streak"] = core.streak
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

def get_game_mode():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("game_mode", "classic")

def get_timeattack_duration():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "timeattack_time_remaining" in data:
        return data["timeattack_time_remaining"]
    else:
        return data.get("timeattack_duration", 120)

def save_timeattack_time_remaining(duration):
    with open("data.json", "r") as f:
        data = json.load(f)
    data["timeattack_time_remaining"] = duration
    with open("data.json", "w") as f:
        json.dump(data, f)

def delete_timeattack_time_remaining():
    with open("data.json", "r") as f:
        data = json.load(f)
    if "timeattack_time_remaining" in data:
        del data["timeattack_time_remaining"]
    with open("data.json", "w") as f:
        json.dump(data, f)

def get_volume_value():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("volume", 0.5)

def get_sounds():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("sounds", True)

def get_music():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("music", True)

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