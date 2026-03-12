** 🛡️ JANUSEYE - SYSTÈME DE SURVEILLANCE
     "SILENCIEUX & INTELLIGENT" — Version v.1.0.4 **

💡 CONCEPT

JanusEye est une alarme silencieuse par détection vidéo. Contrairement aux alarmes classiques, il n'émet aucun son 
strident mais vous alerte instantanément par Notifications (NTFY), SMS et Email avec preuves visuelles à l'appui.

✨ POINTS FORTS

    TRIPLE ALERTE : Recevez vos alertes selon vos préférences :
        NTFY : Notifications push instantanées avec photo sur votre smartphone.
        SMS : Alerte texte rapide (via Free Mobile).
        EMAIL : Rapport complet avec plusieurs clichés de l'intrusion.

    DISCRÉTION : Capture de photos haute résolution lors des mouvements pour ne pas saturer le processeur du Raspberry
    Pi et économiser l'espace de stockage.

    AUTOMATISATION TOTALE : La surveillance s'active automatiquement quand le dernier occupant quitte les lieux et se
    désactive dès l'arrivée d'un smartphone autorisé. Aucun oubli possible.

    SÉCURITÉ RENFORCÉE : Système d'autodéfense enregistrant et bloquant l'ADRESSE IP après 3 tentatives infructueuses
    du code PIN.

 📦 CONTENU DE L'ARCHIVE

* **app.py** : Le serveur Flask principal (Cœur du système).
* **install_januseye.sh** : Script d'installation système complet.
* **backup_januseye.sh** : Script de sauvegarde de vos réglages et certificats SSL.
* **clean_videos.sh** : Nettoyage automatique (rétention paramétrable).
* **templates/** : Interface Web moderne, sécurisée et "Responsive".
* **config/** : Fichiers de réglages et gestion intelligente de présence.

---

🛠️ INSTALLATION

1.  **Transférer** : Copiez le dossier `JanusEye` sur votre Raspberry Pi dans `/home/user/` (remplacez "user" par votre nom d'utilisateur réel).
2.  **Autoriser** : Dans un terminal, rendez le script exécutable :
    `chmod +x /home/user/JanusEye/install_januseye.sh`
3.  **Lancer** : Démarrez l'installation automatisée :
    `sudo ./install_januseye.sh`

---

📱 UTILISATION

* **Accès Web** : `http://adresse_ip_du_pi:5000` (Code PIN par défaut : **1234**)
* **Mode Silence** : En cas d'intrusion, les photos sont stockées dans la Galerie et envoyées par Email/SMS.
* **Gestion Présence** : Le système gère intelligemment le départ et l'arrivée des occupants pour éviter les fausses alertes.

---

⚖️ AVERTISSEMENT LÉGAL ET BON USAGE

L'utilisation d'un système de vidéoprotection est soumise à un cadre réglementaire strict (**RGPD** et Code de la sécurité intérieure) :

* **Cadre Privé** : La caméra doit être installée exclusivement pour la surveillance de votre propriété privée (intérieur, jardin, garage).
* **Espace Public** : Il est strictement interdit de filmer la voie publique (rue, trottoir) ou les propriétés voisines.
* **Droit à l'image** : Si vous employez du personnel à domicile ou recevez des invités, vous devez les informer de la présence du système.
* **Conservation des données** : Les images ne doivent pas être conservées plus de 30 jours, sauf en cas de procédure judiciaire.

---
**JanusEye 2026 : La sécurité qui se fait oublier.**
