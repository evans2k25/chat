from __future__ import annotations

import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_socketio import SocketIO


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web_chat")
TEMPLATE_DIR = os.path.join(WEB_DIR, "templates")
STATIC_DIR = os.path.join(WEB_DIR, "static")


def parse_origins(value: str) -> list[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static",
)

app.config["SECRET_KEY"] = os.getenv("CHAT_SECRET_KEY", "dev-change-this-secret")

allowed_origins = parse_origins(
    os.getenv("CHAT_ALLOWED_ORIGINS", "http://localhost:5000,http://127.0.0.1:5000")
)
socketio = SocketIO(app, cors_allowed_origins=allowed_origins)

users: dict[str, str] = {}
used_names: set[str] = set()


def heure_actuelle() -> str:
    return datetime.now().strftime("%H:%M")


def emit_user_list() -> None:
    ordered_users = [users[sid] for sid in sorted(users)]
    socketio.emit("liste_utilisateurs", ordered_users)


def sanitize_pseudo(value: str) -> str:
    pseudo = str(value or "").strip()
    pseudo = pseudo[:30]
    return pseudo


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok", "users": len(users)}, 200


@socketio.on("connexion")
def connexion(data):
    if not isinstance(data, dict):
        socketio.emit(
            "message_systeme",
            {"message": "Données de connexion invalides.", "heure": heure_actuelle()},
            to=request.sid,
        )
        return

    pseudo = sanitize_pseudo(data.get("pseudo", ""))
    if not pseudo:
        socketio.emit(
            "message_systeme",
            {"message": "Pseudo vide. Veuillez saisir un nom valide.", "heure": heure_actuelle()},
            to=request.sid,
        )
        return

    if pseudo in used_names and users.get(request.sid) != pseudo:
        socketio.emit(
            "message_systeme",
            {"message": f"Le pseudo '{pseudo}' est déjà utilisé.", "heure": heure_actuelle()},
            to=request.sid,
        )
        return

    previous = users.get(request.sid)
    if previous and previous in used_names:
        used_names.discard(previous)

    users[request.sid] = pseudo
    used_names.add(pseudo)

    socketio.emit(
        "message_systeme",
        {"message": f"{pseudo} a rejoint le chat.", "heure": heure_actuelle()},
    )
    emit_user_list()


@socketio.on("message")
def recevoir_message(data):
    if not isinstance(data, dict):
        return

    message = str(data.get("message", "")).strip()
    if not message:
        return

    message = message[:2000]
    pseudo = users.get(request.sid, "Utilisateur")

    socketio.emit(
        "nouveau_message",
        {
            "pseudo": pseudo,
            "message": message,
            "heure": heure_actuelle(),
            "sid": request.sid,
        },
    )


@socketio.on("disconnect")
def deconnexion():
    pseudo = users.pop(request.sid, None)
    if pseudo is None:
        return

    used_names.discard(pseudo)
    socketio.emit(
        "message_systeme",
        {"message": f"{pseudo} a quitté le chat.", "heure": heure_actuelle()},
    )
    emit_user_list()


if __name__ == "__main__":
    host = os.getenv("CHAT_HOST", "0.0.0.0")
    port = int(os.getenv("CHAT_PORT", "5000"))

    print("=" * 60)
    print("            CHAT LOCAL SERVER")
    print("=" * 60)
    print(f"Serveur : http://{host}:{port}")
    print("Logiciel prêt pour les connexions Socket.IO")
    print("=" * 60)

    socketio.run(app, host=host, port=port, debug=False)
