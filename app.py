import cv2
import configparser
import os
import time
import numpy as np
import smtplib
import requests
import shutil
import subprocess
from threading import Thread, Lock
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from flask import send_file
from flask import Flask, render_template, Response, request, redirect, session, send_from_directory, url_for

app = Flask(__name__)
app.secret_key = 'JanusEye_2026_Final_V107'

# --- CONFIGURATION ---
BASE_DIR = '/home/papy/JanusEye'
CONF_PATH = f'{BASE_DIR}/config/januseye.conf'
VIDEO_DIR = f'{BASE_DIR}/videos'
LOG_FILE = f'{BASE_DIR}/logs/januseye.log'
PRESENCE_FILE = f'{BASE_DIR}/config/presence.txt'

# --- ÉTAT GLOBAL ---
alarm_armed = True
global_frame = None
is_recording = False
last_email_time = 0 
last_sms_time = 0
login_attempts = {} 
lock = Lock()
last_param_change = 0

def get_conf():
    c = configparser.ConfigParser()
    if os.path.exists(CONF_PATH):
        c.read(CONF_PATH)
    for s in ['SECRET', 'DEVICES', 'EMAIL', 'EVENTS', 'FREE_SMS', 'CAMERA', 'STORAGE']:
        if s not in c: c[s] = {}
    return c

def get_real_ip():
    try:
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0]
        return request.remote_addr
    except:
        return "127.0.0.1"

def log_event(message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] JanusEye: {message}\n")

def auto_clean():
    try:
        conf = get_conf()
        # On récupère le réglage 'retention_days' (30 par défaut)
        days = conf['STORAGE'].get('retention_days', '30')
        # On trouve le chemin du script clean_videos.sh dans le même dossier que app.py
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean_videos.sh")
        
        if os.path.exists(script_path):
            subprocess.Popen(['/bin/bash', script_path, str(days)])
            log_event(f"SYSTEME : Lancement du nettoyage automatique ({days} jours).")
    except Exception as e:
        log_event(f"ERREUR Nettoyage : {str(e)}")

def get_service_status():
    try:
        # Vérifie si le service januseye est actif
        status = subprocess.check_output(['systemctl', 'is-active', 'januseye.service'], stderr=subprocess.STDOUT).decode().strip()
        return "Actif" if status == "active" else "Inactif"
    except:
        return "Non installé"

# --- FONCTIONS ALERTES ---

def send_free_sms(message):
    conf = get_conf()
    user = conf['FREE_SMS'].get('user_id')
    api_key = conf['FREE_SMS'].get('api_key')
    cam_name = conf['CAMERA'].get('name', 'JanusEye_Cam')
    if not user or not api_key: return
    
    full_message = f"[{cam_name}] {message}"
    msg_url = full_message.replace(" ", "%20")
    url = f"https://smsapi.free-mobile.fr/sendmsg?user={user}&pass={api_key}&msg={msg_url}"
    
    for tentative in range(3):
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                log_event(f"SMS ENVOYE : {full_message}")
                return True
        except: pass
        time.sleep(2)
    return False

def send_mail_async(paths, info_ip, subject_suffix="ALERTE", action_desc="Détection"):
    conf = get_conf()
    cam_name = conf['CAMERA'].get('name', 'JanusEye_Cam')
    try:
        msg = MIMEMultipart()
        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        msg['Subject'] = f"{cam_name} : {subject_suffix} - {now}"
        msg['From'] = conf['EMAIL'].get('sender_email')
        msg['To'] = conf['EMAIL'].get('receiver_email')
        
        body = f"--- RAPPORT {cam_name.upper()} ---\n"
        body += f"Heure      : {now}\n"
        body += f"Action     : {action_desc}\n"
        body += f"IP Source  : {info_ip}\n"
        body += f"------------------------"
        
        msg.attach(MIMEText(body, 'plain'))
        for path in paths:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
                    msg.attach(img)
        with smtplib.SMTP(conf['EMAIL'].get('smtp_server', 'smtp.gmail.com'), int(conf['EMAIL'].get('smtp_port', 587))) as server:
            server.starttls()
            server.login(conf['EMAIL'].get('sender_email'), conf['EMAIL'].get('sender_password'))
            server.send_message(msg)
            log_event(f"EMAIL : Message '{subject_suffix}' envoye pour {cam_name}.")
    except Exception as e:
        log_event(f"ERREUR EMAIL : {str(e)}")

