#!/bin/bash

# 1. Chemins
BASE_DIR="/home/papy/JanusEye"
VIDEO_DIR="$BASE_DIR/videos"
CONF_FILE="$BASE_DIR/config/januseye.conf"
LOG_FILE="$BASE_DIR/logs/januseye.log"

# 2. Lecture de la rétention (en jours)
if [ -f "$CONF_FILE" ]; then
    RETENTION_DAYS=$(grep "^retention_days" "$CONF_FILE" | awk -F'=' '{print $2}' | xargs)
else
    RETENTION_DAYS=1
fi

# Sécurité si vide ou non numérique
[[ ! "$RETENTION_DAYS" =~ ^[0-9]+$ ]] && RETENTION_DAYS=1

# 3. Conversion des jours en minutes pour find (1 jour = 1440 min)
RETENTION_MIN=$((RETENTION_DAYS * 1440))

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ -d "$VIDEO_DIR" ]; then
    echo "$TIMESTAMP - SYSTEME : Nettoyage auto (> $RETENTION_DAYS jour(s))." >> "$LOG_FILE"
    
    # On utilise -mmin (minutes) pour être précis sur les 24h
    # Cela supprimera TOUT ce qui a plus de 24h (jpg et mp4)
    find "$VIDEO_DIR" -type f \( -name "*.mp4" -o -name "*.jpg" \) -mmin +$RETENTION_MIN -delete
    
    echo "$TIMESTAMP - SYSTEME : Nettoyage des fichiers effectué." >> "$LOG_FILE"
else
    echo "$TIMESTAMP - ERREUR : Dossier de stockage introuvable." >> "$LOG_FILE"
fi
