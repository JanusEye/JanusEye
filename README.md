🇫🇷 VERSION FRANÇAISE

====================================================
** 🛡️ JANUSEYE - SYSTÈME DE SURVEILLANCE
     "SILENCIEUX & INTELLIGENT" — Version v.1.0.7 **
====================================================

💡 CONCEPT

JanusEye est une alarme silencieuse par détection vidéo. Contrairement
 aux alarmes classiques, il n'émet aucun son strident mais vous alerte
  instantanément par Notifications (NTFY), SMS et Email avec preuves
   visuelles à l'appui.

✨ POINTS FORTS

    TRIPLE ALERTE : Recevez vos alertes selon vos préférences :
        NTFY : Notifications push instantanées avec photo sur votre
        smartphone.
        SMS : Alerte texte rapide (via Free Mobile).
        EMAIL : Rapport complet avec plusieurs clichés de l'intrusion.

    DISCRÉTION : Capture de photos haute résolution lors des mouvements
     pour ne pas saturer le processeur du Raspberry Pi et économiser 
     l'espace de stockage.

    PERFORMANCE HD & ASYNCHRONE : Capture en 720p HD. L'écriture des
    photos est gérée en arrière-plan (Multi-threading) pour ne jamais
    ralentir le flux vidéo.

    TRAÇABILITÉ : Les cadres de détection verts sont "gravés" sur les
    images pour identifier instantanément l'origine du mouvement.

    AUTOMATISATION TOTALE : La surveillance s'active automatiquement
    quand le dernier occupant quitte les lieux et se désactive dès 
    l'arrivée d'un smartphone autorisé. Aucun oubli possible.

    SÉCURITÉ RENFORCÉE : Système d'autodéfense enregistrant et bloquan
     l'ADRESSE IP après 3 tentatives infructueuses du code PIN.

 📦 CONTENU DE L'ARCHIVE

* **app.py** : Le serveur Flask principal (Cœur du système).
* **install_januseye.sh** : Script d'installation système complet.
* **backup_januseye.sh** : Script de sauvegarde de vos réglages et
certificats SSL.
* **clean_videos.sh** : Nettoyage automatique (rétention paramétrable).
* **templates/** : Interface Web moderne, sécurisée et "Responsive".
* **config/** : Fichiers de réglages et gestion intelligente de présence.

---

🛠️ INSTALLATION

1.  **Transférer** : Copiez le dossier `JanusEye` sur votre Raspberry
Pi dans `/home/user/` (remplacez "user" par votre nom d'utilisateur
réel).
2.  **Autoriser** : Dans un terminal, rendez le script exécutable :
    `chmod +x /home/user/JanusEye/install_januseye.sh`
3.  **Lancer** : Démarrez l'installation automatisée :
    `sudo ./install_januseye.sh`

---

📱 UTILISATION

* **Accès Web** : `http://adresse_ip_du_pi:5000` (Code PIN par défaut :
**1234**)
* **Mode Silence** : En cas d'intrusion, les photos sont stockées dans
la Galerie et envoyées par Email/SMS.
* **Gestion Présence** : Le système gère intelligemment le départ et
l'arrivée des occupants pour éviter les fausses alertes.

---

⚖️ AVERTISSEMENT LÉGAL ET BON USAGE

L'utilisation d'un système de vidéoprotection est soumise à un cadre
réglementaire strict (**RGPD** et Code de la sécurité intérieure) :

* **Cadre Privé** : La caméra doit être installée exclusivement pour
la surveillance de votre propriété privée (intérieur, jardin, garage).
* **Espace Public** : Il est strictement interdit de filmer la voie
publique (rue, trottoir) ou les propriétés voisines.
* **Droit à l'image** : Si vous employez du personnel à domicile ou
recevez des invités, vous devez les informer de la présence du système.
* **Conservation des données** : Les images ne doivent pas être
conservées plus de 30 jours, sauf en cas de procédure judiciaire.

---
**JanusEye 2026 : La sécurité qui se fait oublier.**
sécurité qui se fait oublier.


🇺🇸 ENGLISH VERSION

====================================================
** 🛡️ JANUSEYE - "QUIET & INTELLIGENT”
      MONITORING SYSTEM — Version v.1.0.7 **
====================================================

💡 CONCEPT

JanusEye is a silent step-up video alarm. Compared to traditional alarms, it does not emit a shrill sound but alerts you instantly via Notifications (NTFY), SMS and Email with supporting visual evidence.

✨ STRENGTHS

TRIPLE ALERT: Receive your alerts according to your preferences: 
NTFY: Instant push notifications with photo on your 
smartphone. 
SMS: Quick text alert (via Free Mobile). 
EMAIL: Complete report with several photos of the intrusion.

DISCRETION: Capture high-resolution photos while moving 
so as not to saturate the Raspberry Pi processor and save 
storage space.

HD & ASYNCHRONOUS PERFORMANCE: Capture in 720p HD. The writing of
photos is managed in the background (Multi-threading) so that they never
slow down the video stream.

TRACEABILITY: The green detection frames are “engraved” on the
images to instantly identify the origin of the movement.

TOTAL AUTOMATION: Monitoring is activated automatically
when the last occupant leaves the premises and deactivates as soon as
the arrival of an authorized smartphone. No possible forgetting.

REINFORCED SECURITY: Self-defense system recording and blocking 
the IP ADDRESS after 3 unsuccessful PIN attempts.

📦 ARCHIVE CONTENT 

app.py: The main Flask server (Core of the system). 
install_januseye.sh: Complete system installation script. 
backup_januseye.sh: Script for saving your settings and SSL Certificates. 
clean_videos.sh: Automatic cleaning (retentionable... 
templates/: Modern, secure and “Responsive” Web interface. 
config/: Setting files and intelligent management of.

🛠️ INSTALLATION 

Transfer: Copy the JanusEye folder to your Raspberry Pi to /home/user/ (replace "user" with your actual username). 
Authorizer: In a terminal, enable the script: chmod +x /home/user/JanusEye/install_januseye.sh 
Launch: Start the installation: sudo ./install_januseye.sh

📱 USE 

Web access: http://ip_address_of_pi:5000 (Fault code: 1234) 
Silence Mode: In the event of an intrusion, photos are stored in the Gallery and sent by Email/SMS. 
Presence Management: The system intelligently tracks the departure and arrival of occupants to avoid false alarms.

⚖️ LEGAL WARNING AND PROPER USE

The use of a video protection system is subject to strict regulatory requirements (GDPR and Internal Security Code): 

Private Setting: Is the camera installed for surveillance of your private property (interior, garden, garage). 
Public Space: It is prohibited to film public roads (streets, sidewalks) or neighboring properties. 
Image rights: If you employ staff at home or Reentes des, you must inform them of the presence of the system. 
Data retention: Images may not be kept for more than 30 days, except in the event of legal proceedings.

JanusEye 2026: Security that is forgotten. security that is forgotten.
