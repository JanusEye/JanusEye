#!/bin/bash
# Script de sauvegarde JanusEye v2026
# Usage: ./backup_januseye.sh

USER_HOME="/home/papy"
SOURCE_DIR="$USER_HOME/JanusEye"
BACKUP_DIR="$USER_HOME/Backups_JanusEye"
DATE=$(date +%Y-%m-%d_%Hh%M)
FILE_NAME="backup_januseye_$DATE.tar.gz"

# Créer le dossier de sauvegarde s'il n'existe pas
mkdir -p $BACKUP_DIR

echo "--- 🛡️ Début de la sauvegarde JanusEye ---"

# Compression des fichiers essentiels
# On exclut les vidéos enregistrées pour ne pas avoir un fichier trop lourd
tar -czf $BACKUP_DIR/$FILE_NAME \
    --exclude="$SOURCE_DIR/static/recordings/*" \
    $SOURCE_DIR \
    /etc/systemd/system/januseye.service \
    /etc/apache2/sites-available/000-default-le-ssl.conf 2>/dev/null

echo "✅ Sauvegarde terminée : $BACKUP_DIR/$FILE_NAME"
echo "--- 💡 Conseil : Copiez ce fichier sur une clé USB ou votre PC ! ---"
