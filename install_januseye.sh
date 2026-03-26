#!/bin/bash

# --- CONFIGURATION DYNAMIQUE ---
IF_SUDO_USER=${SUDO_USER:-$(whoami)}
USER_NAME=$IF_SUDO_USER
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="januseye.service"

echo "------------------------------------------------"
echo "   JanusEye 2026 - Installation Universelle V2.0.3"
echo "   Système : $(uname -s) / $(uname -m)"
echo "   Utilisateur : $USER_NAME"
echo "------------------------------------------------"

# --- ETAPE 0 : VERIFICATION ESPACE DISQUE ---
FREE_SPACE=$(df -m "$INSTALL_DIR" | awk 'NR==2 {print $4}')
if [ "$FREE_SPACE" -lt 1000 ]; then
    echo "❌ ERREUR : Espace disque insuffisant (besoin ~1Go, libre ${FREE_SPACE}Mo)."
    exit 1
fi

# 1. Structure des dossiers
echo "[1/7] Création des répertoires..."
mkdir -p "$INSTALL_DIR/videos" "$INSTALL_DIR/logs" "$INSTALL_DIR/config" "$INSTALL_DIR/templates"

# 2. Dépendances système
echo "[2/7] Installation des paquets système..."
sudo apt-get update || { echo "❌ Échec APT update"; exit 1; }
# Suppression de 'requests' ici car il est installé via pip plus bas
sudo apt-get install -y python3-venv python3-pip libopencv-dev python3-opencv python3-numpy || { echo "❌ Échec installation paquets"; exit 1; }

# 3. Configuration Matérielle (Spécifique Raspberry Pi)
echo "[3/7] Analyse du matériel..."
REBOOT_REQUIRED=false

if [ -f /proc/device-tree/model ] && grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "📍 Matériel détecté : Raspberry Pi"
    
    CONFIG_FILE="/boot/firmware/config.txt"
    [ ! -f "$CONFIG_FILE" ] && CONFIG_FILE="/boot/config.txt"

    # Détection caméra CSI (Nappe)
    if grep -q "imx219\|ov5647" /proc/device-tree/model 2>/dev/null || (command -v rpicam-hello &>/dev/null && rpicam-hello --list-cameras | grep -q "imx219\|ov5647"); then
        echo "💡 Caméra CSI détectée. Vérification du mode Legacy..."
        if grep -q "camera_auto_detect=1" "$CONFIG_FILE"; then
            echo "🔧 Activation du mode Legacy dans $CONFIG_FILE..."
            sudo sed -i 's/camera_auto_detect=1/camera_auto_detect=0/' "$CONFIG_FILE"
            echo "start_x=1" | sudo tee -a "$CONFIG_FILE" > /dev/null
            echo "gpu_mem=128" | sudo tee -a "$CONFIG_FILE" > /dev/null
            REBOOT_REQUIRED=true
        fi
    fi
else
    echo "💻 Matériel détecté : PC / Generic Linux (Utilisation standard V4L2)"
fi

# 4. Environnement Python (VENV)
echo "[4/7] Configuration de l'environnement Python..."
cd "$INSTALL_DIR"
[ ! -d "venv" ] && python3 -m venv venv
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
# C'est ici que requests est installé
"$INSTALL_DIR/venv/bin/pip" install flask requests numpy opencv-python

# 5. Permissions
echo "[5/7] Réglage des droits..."
[ -f "$INSTALL_DIR/clean_videos.sh" ] && chmod +x "$INSTALL_DIR/clean_videos.sh"
sudo chown -R "$USER_NAME:$USER_NAME" "$INSTALL_DIR"
sudo usermod -a -G video "$USER_NAME"

# 6. Service Systemd
echo "[6/7] Configuration du service..."
cat << EOF > januseye.service.tmp
[Unit]
Description=Serveur de Surveillance JanusEye
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo mv januseye.service.tmp /etc/systemd/system/$SERVICE_NAME

# 7. Lancement
echo "[7/7] Activation du service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "------------------------------------------------"
if [ "$REBOOT_REQUIRED" = true ]; then
    echo " ⚠️  ATTENTION : Mode Legacy activé pour la caméra Raspberry Pi."
    echo " Un REDÉMARRAGE est OBLIGATOIRE : sudo reboot"
else
    echo " ✅ INSTALLATION TERMINÉE AVEC SUCCÈS !"
fi
echo " Accès : http://$(hostname -I | awk '{print $1}'):5000"
echo "------------------------------------------------"
