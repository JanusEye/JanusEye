#!/bin/bash
# Script de sauvegarde JanusEye v2026 - Version Dynamique

# --- DÉTECTION DES CHEMINS ---
# Dossier actuel du projet (on suppose que le script est dans le dossier JanusEye)
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USER_HOME=$(eval echo "~$USER")
BACKUP_DIR="$USER_HOME/Backups_JanusEye"

DATE=$(date +%Y-%m-%d_%Hh%M)
FILE_NAME="backup_januseye_$DATE.tar.gz"

# Créer le dossier de sauvegarde s'il n'existe pas
mkdir -p "$BACKUP_DIR"

echo "--- 🛡️ Début de la sauvegarde JanusEye ---"
echo "Source  : $SOURCE_DIR"
echo "Cible   : $BACKUP_DIR/$FILE_NAME"

# Compression des fichiers essentiels
# On exclut les médias lourds (vidéos et photos de la galerie)
# On inclut le service systemd et la conf Apache s'ils existent
tar -czf "$BACKUP_DIR/$FILE_NAME" \
    --exclude="$SOURCE_DIR/videos/*" \
    --exclude="$SOURCE_DIR/static/recordings/*" \
    --exclude="$SOURCE_DIR/venv" \
    "$SOURCE_DIR" \
    /etc/systemd/system/januseye.service \
    /etc/apache2/sites-available/000-default-le-ssl.conf 2>/dev/null

echo "------------------------------------------------"
echo " ✅ SAUVEGARDE TERMINÉE AVEC SUCCÈS !"
echo " Fichier : $BACKUP_DIR/$FILE_NAME"
echo "------------------------------------------------"
echo " 💡 Conseil : Transférez ce fichier sur un support externe !"
