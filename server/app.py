from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request
from flask_socketio import SocketIO

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web_chat"

app = Flask(
    __name__,
    template_folder=str(WEB_DIR / "templates"),
    static_folder=str(WEB_DIR / "static"),
    static_url_path="/static",
)
app.config["SECRET_KEY"] = os.getenv("CHAT_SECRET_KEY", "dev-only-change-me")


def parse_origins(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


socketio = SocketIO(
    app,
    cors_allowed_origins=parse_origins(
        os.getenv(
            "CHAT_ALLOWED_ORIGINS",
            "http://localhost:5000,http://127.0.0.1:5000",
        )
    ),
)

users: dict[str, str] = {}


def now() -> str:
    return datetime.now().strftime("%H:%M")


def clean_nickname(value: object) -> str:
    return str(value or "").strip()[:30]


def emit_users() -> None:
    socketio.emit("liste_utilisateurs", list(users.values()))


def system_message(message: str, sid: str | None = None) -> None:
    payload = {"message": message, "heure": now()}
    if sid is None:
        socketio.emit("message_systeme", payload)
    else:
        socketio.emit("message_systeme", payload, to=sid)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok", "users": len(users)}


@socketio.on("connexion")
def connect_user(data):
    if not isinstance(data, dict):
        system_message("Données de connexion invalides.", request.sid)
        return

    nickname = clean_nickname(data.get("pseudo"))
    if not nickname:
        system_message("Veuillez saisir un pseudo valide.", request.sid)
        return

    existing_sid = next(
        (sid for sid, name in users.items() if name.casefold() == nickname.casefold()),
        None,
    )
    if existing_sid is not None and existing_sid != request.sid:
        system_message("Ce pseudo est déjà utilisé.", request.sid)
        return

    previous = users.get(request.sid)
    users[request.sid] = nickname
    if previous is None:
        system_message(f"{nickname} a rejoint le chat.")
    emit_users()


@socketio.on("message")
def receive_message(data):
    if not isinstance(data, dict):
        return

    message = str(data.get("message") or "").strip()[:2000]
    nickname = users.get(request.sid)
    if not message or nickname is None:
        return

    socketio.emit(
        "nouveau_message",
        {"pseudo": nickname, "message": message, "heure": now(), "sid": request.sid},
    )


@socketio.on("disconnect")
def disconnect_user():
    nickname = users.pop(request.sid, None)
    if nickname is None:
        return
    system_message(f"{nickname} a quitté le chat.")
    emit_users()


if __name__ == "__main__":
    host = os.getenv("CHAT_HOST", "0.0.0.0")
    port = int(os.getenv("CHAT_PORT", "5000"))
    socketio.run(app, host=host, port=port, debug=False)
