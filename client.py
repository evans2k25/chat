import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


client.connect((HOST, PORT))


def recevoir_messages():
    """Reçoit les messages du serveur."""

    while True:

        try:

            message = client.recv(4096).decode("utf-8")

            if not message:
                break

            print(f"\n{message}")
            print("Vous : ", end="", flush=True)

        except:

            break


# ==========================================================
# INTERFACE
# ==========================================================

print("=" * 55)
print("                  CHAT LOCAL")
print("=" * 55)


# Le serveur demande le pseudo
message = client.recv(1024).decode("utf-8")

print(message, end="")

pseudo = input()

client.send(pseudo.encode("utf-8"))


# Message de bienvenue
message = client.recv(1024).decode("utf-8")

print(message)


# Thread de réception
thread = threading.Thread(
    target=recevoir_messages,
    daemon=True
)

thread.start()


print("Vous pouvez maintenant discuter.")
print("Tapez 'exit' pour quitter.\n")


# ==========================================================
# ENVOI DES MESSAGES
# ==========================================================

while True:

    try:

        message = input("Vous : ")

        client.send(
            message.encode("utf-8")
        )

        if message.lower() == "exit":
            break

    except:

        break


client.close()

print("Déconnecté du serveur.")