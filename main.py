# Function : Script qui démarre le jeu
# Author : Natan Humblet
# Date : 01/04/2026
# Version : 1.7 DEV

# Importation des modules nécessaires
import json
import os

data = {
    "best_score": 0,
    "win": False,
    "best_streak": 0,
    "game_mode": "classic",  # "classic" ou "time_attack"
    "volume": 0.5,  # Valeur de volume par défaut (50%)
    "sounds": True,  # Sons activés par défaut
    "music": True  # Musique activée par défaut
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
    import sounds
    sounds.load_sounds()  # Charger tous les sons au démarrage pour éviter les lags
    gfx.run_gfx()
except Exception as e:
    print("The game closed successfully or crashed:", e)