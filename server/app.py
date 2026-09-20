from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime
import os


# ============================================================
# CHEMINS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WEB_DIR = os.path.join(
    BASE_DIR,
    "web_chat"
)

TEMPLATE_DIR = os.path.join(
    WEB_DIR,
    "templates"
)

STATIC_DIR = os.path.join(
    WEB_DIR,
    "static"
)


# ============================================================
# FLASK
# ============================================================

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)

app.config["SECRET_KEY"] = "chat-local-secret"


# ============================================================
# SOCKET.IO
# ============================================================

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


# ============================================================
# UTILISATEURS
# ============================================================

utilisateurs = {}


# ============================================================
# PAGE WEB
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# CONNEXION
# ============================================================

@socketio.on("connexion")
def connexion(data):

    if not isinstance(data, dict):
        return

    pseudo = str(
        data.get("pseudo", "")
    ).strip()

    if not pseudo:
        pseudo = "Utilisateur"

    pseudo = pseudo[:30]

    utilisateurs[request.sid] = pseudo

    print(
        f"[+] {pseudo} connecté"
    )

    socketio.emit(
        "message_systeme",
        {
            "message": f"{pseudo} a rejoint le chat.",
            "heure": heure_actuelle()
        }
    )

    envoyer_liste_utilisateurs()


# ============================================================
# MESSAGE
# ============================================================

@socketio.on("message")
def recevoir_message(data):

    if not isinstance(data, dict):
        return

    message = str(
        data.get("message", "")
    ).strip()

    if not message:
        return

    message = message[:2000]

    pseudo = utilisateurs.get(
        request.sid,
        "Utilisateur"
    )

    print(
        f"[MESSAGE] {pseudo} : {message}"
    )

    socketio.emit(
        "nouveau_message",
        {
            "pseudo": pseudo,
            "message": message,
            "heure": heure_actuelle(),
            "sid": request.sid
        }
    )


# ============================================================
# DÉCONNEXION
# ============================================================

@socketio.on("disconnect")
def deconnexion():

    pseudo = utilisateurs.pop(
        request.sid,
        None
    )

    if pseudo is None:
        return

    print(
        f"[-] {pseudo} déconnecté"
    )

    socketio.emit(
        "message_systeme",
        {
            "message": f"{pseudo} a quitté le chat.",
            "heure": heure_actuelle()
        }
    )

    envoyer_liste_utilisateurs()


# ============================================================
# LISTE UTILISATEURS
# ============================================================

def envoyer_liste_utilisateurs():

    liste = list(
        utilisateurs.values()
    )

    socketio.emit(
        "liste_utilisateurs",
        liste
    )

    print(
        f"[UTILISATEURS] "
        f"{len(liste)} connecté(s)"
    )


# ============================================================
# HEURE
# ============================================================

def heure_actuelle():

    return datetime.now().strftime("%H:%M")


# ============================================================
# DÉMARRAGE
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("                 CHAT LOCAL SERVER")
    print("=" * 60)

    print("PC      : http://127.0.0.1:5000")
    print("Réseau  : http://192.168.1.5:5000")

    print("=" * 60)
    print("Serveur en attente...")
    print()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )