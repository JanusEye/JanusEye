🇫🇷 VERSION FRANÇAISE

====================================================
** 🛡️ JANUSEYE — SYSTÈME DE SURVEILLANCE "SILENCIEUX & INTELLIGENT" **
** Version v.2.0.3 (Mars 2026) **

💡 CONCEPT
JanusEye est une sentinelle vidéo intelligente pour Raspberry Pi et PC
Linux. Contrairement aux alarmes bruyantes, il agit avec discrétion en
vous alertant instantanément par Notifications (NTFY), SMS et Email
avec preuves visuelles à l'appui.

✨ POINTS FORTS (V2.0.3)

    TRIPLE ALERTE : Notifications Push (NTFY) avec photo, SMS (Free
    Mobile) et Email complet.

    COMPATIBILITÉ UNIVERSELLE : Nouveau script d'installation détectant
    automatiquement votre matériel (PC ou Raspberry Pi) et configurant
    le Mode Legacy pour les caméras CSI (nappes).

    DISCRÉTION & PERF : Capture HD 720p asynchrone (Multi-threading)
    pour ne jamais ralentir le flux, même sur un Pi Zero.

    SÉCURITÉ IP : Protection contre les intrusions de l'interface :
    blocage automatique de l'adresse IP après 3 codes PIN erronés
    (stockage en mémoire vive pour plus de sécurité).

    GESTION DE PRÉSENCE : Activation/Désactivation automatique basée
    sur la détection de votre smartphone.

    STOCKAGE OPTIMISÉ : Installation complète ultra-légère (< 5.3 Go)
    pour préserver vos cartes SD.

📦 CONTENU DE L'ARCHIVE

    app.py : Le cœur du système (Serveur Flask).

    install_januseye.sh : Script d'installation universel et intelligent.

    uninstall_januseye.sh : Script de désinstallation propre.

    backup_januseye.sh : Sauvegarde de vos réglages et certificats.

    clean_videos.sh : Gestion automatique de l'espace disque.

    logs/ : Dossier contenant les journaux système (januseye.log).

    videos/ : Dossier de stockage des captures d'alertes.

    templates/ : banned.html, galerie.html, index.html, login.html,
    settings.html.

    config/ : settings.json, presence.txt.

🛠️ INSTALLATION & MISE À JOUR

    Transférer : Copiez le dossier JanusEye dans votre répertoire
    personnel (ex: /home/pi/).

    Autoriser : chmod +x ~/JanusEye/install_januseye.sh

    Lancer : sudo ~/JanusEye/install_januseye.sh

    Note : Si le script active le mode caméra Legacy, un redémarrage
    (sudo reboot) sera nécessaire.

🗑️ DÉSINSTALLATION
Pour retirer le service et nettoyer le système :
chmod +x ~/JanusEye/uninstall_januseye.sh && ./~/JanusEye/uninstall_januseye.sh


🇺🇸 ENGLISH VERSION

====================================================
** 🛡️ JANUSEYE — "QUIET & INTELLIGENT" MONITORING SYSTEM **
** Version v.2.0.3 (March 2026) **

💡 CONCEPT
JanusEye is a smart video sentinel for Raspberry Pi and Linux PCs.
Unlike noisy alarms, it acts discreetly by instantly alerting you via
Notifications (NTFY), SMS, and Email with visual evidence.

✨ STRENGTHS (V2.0.3)

    TRIPLE ALERT: Push Notifications (NTFY) with photo, SMS (Free
    Mobile), and detailed Email.

    UNIVERSAL COMPATIBILITY: New installation script that auto-detects
    hardware (PC or Raspberry Pi) and configures Legacy Mode for CSI
    (ribbon) cameras.

    DISCRETION & PERF: Asynchronous 720p HD capture (Multi-threading)
    to ensure smooth streaming even on a Pi Zero.

    IP SECURITY: Interface intrusion protection: automatic IP address
    blocking after 3 incorrect PIN attempts (stored in RAM for extra
    security).

    PRESENCE MANAGEMENT: Automatic Arm/Disarm based on smartphone
    detection.

    OPTIMIZED STORAGE: Ultra-light full install (< 5.3 GB) to extend
    SD card lifespan.

📦 ARCHIVE CONTENT

    app.py: Main Flask server (Core).

    install_januseye.sh: Universal and smart installation script.

    uninstall_januseye.sh: Clean uninstallation script.

    backup_januseye.sh: Backup of settings and certificates.

    clean_videos.sh: Automatic disk space management.

    logs/: Directory for system logs (januseye.log).

    videos/: Storage directory for alert captures.

    templates/: banned.html, galerie.html, index.html, login.html,
    settings.html.

    config/: settings.json, presence.txt.

🛠️ INSTALLATION & UPDATE

    Transfer: Copy the JanusEye folder to your home directory
    (e.g., /home/pi/).

    Authorize: chmod +x ~/JanusEye/install_januseye.sh

    Launch: sudo ~/JanusEye/install_januseye.sh

    Note: If the script enables Legacy Camera Mode, a reboot
    (sudo reboot) will be required.

🗑️ UNINSTALLATION
To remove the service and clean the system:
chmod +x ~/JanusEye/uninstall_januseye.sh && ./~/JanusEye/uninstall_januseye.sh


⚖️ AVERTISSEMENT / LEGAL WARNING

    FR : Ne filmez que votre propriété privée. Il est interdit de
    filmer la voie publique ou les voisins (RGPD).

    EN: Only monitor your private property. Filming public roads
    or neighbors is strictly prohibited (GDPR).

JanusEye 2026 : La sécurité qui se fait oublier / Security that is forgotten.

