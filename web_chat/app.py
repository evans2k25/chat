from server.app import app, socketio

__all__ = ["app", "socketio"]

if __name__ == "__main__":
    import os

    socketio.run(
        app,
        host=os.getenv("CHAT_HOST", "0.0.0.0"),
        port=int(os.getenv("CHAT_PORT", "5000")),
        debug=False,
    )
