#!/bin/bash

# Configuration des chemins
INSTALL_DIR="/home/papy/JanusEye"
SERVICE_NAME="januseye.service"

echo "------------------------------------------------"
echo "   JanusEye 2026 - Installation Automatisée"
echo "------------------------------------------------"

# 1. Création de la structure des dossiers
echo "[1/6] Création des répertoires..."
mkdir -p "$INSTALL_DIR/videos"
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/config"
mkdir -p "$INSTALL_DIR/templates"

# 2. Installation des dépendances système
echo "[2/6] Installation des paquets système (Python & Camera)..."
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip libopencv-dev python3-opencv

# 3. Création de l'environnement virtuel (VENV)
echo "[3/6] Configuration de l'environnement Python..."
cd "$INSTALL_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install flask opencv-python numpy requests

# 4. Configuration des permissions
echo "[4/6] Réglage des droits d'exécution..."
chmod +x "$INSTALL_DIR/clean_videos.sh"
sudo chown -R papy:papy "$INSTALL_DIR"

# 5. Création du service Systemd pour le démarrage automatique
echo "[5/6] Configuration du service de démarrage..."
sudo bash -c "cat > /etc/systemd/system/$SERVICE_NAME" << EOF
[Unit]
Description=Serveur de Surveillance JanusEye
After=network.target

[Service]
User=papy
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 6. Activation du service
echo "[6/6] Activation et lancement..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "------------------------------------------------"
echo " ✅ INSTALLATION TERMINÉE AVEC SUCCÈS !"
echo " Accès : http://$(hostname -I | awk '{print $1}'):5000"
echo "------------------------------------------------"