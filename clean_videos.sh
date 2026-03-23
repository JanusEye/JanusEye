#!/bin/bash

# --- CONFIGURATION DYNAMIQUE ---
# On récupère le dossier où se trouve ce script (le dossier racine JanusEye)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Si le script est à la racine (comme app.py), BASE_DIR est SCRIPT_DIR
BASE_DIR="$SCRIPT_DIR"

VIDEO_DIR="$BASE_DIR/videos"
CONF_FILE="$BASE_DIR/config/januseye.conf"
LOG_FILE="$BASE_DIR/logs/januseye.log"

# --- LECTURE DE LA RÉTENTION ---
# On cherche retention_days dans le fichier de conf
if [ -f "$CONF_FILE" ]; then
    RETENTION_DAYS=$(grep -i "retention_days" "$CONF_FILE" | head -1 | cut -d'=' -f2 | tr -d '[:space:]')
else
    RETENTION_DAYS=7 # Valeur par défaut si pas de conf
fi

# Sécurité : si vide ou non numérique, on met 7 jours
[[ ! "$RETENTION_DAYS" =~ ^[0-9]+$ ]] && RETENTION_DAYS=7

# Conversion en minutes (1440 min = 1 jour)
RETENTION_MIN=$((RETENTION_DAYS * 1440))
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# --- EXÉCUTION DU NETTOYAGE ---
if [ -d "$VIDEO_DIR" ]; then
    # Sécurité anti-catastrophe (ne jamais nettoyer / ou un dossier vide)
    if [ "$VIDEO_DIR" != "/" ] && [ -n "$VIDEO_DIR" ]; then
        # Suppression des .mp4 et .jpg plus vieux que X minutes
        find "$VIDEO_DIR" -type f \( -name "*.mp4" -o -name "*.jpg" \) -mmin +$RETENTION_MIN -delete
        echo "[$TIMESTAMP] JanusEye: SYSTEME - Nettoyage auto effectué (> $RETENTION_DAYS jours) dans $VIDEO_DIR" >> "$LOG_FILE"
    fi
else
    # Si le dossier n'existe pas, on le crée pour la prochaine fois
    mkdir -p "$VIDEO_DIR"
    echo "[$TIMESTAMP] JanusEye: ERREUR - Dossier $VIDEO_DIR introuvable, création du répertoire." >> "$LOG_FILE"
fi