# --- GESTION PRÉSENCE ---

def load_presence():
    if os.path.exists(PRESENCE_FILE):
        try:
            with open(PRESENCE_FILE, 'r') as f:
                data = f.read().strip().lower()
                return set(n.strip() for n in data.split(",") if n.strip())
        except: return set()
    return set()

def save_presence(presence_set):
    with open(PRESENCE_FILE, 'w') as f:
        f.write(", ".join(list(presence_set)))

def draw_timestamp_with_bg(frame):
    h, w, _ = frame.shape
    conf = get_conf()
    cam_name = conf['CAMERA'].get('name', 'JanusEye_Cam')
    ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness_outline = 3
    thickness_text = 1 
    
    pos_time = (15, h - 20)
    (name_w, _), _ = cv2.getTextSize(cam_name, font, scale, thickness_text)
    pos_name = (w - name_w - 15, h - 20)

    cv2.putText(frame, ts, pos_time, font, scale, (0, 0, 0), thickness_outline, cv2.LINE_AA)
    cv2.putText(frame, ts, pos_time, font, scale, (255, 255, 255), thickness_text, cv2.LINE_AA)
    cv2.putText(frame, cam_name, pos_name, font, scale, (0, 0, 0), thickness_outline, cv2.LINE_AA)
    cv2.putText(frame, cam_name, pos_name, font, scale, (255, 255, 255), thickness_text, cv2.LINE_AA)

    return frame

def gen_frames():
    global global_frame
    while True:
        with lock:
            if global_frame is None:
                img = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(img, "Initialisation Camera...", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                _, buffer = cv2.imencode('.jpg', img)
            else:
                _, buffer = cv2.imencode('.jpg', global_frame)
        
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.04)

