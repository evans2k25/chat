import socket
import threading


HOST = "192.168.1.5"
PORT = 5000

clients = {}
lock = threading.Lock()


def envoyer_a_tous(message, client_expediteur=None):
    """Envoie un message à tous les clients connectés."""

    with lock:
        clients_copies = list(clients.items())

    for client, pseudo in clients_copies:

        if client == client_expediteur:
            continue

        try:
            client.send(message.encode("utf-8"))

        except:
            retirer_client(client)


def retirer_client(client):
    """Retire un client du serveur."""

    with lock:

        if client in clients:
            pseudo = clients[client]
            del clients[client]

        else:
            return

    try:
        client.close()
    except:
        pass

    print(f"[-] {pseudo} s'est déconnecté")

    envoyer_a_tous(
        f"🔴 {pseudo} a quitté le chat."
    )


def gerer_client(client, adresse):
    """Gère un utilisateur."""

    try:

        # Demander le pseudo
        client.send(
            "Entrez votre pseudo : ".encode("utf-8")
        )

        pseudo = client.recv(1024).decode("utf-8").strip()

        if not pseudo:
            pseudo = f"Utilisateur-{adresse[1]}"

        # Enregistrer le client
        with lock:
            clients[client] = pseudo

        print(f"[+] {pseudo} connecté depuis {adresse}")

        client.send(
            f"Bienvenue {pseudo} !\n".encode("utf-8")
        )

        envoyer_a_tous(
            f"🟢 {pseudo} vient de rejoindre le chat.",
            client
        )

        # Boucle de réception
        while True:

            message = client.recv(1024).decode("utf-8")

            if not message:
                break

            message = message.strip()

            if message.lower() == "exit":
                break

            print(f"{pseudo} : {message}")

            envoyer_a_tous(
                f"{pseudo} : {message}",
                client
            )

    except Exception as e:

        print(f"Erreur avec {adresse} : {e}")

    finally:

        retirer_client(client)


# ==========================================================
# SERVEUR
# ==========================================================

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))

server.listen()

print("=" * 55)
print("                  CHAT LOCAL")
print("=" * 55)
print(f"Serveur démarré sur le port {PORT}")
print("En attente des utilisateurs...\n")


while True:

    client, adresse = server.accept()

    thread = threading.Thread(
        target=gerer_client,
        args=(client, adresse),
        daemon=True
    )

    thread.start()

    with lock:
        nombre_clients = len(clients)

    print(
        f"Nombre d'utilisateurs connectés : "
        f"{nombre_clients}"
    )