# Function : Script qui démarre le jeu
# Author : Natan Humblet
# Date : 02/04/2026
# Version : 1.0 RELEASE

# Importation des modules nécessaires
import json
import os

# Data de base pour le json
data = {
    "best_score": 0,
    "win": False,
    "best_streak": 0,
    "game_mode": "classic",
    "volume": 0.5,
    "sounds": True,
    "music": True
}

# Fonction pour s'assurer que le fichier de configuration existe
def ensure_settings(path="data.json"):
    # Vérifie si le fichier existe
    if not os.path.exists(path):
        try:
            # Crée le fichier avec les données par défaut
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.write("\n")
                print("Created default data.json")
        # Si une erreur se produit lors de la création du fichier, affiche un message d'erreur et quitter
        except Exception as e:
            print("Error creating data.json:", e)
            exit(1)


# Démarrer le jeu
try:
    
    ensure_settings()
    import gfx
    import sounds
    # Charger tous les sons au démarrage pour éviter les lags
    sounds.load_sounds()
    # Initialiser l'interface graphique
    gfx.run_gfx()
# Except pour le lancement du jeu
except Exception as e:
    print("Oops, it looks like the game crashed.", e)