def camera_worker():
    global global_frame, alarm_armed, is_recording, last_email_time, last_sms_time, last_param_change
    cap = None
    last_gray = None
    current_res = ""
    motion_timer = 0
    mail_paths = []

    while True:
        if alarm_armed:
            conf = get_conf()
            target_res = conf['CAMERA'].get('size', '640x480')

            if cap is not None and target_res != current_res:
                log_event(f"CAM : Changement resolution vers {target_res}")
                cap.release()
                cap = None
                last_param_change = time.time() 
                time.sleep(1)

            if cap is None or not cap.isOpened():
                cap = cv2.VideoCapture(0)
                current_res = target_res
                try:
                    w, h = map(int, current_res.split('x'))
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
                except:
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                time.sleep(1)
                continue

            success, frame = cap.read()
            if not success: continue

            bright = int(conf['CAMERA'].get('brightness', 0))
            if bright != 0:
                frame = cv2.convertScaleAbs(frame, alpha=1, beta=bright)

            rot_val = conf['CAMERA'].get('rotation', '180')
            if rot_val == '90': frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif rot_val == '180': frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif rot_val == '270': frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            if (time.time() - last_param_change) < 5:
                small_temp = cv2.resize(frame, (320, 240))
                last_gray = cv2.cvtColor(small_temp, cv2.COLOR_BGR2GRAY)
                last_gray = cv2.GaussianBlur(last_gray, (21, 21), 0)
                with lock:
                    global_frame = draw_timestamp_with_bg(frame.copy())
                continue

            # --- ANALYSE MOUVEMENT AVEC CADRES ---
            small = cv2.resize(frame, (320, 240))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            motion_boxes = []
            if last_gray is not None and last_gray.shape == gray.shape:
                delta = cv2.absdiff(last_gray, gray)
                thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                
                sens = int(conf['CAMERA'].get('sensitivity', 5000))
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                movement_in_frame = False
                for c in contours:
                    if cv2.contourArea(c) > (sens / 5): # Seuil de déclenchement par contour
                        movement_in_frame = True
                        (x, y, w_b, h_b) = cv2.boundingRect(c)
                        # Redimensionnement des cadres pour l'image haute résolution
                        r_w = frame.shape[1] / 320
                        r_h = frame.shape[0] / 240
                        motion_boxes.append((int(x*r_w), int(y*r_h), int(w_b*r_w), int(h_b*r_h)))

                if movement_in_frame:
                    motion_timer = 10
                    if not is_recording:
                        is_recording = True
                        mail_paths = []
                        log_event("MOUVEMENT : Debut de l'enregistrement.")
                        if conf['EVENTS'].getboolean('sms_motion', False):
                            if (time.time() - last_sms_time) > 60:
                                h_now = datetime.now().strftime("%H:%M:%S")
                                Thread(target=send_free_sms, args=(f"Mouvement detecte a {h_now}",), daemon=True).start()
                                last_sms_time = time.time()


                if motion_timer > 0:
                    motion_timer -= 1
                    if motion_timer % 2 == 0:
                        f_save = draw_timestamp_with_bg(frame.copy())
                        for (bx, by, bw, bh) in motion_boxes:
                            cv2.rectangle(f_save, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
                        fname = f"Photo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-4]}.jpg"
                        p = os.path.join(VIDEO_DIR, fname)
                        cv2.imwrite(p, f_save)
                        if len(mail_paths) < 5: mail_paths.append(p)
                elif is_recording:
                    is_recording = False
                    log_event("FIN DE MOUVEMENT.")
                    if mail_paths and (time.time() - last_email_time) > 60:
                        Thread(target=send_mail_async, args=(list(mail_paths), "Detection Interne", "ALERTE MOUVEMENT", "Mouvement"), daemon=True).start()
                        last_email_time = time.time()

            last_gray = gray
            with lock:
                global_frame = draw_timestamp_with_bg(frame.copy())
                # Dessin des cadres de mouvement sur le flux direct
                for (bx, by, bw, bh) in motion_boxes:
                    cv2.rectangle(global_frame, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
                if is_recording:
                    cv2.rectangle(global_frame, (2,2), (global_frame.shape[1]-2, global_frame.shape[0]-2), (0,0,255), 2)
            time.sleep(0.01)
        else:
            if cap: cap.release(); cap = None
            with lock: global_frame = None
            is_recording = False; time.sleep(1)

Thread(target=camera_worker, daemon=True).start()

# --- ROUTES ---

@app.route('/')
def index():
    if not session.get('logged_in'): return redirect("./login")
    conf = get_conf(); presence = load_presence()
    pres_status = {name: ("Présent" if name.lower() in presence else "Absent") for name in conf['DEVICES'].values()}
    logs_list = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f.readlines()[-20:]:
                line = line.strip()
                color = "#aaaaaa" # Gris par défaut
                
                # --- LOGIQUE DE COLORATION MODIFIÉE ---
                if "DESACTIVE par" in line:
                    color = "#4dff4d" # VERT ÉCLATANT pour la désactivation
                elif any(x in line for x in ["ACTIVE par", "MOUVEMENT : Debut", "Blocage", "SECURITE"]):
                    color = "#ff4d4d" # ROUGE pour l'armement et les alertes
                elif "SMS ENVOYE" in line:
                    color = "#ffff00" # JAUNE
                elif "EMAIL" in line:
                    color = "#00d9ff" # BLEU
                
                logs_list.append({'text': line, 'color': color})
            logs_list.reverse()
    return render_template('index.html', status="ACTIVÉE" if alarm_armed else "DÉSACTIVÉE", logs=logs_list, armed=alarm_armed, presence_status=pres_status, recording=is_recording)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global login_attempts
    ip = get_real_ip()
    conf = get_conf()
    if ip not in login_attempts: login_attempts[ip] = 0
    if request.method == 'POST':
        if login_attempts[ip] >= 3:
            return render_template('login.html', error="Compte bloqué (3 échecs). Redémarrez le service.")
        pin_saisi = request.form.get('pin')
        pin_correct = conf['SECRET'].get('web_pin', '1234')
        if pin_saisi == pin_correct:
            session['logged_in'] = True
            login_attempts[ip] = 0
            log_event(f"LOGIN : Succès (IP: {ip})")
            return redirect("./")
        else:
            login_attempts[ip] += 1
            log_event(f"SECURITE : Echec PIN {login_attempts[ip]}/3 (IP: {ip})")
            if login_attempts[ip] == 3:
                log_event(f"SECURITE : Blocage définitif de l'IP {ip}")
                if conf['EVENTS'].getboolean('sms_on_block', False):
                    Thread(target=send_free_sms, args=(f"Blocage IP {ip} (3 echecs PIN)",), daemon=True).start()
                if conf['EVENTS'].getboolean('mail_security', False):
                    Thread(target=send_mail_async, args=([], ip, "ALERTE SECURITE", "Blocage IP définitif (3 tentatives)"), daemon=True).start()
            return render_template('login.html', error=f"Incorrect ({login_attempts[ip]}/3)")
    return render_template('login.html')

@app.route('/arm')
def arm_webhook():
    global alarm_armed, is_recording, last_email_time, last_sms_time
    conf = get_conf(); action = request.args.get('action')
    device = request.args.get('device', 'Manuel').replace('iPhone_', '').capitalize()
    presence = load_presence(); ip = get_real_ip()
    if action == 'off':
        presence.add(device.lower())
        log_event(f"PRESENCE : Entree de {device} (IP: {ip})") 
        if alarm_armed:
            alarm_armed = False; msg = f"DESACTIVE par {device}"
            log_event(f"{msg} - IP: {ip}")
            if conf['EVENTS'].getboolean('sms_toggle', False): Thread(target=send_free_sms, args=(msg,), daemon=True).start()
            if conf['EVENTS'].getboolean('mail_toggle', False): Thread(target=send_mail_async, args=([], ip, "ETAT ALARME", f"DESACTIVE par {device}"), daemon=True).start()
    elif action == 'on':
        presence.discard(device.lower())
        log_event(f"PRESENCE : Sortie de {device} (IP: {ip})")
        if not presence and not alarm_armed:
            alarm_armed = True; msg = f"ACTIVE par {device}"
            log_event(f"{msg} - IP: {ip}")
            # Lancement du nettoyage automatique à l'activation
            auto_clean()
            if conf['EVENTS'].getboolean('sms_toggle', False): Thread(target=send_free_sms, args=(msg,), daemon=True).start()
            if conf['EVENTS'].getboolean('mail_toggle', False): Thread(target=send_mail_async, args=([], ip, "ETAT ALARME", f"ACTIVE par {device}"), daemon=True).start()
    save_presence(presence)
    if request.args.get('source') == 'web': return redirect("./")
    return "OK"

@app.route('/galerie')
def galerie():
    if not session.get('logged_in'): return redirect("./login")
    if not os.path.exists(VIDEO_DIR): os.makedirs(VIDEO_DIR)
    files = sorted([f for f in os.listdir(VIDEO_DIR) if f.lower().endswith('.jpg')], reverse=True)
    return render_template('galerie.html', files=files)

@app.route('/get_video/<path:filename>')
def serve_video(filename):
    if not session.get('logged_in'): return redirect("./login")
    return send_from_directory(VIDEO_DIR, filename)

@app.route('/download/<filename>')
def download_file(filename):
    if not session.get('logged_in'): return redirect("./login")
    file_path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return f"Erreur : Le fichier est introuvable", 404

@app.route('/delete_image/<filename>')
def delete_image(filename):
    if not session.get('logged_in'): return redirect("./login")
    path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(path):
        try: os.remove(path)
        except: pass
    return redirect("../galerie")

@app.route('/clear_gallery')
def clear_gallery():
    if not session.get('logged_in'): return redirect("./login")
    import glob
    files = glob.glob(os.path.join(VIDEO_DIR, "*.jpg"))
    for f in files:
        try: os.remove(f)
        except: pass
    log_event("GALERIE : Toutes les images ont été supprimées.")
    return redirect("./galerie")

@app.route('/settings')
def settings():
    if not session.get('logged_in'): return redirect("./login")
    total, used, free = shutil.disk_usage("/")
    disk_info = {
        'total': round(total / (2**30), 1),
        'used': round(used / (2**30), 1),
        'free': round(free / (2**30), 1),
        'percent': round((used / total) * 100, 1)
    }
    banned_list = [ip for ip, count in login_attempts.items() if count >= 3]

    service_status = "Inactif"
    try:
        status = subprocess.check_output(['systemctl', 'is-active', 'januseye.service'], stderr=subprocess.STDOUT).decode().strip()
        if status == "active": service_status = "Actif"
    except:
        service_status = "Non installé"

    return render_template('settings.html', config=get_conf(), devices=get_conf()['DEVICES'], banned_ips=banned_list, disk=disk_info, service_status=service_status)

@app.route('/restart_service')
def restart_service():
    if not session.get('logged_in'): return redirect("./login")
    log_event("SYSTEME : Redémarrage du service (RAZ des blocages IP).")
    def perform_restart():
        time.sleep(2)
        os.system('sudo systemctl restart januseye.service')
    Thread(target=perform_restart).start()
    return redirect("./")

@app.route('/save_settings', methods=['POST'])
def save_settings():
    if not session.get('logged_in'): return redirect("./login")
    conf = get_conf()
    if 'CAMERA' not in conf: conf['CAMERA'] = {}
    if 'STORAGE' not in conf: conf['STORAGE'] = {}

    conf['CAMERA']['name'] = request.form.get('camera_name', 'JanusEye_Cam')
    conf['SECRET']['web_pin'] = request.form.get('web_pin', '1234')
    conf['STORAGE']['retention_days'] = request.form.get('retention_days', '30')
    conf['FREE_SMS']['user_id'] = request.form.get('free_user', '')
    conf['FREE_SMS']['api_key'] = request.form.get('free_pass', '')
    conf['EVENTS']['sms_motion'] = 'true' if request.form.get('sms_motion') else 'false'
    conf['EVENTS']['sms_toggle'] = 'true' if request.form.get('sms_toggle') else 'false'
    conf['EVENTS']['sms_on_block'] = 'true' if request.form.get('sms_on_block') else 'false'
    conf['EMAIL']['smtp_server'] = request.form.get('smtp_serv', 'smtp.gmail.com')
    conf['EMAIL']['smtp_port'] = request.form.get('smtp_port', '587')
    conf['EMAIL']['sender_email'] = request.form.get('mail_user', '')
    conf['EMAIL']['sender_password'] = request.form.get('mail_pass', '')
    conf['EMAIL']['receiver_email'] = request.form.get('mail_recv', '')
    conf['EVENTS']['mail_motion'] = 'true' if request.form.get('mail_motion') else 'false'
    conf['EVENTS']['mail_toggle'] = 'true' if request.form.get('mail_toggle') else 'false'
    conf['EVENTS']['mail_security'] = 'true' if request.form.get('mail_security') else 'false'
    
    conf.remove_section('DEVICES'); conf.add_section('DEVICES')
    for i, name in enumerate(request.form.getlist('device_name[]')):
        if name.strip(): conf['DEVICES'][f'dev_{i}'] = name.strip()
        
    with open(CONF_PATH, 'w') as f: conf.write(f)
    return redirect("./")

@app.route('/video_feed')
def video_feed():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if not alarm_armed: return "Caméra désactivée"
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame', headers={'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache'})

@app.route('/clear_logs')
def clear_logs():
    if not session.get('logged_in'): return redirect("./login")
    with open(LOG_FILE, 'w') as f: f.write("")
    return redirect("./")

@app.route('/logout')
def logout(): session.clear(); return redirect("./login")

@app.route('/test_sms')
def test_sms():
    if not session.get('logged_in'): return redirect("./login")
    send_free_sms("Test de communication reussi.")
    return redirect("./settings")

@app.route('/test_mail')
def test_mail():
    if not session.get('logged_in'): return redirect("./login")
    ip = get_real_ip()
    Thread(target=send_mail_async, args=([], ip, "TEST CONNEXION", "Ceci est un email de test de JanusEye."), daemon=True).start()
    return redirect("./settings")

@app.route('/update_cam')
def update_cam():
    global last_param_change
    if not session.get('logged_in'): return "Unauthorized", 401
    param = request.args.get('param')
    value = request.args.get('value')
    conf = get_conf()
    if 'CAMERA' not in conf: conf['CAMERA'] = {}
    conf['CAMERA'][param] = value
    with open(CONF_PATH, 'w') as f: conf.write(f)
    last_param_change = time.time()
    log_event(f"CAM : Modification {param} -> {value}")
    return "OK"

if __name__ == '__main__':
    auto_clean()
    app.run(host='0.0.0.0', port=5000, threaded=True)
