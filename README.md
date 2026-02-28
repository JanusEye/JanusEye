========================================================== 
JANUSEYE - MONITORING SYSTEM 
“QUIET & INTELLIGENT” 
Version 2026
==========================================================

CONCEPT:
JanusEye is a silent alarm by video detection. Unlike
with classic alarms, it does not emit any sound but alerts you
instantly by SMS and Email with visual proof.

STRENGTHS:
- DISCRETION: Capture high-resolution photos during movement 
so as not to saturate the Raspberry Pi processor and save 
storage space.
- TOTAL AUTOMATION: Monitoring is activated automatically 
when the last occupant leaves the premises and deactivates as soon as 
the arrival of an authorized smartphone. No possible forgetting.
- ENHANCED SECURITY: Self-defense system blocking the IP address 
after 3 unsuccessful PIN attempts.

ARCHIVE CONTENT:
- app.py: The main Flask server.
- install_januseye.sh: Complete system installation script.
- clean_videos.sh: Automatic cleaning (30 day retention).
- templates/: Modern and secure Web interface.
- config/: Settings files and presence management.

INSTALLATION:
1. Copy the JanusEye folder to your Raspberry Pi (/home/user/),
Replace "user" with your username on Raspberry PI.
2. In a terminal, make the script executable: 
chmod +x install_januseye.sh
3. Start the installation: 
./install_januseye.sh

USE:
- Access: http://address_ip_du_pi:5000 (PIN code: 1234)
- Silence mode: In the event of intrusion, photos are stored in 
the Gallery and sent by Email.
- Presence Management: The system intelligently manages departure and 
the arrival of occupants to avoid false alarms.

⚖️ Legal warning and proper use

The use of a video protection system is subject to a framework
strict regulatory (GDPR and Internal Security Code): 

Private setting: 
The camera must be installed exclusively for surveillance of 
your private property (interior, garden, garage). 
Public Space: 
It is strictly forbidden to film on public roads (streets, 
sidewalk) or neighboring properties. 
Image rights: 
If you employ home staff or receive guests, 
you must inform them of the presence of the system. 
Data retention: 
Images should not be kept for more than 30 days, unless 
in the event of legal proceedings.

--------------------------------------------------------------
JanusEye 2026: Security that is forgotten.
