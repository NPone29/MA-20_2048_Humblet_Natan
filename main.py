# Function : Script qui démarre le jeu
# author : Natan Humblet
# Date : 26/03/2026
# Version : 1.6 DEV

# Importation des modules nécessaires
import json
import os

data = {
    "best_score": 0,
    "win": False,
    "best_streak": 0,
    "game_mode": "classic",  # "classic" ou "time_attack"
}

def ensure_settings(path="data.json"):
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.write("\n")
                print("Created default data.json")
        except Exception as e:
            print("Error creating data.json:", e)
            exit(1)


# Démarrer le jeu
try:
    if __name__ == "__main__":
        ensure_settings()
    import gfx
except Exception as e:
    print("The game closed successfully or crashed:", e)