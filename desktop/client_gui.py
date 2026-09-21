from __future__ import annotations

import os

from server.app import app, socketio


if __name__ == "__main__":
    host = os.getenv("CHAT_HOST", "0.0.0.0")
    port = int(os.getenv("CHAT_PORT", "5000"))
    socketio.run(app, host=host, port=port, debug=False)
