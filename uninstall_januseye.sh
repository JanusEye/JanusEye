#!/bin/bash

# --- CONFIGURATION ---
SERVICE_NAME="januseye.service"
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "------------------------------------------------"
echo "   JanusEye 2026 - Désinstallation Complète"
echo "   Dossier cible : $INSTALL_DIR"
echo "------------------------------------------------"

# 1. Arrêt et suppression du service Systemd
echo "[1/4] Arrêt du service en cours..."
sudo systemctl stop $SERVICE_NAME 2>/dev/null
sudo systemctl disable $SERVICE_NAME 2>/dev/null
if [ -f "/etc/systemd/system/$SERVICE_NAME" ]; then
    sudo rm "/etc/systemd/system/$SERVICE_NAME"
    sudo systemctl daemon-reload
    sudo systemctl reset-failed
    echo "✅ Service Systemd supprimé."
fi

# 2. Nettoyage des processus Python restants
echo "[2/4] Nettoyage des processus..."
pkill -f "python3 $INSTALL_DIR/app.py" 2>/dev/null

# 3. Suppression des fichiers (avec confirmation pour les vidéos)
echo "------------------------------------------------"
read -p "⚠️ Voulez-vous supprimer TOUT le dossier JanusEye (y compris les VIDÉOS) ? [y/N] " confirm
if [[ "$confirm" == [yY] || "$confirm" == [yY][eE][sS] ]]; then
    echo "[3/4] Suppression des fichiers et du VENV..."
    cd ..
    rm -rf "$INSTALL_DIR"
    echo "✅ Dossier $INSTALL_DIR supprimé."
else
    echo "[3/4] Conservation des fichiers. Seul le service a été retiré."
fi

# 4. Nettoyage des groupes (Optionnel)
echo "[4/4] Finalisation..."
echo "Note : L'utilisateur reste dans le groupe 'video' pour ne pas casser d'autres logiciels."

echo "------------------------------------------------"
echo " ✅ DÉSINSTALLATION TERMINÉE."
echo "------------------------------------------------"
