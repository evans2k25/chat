from flask import Flask, render_template, request
from flask_socketio import SocketIO
from datetime import datetime


# ============================================================
# CONFIGURATION FLASK
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "chat-local-secret"

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


# ============================================================
# UTILISATEURS CONNECTÉS
# ============================================================

utilisateurs = {}


# ============================================================
# PAGE PRINCIPALE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# CONNEXION D'UN UTILISATEUR
# ============================================================

@socketio.on("connexion")
def connexion(data):

    if not isinstance(data, dict):
        return

    pseudo = str(data.get("pseudo", "")).strip()

    if not pseudo:
        pseudo = "Utilisateur"

    # Limite du pseudo
    pseudo = pseudo[:30]

    # request.sid = identifiant unique de la connexion Socket.IO
    utilisateurs[request.sid] = pseudo

    print(
        f"[+] {pseudo} connecté "
        f"(ID : {request.sid})"
    )

    # Informer tous les utilisateurs
    socketio.emit(
        "message_systeme",
        {
            "message": f"{pseudo} a rejoint le chat.",
            "heure": heure_actuelle()
        }
    )

    # Mettre à jour la liste
    envoyer_liste_utilisateurs()


# ============================================================
# RÉCEPTION D'UN MESSAGE
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

    # Limite du message
    message = message[:2000]

    # Récupérer le pseudo grâce au SID
    pseudo = utilisateurs.get(
        request.sid,
        "Utilisateur"
    )

    heure = heure_actuelle()

    print(
        f"[MESSAGE] {pseudo} : {message}"
    )

    # Envoyer à tous les utilisateurs
    socketio.emit(
        "nouveau_message",
        {
            "pseudo": pseudo,
            "message": message,
            "heure": heure,
            "sid": request.sid
        }
    )


# ============================================================
# DÉCONNEXION
# ============================================================

@socketio.on("disconnect")
def utilisateur_deconnecte():

    pseudo = utilisateurs.pop(
        request.sid,
        None
    )

    if pseudo is None:
        return

    print(
        f"[-] {pseudo} déconnecté "
        f"(ID : {request.sid})"
    )

    # Informer les autres utilisateurs
    socketio.emit(
        "message_systeme",
        {
            "message": f"{pseudo} a quitté le chat.",
            "heure": heure_actuelle()
        }
    )

    # Actualiser la liste
    envoyer_liste_utilisateurs()


# ============================================================
# ENVOYER LA LISTE DES UTILISATEURS
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
# DÉMARRAGE DU SERVEUR
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("                 CHAT LOCAL WEB")
    print("=" * 60)

    print(
        "Serveur local : "
        "http://127.0.0.1:5000"
    )

    print(
        "Réseau local  : "
        "http://192.168.1.5:5000"
    )

    print("=" * 60)
    print("En attente des utilisateurs...")
    print()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )