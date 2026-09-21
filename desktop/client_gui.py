from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox, simpledialog

import socketio
import ttkbootstrap as ttk

SERVER_URL = os.getenv("CHAT_SERVER_URL", "http://127.0.0.1:5000")


class ChatClient:
    def __init__(self, root: ttk.Window) -> None:
        self.root = root
        self.root.title("Chat Local")
        self.root.geometry("700x500")
        self.nickname = ""
        self.connected = False
        self.socket = socketio.Client(reconnection=True)

        self.messages = tk.Text(root, state="disabled", wrap="word")
        self.messages.pack(fill="both", expand=True, padx=12, pady=12)
        bottom = ttk.Frame(root)
        bottom.pack(fill="x", padx=12, pady=(0, 12))
        self.entry = ttk.Entry(bottom)
        self.entry.pack(side="left", fill="x", expand=True)
        ttk.Button(bottom, text="Envoyer", command=self.send).pack(side="right", padx=(8, 0))
        self.entry.bind("<Return>", lambda _: self.send())
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.socket.on("nouveau_message", self.on_message)
        self.socket.on("message_systeme", self.on_system)
        self.socket.on("connect", self.on_connect)
        self.socket.on("disconnect", self.on_disconnect)
        self.join()

    def append(self, text: str) -> None:
        self.messages.configure(state="normal")
        self.messages.insert("end", text + "\n")
        self.messages.see("end")
        self.messages.configure(state="disabled")

    def join(self) -> None:
        nickname = simpledialog.askstring("Connexion", "Votre pseudo :", parent=self.root)
        if not nickname or not nickname.strip():
            self.root.destroy()
            return
        self.nickname = nickname.strip()[:30]
        try:
            self.socket.connect(SERVER_URL, transports=["polling", "websocket"])
        except Exception as exc:
            messagebox.showerror("Connexion impossible", str(exc), parent=self.root)

    def on_connect(self) -> None:
        self.connected = True
        self.socket.emit("connexion", {"pseudo": self.nickname})

    def on_disconnect(self) -> None:
        self.connected = False

    def on_message(self, data: dict) -> None:
        self.root.after(0, lambda: self.append(f"{data.get('pseudo', 'Utilisateur')} [{data.get('heure', '')}] : {data.get('message', '')}"))

    def on_system(self, data: dict) -> None:
        self.root.after(0, lambda: self.append(f"— {data.get('message', '')} [{data.get('heure', '')}]"))

    def send(self) -> None:
        message = self.entry.get().strip()
        if message and self.connected:
            self.socket.emit("message", {"message": message[:2000]})
            self.entry.delete(0, "end")

    def close(self) -> None:
        if self.socket.connected:
            self.socket.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    window = ttk.Window(themename="darkly")
    ChatClient(window)
    window.mainloop()
