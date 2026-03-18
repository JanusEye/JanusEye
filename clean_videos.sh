#!/bin/bash

# 1. Détection dynamique du chemin (Chemin générique)
# On récupère le dossier où se trouve ce script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# On définit BASE_DIR comme étant le dossier parent du script
# (Si votre script est dans /home/papy/JanusEye/scripts, BASE_DIR sera /home/papy/JanusEye)
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Si le script est à la racine du projet, utilisez : BASE_DIR="$SCRIPT_DIR"
# Mais généralement, on le place dans un sous-dossier.

VIDEO_DIR="$BASE_DIR/videos"
CONF_FILE="$BASE_DIR/config/januseye.conf"
LOG_FILE="$BASE_DIR/logs/januseye.log"

# 2. Lecture de la rétention (en jours)
if [ -f "$CONF_FILE" ]; then
    # On cherche la ligne retention_days, on nettoie les espaces et les retours à la ligne
    RETENTION_DAYS=$(grep -i "^retention_days" "$CONF_FILE" | cut -d'=' -f2 | tr -d '[:space:]')
else
    RETENTION_DAYS=1
fi

# Sécurité si vide ou non numérique
[[ ! "$RETENTION_DAYS" =~ ^[0-9]+$ ]] && RETENTION_DAYS=1

# 3. Conversion en minutes
RETENTION_MIN=$((RETENTION_DAYS * 1440))
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 4. Exécution du nettoyage
if [ -d "$VIDEO_DIR" ]; then
    # Log de début
    echo "$TIMESTAMP - SYSTEME : Nettoyage auto (> $RETENTION_DAYS jour(s))." >> "$LOG_FILE"
    
    # Suppression des fichiers anciens
    # On ajoute une sécurité pour ne pas supprimer à la racine en cas d'erreur de variable
    if [ "$VIDEO_DIR" != "/" ] && [ -n "$VIDEO_DIR" ]; then
        find "$VIDEO_DIR" -type f \( -name "*.mp4" -o -name "*.jpg" \) -mmin +$RETENTION_MIN -delete
        echo "$TIMESTAMP - SYSTEME : Nettoyage des fichiers effectué dans $VIDEO_DIR." >> "$LOG_FILE"
    fi
else
    echo "$TIMESTAMP - ERREUR : Dossier $VIDEO_DIR introuvable." >> "$LOG_FILE"
fi
