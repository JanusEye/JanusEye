#!/bin/bash
# Script de sauvegarde JanusEye v2026 - Version 2.0.1 (Optimisée)

# --- DÉTECTION DES CHEMINS ---
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Détection de l'utilisateur réel
REAL_USER=${SUDO_USER:-$(whoami)}
USER_HOME=$(eval echo "~$REAL_USER")
BACKUP_DIR="$USER_HOME/Backups_JanusEye"

DATE=$(date +%Y-%m-%d_%Hh%M)
FILE_NAME="backup_januseye_light_$DATE.tar.gz"

# Créer le dossier de sauvegarde s'il n'existe pas
mkdir -p "$BACKUP_DIR"
chown "$REAL_USER:$REAL_USER" "$BACKUP_DIR"

echo "------------------------------------------------"
echo " 🛡️  Début de la sauvegarde JanusEye (Mode Light)"
echo " Source : $SOURCE_DIR"
echo " Cible  : $BACKUP_DIR/$FILE_NAME"
echo " Note   : Les vidéos et logs sont exclus."
echo "------------------------------------------------"

# 1. Préparation temporaire des fichiers système
TEMP_DIR="/tmp/januseye_backup_tmp"
rm -rf "$TEMP_DIR" # Nettoyage préventif
mkdir -p "$TEMP_DIR/sys_config"

[ -f /etc/systemd/system/januseye.service ] && cp /etc/systemd/system/januseye.service "$TEMP_DIR/sys_config/"
[ -f /etc/apache2/sites-available/000-default-le-ssl.conf ] && cp /etc/apache2/sites-available/000-default-le-ssl.conf "$TEMP_DIR/sys_config/"

# 2. Compression avec exclusions strictes
# Note : Pour tar, il est souvent préférable d'exclure le nom du dossier relativement au point de départ (-C)
tar -czf "$BACKUP_DIR/$FILE_NAME" \
    --exclude="videos" \
    --exclude="logs" \
    --exclude="venv" \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    -C "$SOURCE_DIR" . \
    -C "$TEMP_DIR" sys_config

# 3. Nettoyage final
rm -rf "$TEMP_DIR"
chown "$REAL_USER:$REAL_USER" "$BACKUP_DIR/$FILE_NAME"

echo "------------------------------------------------"
echo " ✅ SAUVEGARDE TERMINÉE AVEC SUCCÈS !"
echo " Taille archive : $(du -h "$BACKUP_DIR/$FILE_NAME" | cut -f1)"
echo "------------------------------------------------"
