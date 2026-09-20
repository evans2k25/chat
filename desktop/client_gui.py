import socketio
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


# ============================================================
# CONFIGURATION
# ============================================================

SERVER_URL = "http://192.168.1.5:5000"


# ============================================================
# SOCKET.IO
# ============================================================

sio = socketio.Client(
    reconnection=True,
    reconnection_attempts=10,
    reconnection_delay=1,
    reconnection_delay_max=5
)


# ============================================================
# VARIABLES
# ============================================================

pseudo = ""
connecte = False


# ============================================================
# PALETTE
# ============================================================

COLORS = {

    "background": "#080C16",
    "sidebar": "#0D1320",
    "sidebar_hover": "#151E30",

    "panel": "#101827",
    "panel_light": "#151F31",

    "primary": "#6366F1",
    "primary_dark": "#4F46E5",
    "accent": "#8B5CF6",

    "text": "#F8FAFC",
    "text_secondary": "#A7B0C0",
    "text_muted": "#667085",

    "success": "#22C55E",
    "danger": "#EF4444",
    "warning": "#F59E0B",

    "border": "#1E293B",

    "message_me": "#4F46E5",
    "message_other": "#182235",

}


# ============================================================
# FENÊTRE PRINCIPALE
# ============================================================

app = ttk.Window(
    title="ChatLocal",
    themename="darkly",
    size=(1200, 750),
    minsize=(900, 600),
    resizable=(True, True)
)

app.configure(
    background=COLORS["background"]
)


# ============================================================
# STYLE GLOBAL
# ============================================================

style = ttk.Style()


style.configure(
    "Main.TFrame",
    background=COLORS["background"]
)


style.configure(
    "Sidebar.TFrame",
    background=COLORS["sidebar"]
)


style.configure(
    "Panel.TFrame",
    background=COLORS["panel"]
)


style.configure(
    "Title.TLabel",
    background=COLORS["background"],
    foreground=COLORS["text"],
    font=("Segoe UI", 19, "bold")
)


style.configure(
    "Muted.TLabel",
    background=COLORS["background"],
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 9)
)


style.configure(
    "SidebarTitle.TLabel",
    background=COLORS["sidebar"],
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 9, "bold")
)


# ============================================================
# HEADER GLOBAL
# ============================================================

header = ttk.Frame(
    app,
    style="Main.TFrame",
    padding=(24, 18)
)

header.pack(
    fill=X
)


# ============================================================
# LOGO
# ============================================================

logo_container = ttk.Frame(
    header,
    style="Main.TFrame"
)

logo_container.pack(
    side=LEFT
)


logo = ttk.Label(
    logo_container,
    text="●",
    foreground=COLORS["primary"],
    background=COLORS["background"],
    font=("Segoe UI", 26, "bold")
)

logo.pack(
    side=LEFT,
    padx=(0, 10)
)


titre_zone = ttk.Frame(
    logo_container,
    style="Main.TFrame"
)

titre_zone.pack(
    side=LEFT
)


ttk.Label(
    titre_zone,
    text="ChatLocal",
    style="Title.TLabel"
).pack(
    anchor=W
)


ttk.Label(
    titre_zone,
    text="Messagerie privée • Réseau local",
    style="Muted.TLabel"
).pack(
    anchor=W
)


# ============================================================
# STATUT GLOBAL
# ============================================================

statut_container = ttk.Frame(
    header,
    style="Main.TFrame"
)

statut_container.pack(
    side=RIGHT
)


statut = ttk.Label(
    statut_container,
    text="● Déconnecté",
    foreground=COLORS["danger"],
    background=COLORS["background"],
    font=("Segoe UI", 10, "bold")
)

statut.pack(
    side=LEFT,
    padx=(0, 20)
)


# ============================================================
# CONTENU PRINCIPAL
# ============================================================

conteneur = ttk.Frame(
    app,
    style="Main.TFrame"
)

conteneur.pack(
    fill=BOTH,
    expand=True,
    padx=20,
    pady=(0, 20)
)


# ============================================================
# SIDEBAR
# ============================================================

sidebar = ttk.Frame(
    conteneur,
    width=300,
    style="Sidebar.TFrame"
)

sidebar.pack(
    side=LEFT,
    fill=Y,
    padx=(0, 15)
)

sidebar.pack_propagate(False)


# ============================================================
# PROFIL
# ============================================================

profil = ttk.Frame(
    sidebar,
    style="Sidebar.TFrame",
    padding=18
)

profil.pack(
    fill=X
)


avatar = ttk.Label(
    profil,
    text="?",
    anchor=CENTER,
    foreground="white",
    background=COLORS["primary"],
    font=("Segoe UI", 15, "bold")
)

avatar.place(
    x=0,
    y=0,
    width=48,
    height=48
)


profil_infos = ttk.Frame(
    profil,
    style="Sidebar.TFrame"
)

profil_infos.pack(
    side=LEFT,
    padx=(58, 0)
)


profil_nom = ttk.Label(
    profil_infos,
    text="Non connecté",
    background=COLORS["sidebar"],
    foreground=COLORS["text"],
    font=("Segoe UI", 11, "bold")
)

profil_nom.pack(
    anchor=W
)


profil_status = ttk.Label(
    profil_infos,
    text="Hors ligne",
    background=COLORS["sidebar"],
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 9)
)

profil_status.pack(
    anchor=W,
    pady=(2, 0)
)


# ============================================================
# SÉPARATEUR
# ============================================================

ttk.Separator(
    sidebar
).pack(
    fill=X,
    padx=18,
    pady=5
)


# ============================================================
# TITRE UTILISATEURS
# ============================================================

users_header = ttk.Frame(
    sidebar,
    style="Sidebar.TFrame",
    padding=(18, 12)
)

users_header.pack(
    fill=X
)


ttk.Label(
    users_header,
    text="UTILISATEURS",
    style="SidebarTitle.TLabel"
).pack(
    side=LEFT
)


users_badge = ttk.Label(
    users_header,
    text="0",
    foreground="white",
    background=COLORS["primary"],
    font=("Segoe UI", 8, "bold"),
    padding=(8, 3)
)

users_badge.pack(
    side=RIGHT
)


# ============================================================
# RECHERCHE
# ============================================================

search_frame = ttk.Frame(
    sidebar,
    style="Sidebar.TFrame"
)

search_frame.pack(
    fill=X,
    padx=15,
    pady=(0, 10)
)


search_entry = ttk.Entry(
    search_frame,
    font=("Segoe UI", 9)
)

search_entry.pack(
    fill=X,
    ipady=6
)


# ============================================================
# LISTE UTILISATEURS
# ============================================================

liste_utilisateurs = ttk.Treeview(
    sidebar,
    columns=("pseudo",),
    show="tree",
    selectmode="browse"
)

liste_utilisateurs.column(
    "#0",
    width=48,
    stretch=False
)

liste_utilisateurs.pack(
    fill=BOTH,
    expand=True,
    padx=12,
    pady=(0, 12)
)


# ============================================================
# CHAT
# ============================================================

zone_chat = ttk.Frame(
    conteneur,
    style="Panel.TFrame"
)

zone_chat.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)


# ============================================================
# HEADER CHAT
# ============================================================

chat_header = ttk.Frame(
    zone_chat,
    style="Panel.TFrame",
    padding=(22, 16)
)

chat_header.pack(
    fill=X
)


chat_avatar = ttk.Label(
    chat_header,
    text="👥",
    anchor=CENTER,
    background=COLORS["primary"],
    foreground="white",
    font=("Segoe UI Emoji", 18)
)

chat_avatar.pack(
    side=LEFT,
    padx=(0, 12),
    ipadx=9,
    ipady=8
)


chat_infos = ttk.Frame(
    chat_header,
    style="Panel.TFrame"
)

chat_infos.pack(
    side=LEFT
)


ttk.Label(
    chat_infos,
    text="Discussion générale",
    background=COLORS["panel"],
    foreground=COLORS["text"],
    font=("Segoe UI", 14, "bold")
).pack(
    anchor=W
)


chat_statut = ttk.Label(
    chat_infos,
    text="● Hors ligne",
    background=COLORS["panel"],
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 9)
)

chat_statut.pack(
    anchor=W,
    pady=(2, 0)
)


# ============================================================
# ACTIONS CHAT
# ============================================================

actions = ttk.Frame(
    chat_header,
    style="Panel.TFrame"
)

actions.pack(
    side=RIGHT
)


bouton_info = ttk.Button(
    actions,
    text="ⓘ",
    bootstyle="secondary",
    width=3
)

bouton_info.pack(
    side=RIGHT,
    padx=(5, 0)
)


# ============================================================
# SÉPARATEUR
# ============================================================

ttk.Separator(
    zone_chat
).pack(
    fill=X
)


# ============================================================
# ZONE MESSAGES
# ============================================================

messages_frame = ttk.Frame(
    zone_chat,
    style="Panel.TFrame"
)

messages_frame.pack(
    fill=BOTH,
    expand=True
)


messages = ttk.Text(
    messages_frame,
    wrap="word",
    state="disabled",

    background=COLORS["background"],
    foreground=COLORS["text"],

    insertbackground="white",

    relief="flat",
    borderwidth=0,

    font=("Segoe UI", 10),

    padx=25,
    pady=20
)

messages.pack(
    fill=BOTH,
    expand=True
)


# ============================================================
# TAGS
# ============================================================

messages.tag_configure(
    "system",
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 9, "italic"),
    justify="center"
)


messages.tag_configure(
    "author_me",
    foreground="#A5B4FC",
    font=("Segoe UI", 9, "bold")
)


messages.tag_configure(
    "author_other",
    foreground="#C4B5FD",
    font=("Segoe UI", 9, "bold")
)


messages.tag_configure(
    "body",
    foreground=COLORS["text"],
    font=("Segoe UI", 10)
)


messages.tag_configure(
    "time",
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 8)
)


# ============================================================
# COMPOSER
# ============================================================

composer_zone = ttk.Frame(
    zone_chat,
    style="Panel.TFrame",
    padding=(18, 10, 18, 18)
)

composer_zone.pack(
    fill=X
)


composer = ttk.Frame(
    composer_zone,
    style="Panel.TFrame"
)

composer.pack(
    fill=X
)


# ============================================================
# EMOJI
# ============================================================

bouton_emoji = ttk.Button(
    composer,
    text="😊",
    bootstyle="secondary",
    width=3
)

bouton_emoji.pack(
    side=LEFT,
    padx=(0, 8)
)


# ============================================================
# CHAMP
# ============================================================

champ_message = ttk.Entry(
    composer,
    font=("Segoe UI", 11)
)

champ_message.pack(
    side=LEFT,
    fill=X,
    expand=True,
    ipady=9
)


# ============================================================
# ENVOYER
# ============================================================

bouton_envoyer = ttk.Button(
    composer,
    text="Envoyer  ➤",
    bootstyle="primary",
    command=lambda: envoyer_message()
)

bouton_envoyer.pack(
    side=RIGHT,
    padx=(8, 0),
    ipady=4
)


# ============================================================
# INDICATION
# ============================================================

ttk.Label(
    composer_zone,
    text="Entrée pour envoyer  •  Communication sur réseau local",
    background=COLORS["panel"],
    foreground=COLORS["text_muted"],
    font=("Segoe UI", 8)
).pack(
    anchor=E,
    pady=(6, 0)
)


# ============================================================
# AFFICHAGE MESSAGE
# ============================================================

def afficher_message(
    texte,
    tag=None
):

    messages.configure(
        state="normal"
    )

    messages.insert(
        "end",
        texte + "\n",
        tag
    )

    messages.see(
        "end"
    )

    messages.configure(
        state="disabled"
    )


# ============================================================
# MESSAGE AVEC STYLE
# ============================================================

def afficher_bulle(
    nom,
    message,
    heure,
    est_moi=False
):

    messages.configure(
        state="normal"
    )

    messages.insert(
        "end",
        "\n"
    )

    if est_moi:

        messages.insert(
            "end",
            f"Vous  •  {heure}\n",
            "author_me"
        )

    else:

        messages.insert(
            "end",
            f"{nom}  •  {heure}\n",
            "author_other"
        )

    messages.insert(
        "end",
        f"  {message}\n",
        "body"
    )

    messages.insert(
        "end",
        "\n"
    )

    messages.see(
        "end"
    )

    messages.configure(
        state="disabled"
    )


# ============================================================
# ENVOYER MESSAGE
# ============================================================

def envoyer_message():

    message = champ_message.get().strip()

    if not message:

        return

    if not connecte:

        messagebox.showwarning(
            "ChatLocal",
            "Vous n'êtes pas connecté au serveur."
        )

        return

    try:

        sio.emit(
            "message",
            {
                "message": message
            }
        )

        champ_message.delete(
            0,
            "end"
        )

        champ_message.focus()

    except Exception as erreur:

        messagebox.showerror(
            "Erreur",
            str(erreur)
        )


# ============================================================
# EMOJI
# ============================================================

def ajouter_emoji():

    emojis = [
        "😀",
        "😂",
        "😍",
        "😎",
        "👍",
        "❤️",
        "🔥",
        "🎉",
        "👏",
        "🙏",
        "🚀",
        "💯"
    ]

    import random

    champ_message.insert(
        "end",
        random.choice(emojis)
    )

    champ_message.focus()


bouton_emoji.configure(
    command=ajouter_emoji
)


# ============================================================
# AVATAR
# ============================================================

def actualiser_profil():

    if pseudo:

        avatar.configure(
            text=pseudo[0].upper()
        )

        profil_nom.configure(
            text=pseudo
        )

    else:

        avatar.configure(
            text="?"
        )

        profil_nom.configure(
            text="Non connecté"
        )


# ============================================================
# FENÊTRE DE CONNEXION
# ============================================================

def demander_pseudo():

    global pseudo

    fenetre = ttk.Toplevel(
        app
    )

    fenetre.title(
        "Connexion à ChatLocal"
    )

    fenetre.geometry(
        "480x350"
    )

    fenetre.resizable(
        False,
        False
    )

    fenetre.configure(
        background=COLORS["background"]
    )

    fenetre.grab_set()

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    ttk.Label(
        fenetre,
        text="●",
        foreground=COLORS["primary"],
        background=COLORS["background"],
        font=("Segoe UI", 42, "bold")
    ).pack(
        pady=(25, 5)
    )

    # --------------------------------------------------------
    # TITRE
    # --------------------------------------------------------

    ttk.Label(
        fenetre,
        text="Bienvenue sur ChatLocal",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=("Segoe UI", 19, "bold")
    ).pack()


    ttk.Label(
        fenetre,
        text="Connectez-vous à votre réseau local",
        background=COLORS["background"],
        foreground=COLORS["text_muted"],
        font=("Segoe UI", 9)
    ).pack(
        pady=(5, 20)
    )


    # --------------------------------------------------------
    # PSEUDO
    # --------------------------------------------------------

    ttk.Label(
        fenetre,
        text="Votre pseudo",
        background=COLORS["background"],
        foreground=COLORS["text_secondary"],
        font=("Segoe UI", 9, "bold")
    ).pack(
        anchor=W,
        padx=55
    )


    champ = ttk.Entry(
        fenetre,
        font=("Segoe UI", 11)
    )

    champ.pack(
        fill=X,
        padx=55,
        pady=(7, 20),
        ipady=8
    )

    champ.focus()


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    def valider():

        global pseudo

        valeur = champ.get().strip()

        if not valeur:

            messagebox.showwarning(
                "Pseudo",
                "Veuillez entrer un pseudo."
            )

            champ.focus()

            return

        pseudo = valeur[:30]

        fenetre.destroy()

        actualiser_profil()

        connecter()


    bouton = ttk.Button(
        fenetre,
        text="Rejoindre le chat  →",
        bootstyle="primary",
        command=valider
    )

    bouton.pack(
        fill=X,
        padx=55,
        ipady=7
    )


    champ.bind(
        "<Return>",
        lambda event: valider()
    )


# ============================================================
# CONNEXION SERVEUR
# ============================================================

def connecter():

    global connecte

    try:

        statut.configure(
            text="● Connexion...",
            foreground=COLORS["warning"]
        )

        chat_statut.configure(
            text="● Connexion au serveur...",
            foreground=COLORS["warning"]
        )

        app.update_idletasks()


        if not sio.connected:

            sio.connect(
                SERVER_URL,
                transports=[
                    "polling",
                    "websocket"
                ]
            )


    except Exception as erreur:

        connecte = False

        statut.configure(
            text="● Déconnecté",
            foreground=COLORS["danger"]
        )

        chat_statut.configure(
            text="● Serveur inaccessible",
            foreground=COLORS["danger"]
        )

        messagebox.showerror(
            "Connexion impossible",
            f"Impossible de joindre le serveur.\n\n"
            f"Serveur : {SERVER_URL}\n\n"
            f"{erreur}"
        )


# ============================================================
# SOCKET.IO CONNECT
# ============================================================

@sio.event
def connect():

    global connecte

    print(
        "[Socket.IO] Connecté au serveur"
    )

    connecte = True


    def actualiser():

        statut.configure(
            text="● Connecté",
            foreground=COLORS["success"]
        )

        profil_status.configure(
            text="● En ligne",
            foreground=COLORS["success"]
        )

        chat_statut.configure(
            text="● En ligne",
            foreground=COLORS["success"]
        )


        if pseudo:

            sio.emit(
                "connexion",
                {
                    "pseudo": pseudo
                }
            )


    app.after(
        0,
        actualiser
    )


# ============================================================
# SOCKET.IO DISCONNECT
# ============================================================

@sio.event
def disconnect():

    global connecte

    connecte = False

    print(
        "[Socket.IO] Déconnecté"
    )


    def actualiser():

        statut.configure(
            text="● Déconnecté",
            foreground=COLORS["danger"]
        )

        profil_status.configure(
            text="Hors ligne",
            foreground=COLORS["danger"]
        )

        chat_statut.configure(
            text="● Serveur déconnecté",
            foreground=COLORS["danger"]
        )


    app.after(
        0,
        actualiser
    )


# ============================================================
# NOUVEAU MESSAGE
# ============================================================

@sio.on("nouveau_message")
def nouveau_message(data):

    nom = data.get(
        "pseudo",
        "Utilisateur"
    )

    message = data.get(
        "message",
        ""
    )

    heure = data.get(
        "heure",
        ""
    )


    est_moi = (
        nom == pseudo
    )


    app.after(
        0,
        lambda: afficher_bulle(
            nom,
            message,
            heure,
            est_moi
        )
    )


# ============================================================
# MESSAGE SYSTÈME
# ============================================================

@sio.on("message_systeme")
def message_systeme(data):

    message = data.get(
        "message",
        ""
    )

    heure = data.get(
        "heure",
        ""
    )


    texte = (
        f"────  {message}  •  {heure}  ────"
    )


    app.after(
        0,
        lambda: afficher_message(
            texte,
            "system"
        )
    )


# ============================================================
# LISTE UTILISATEURS
# ============================================================

@sio.on("liste_utilisateurs")
def liste_utilisateurs(data):

    def actualiser():

        for element in liste_utilisateurs.get_children():

            liste_utilisateurs.delete(
                element
            )


        users_badge.configure(
            text=str(
                len(data)
            )
        )


        for utilisateur in data:

            initiale = (
                utilisateur[0].upper()
                if utilisateur
                else "?"
            )


            liste_utilisateurs.insert(
                "",
                "end",
                text=initiale,
                values=(utilisateur,)
            )


    app.after(
        0,
        actualiser
    )


# ============================================================
# RECHERCHE UTILISATEURS
# ============================================================

def rechercher_utilisateurs(event=None):

    recherche = (
        search_entry
        .get()
        .strip()
        .lower()
    )

    for element in liste_utilisateurs.get_children():

        valeurs = liste_utilisateurs.item(
            element,
            "values"
        )

        if not valeurs:

            continue

        nom = valeurs[0].lower()

        if recherche in nom:

            liste_utilisateurs.reattach(
                element,
                "",
                "end"
            )

        else:

            liste_utilisateurs.detach(
                element
            )


search_entry.bind(
    "<KeyRelease>",
    rechercher_utilisateurs
)


# ============================================================
# ENTRÉE
# ============================================================

champ_message.bind(
    "<Return>",
    lambda event: envoyer_message()
)


# ============================================================
# FERMETURE
# ============================================================

def fermer():

    try:

        if sio.connected:

            sio.disconnect()

    except Exception:
        pass

    app.destroy()


app.protocol(
    "WM_DELETE_WINDOW",
    fermer
)


# ============================================================
# DÉMARRAGE
# ============================================================

demander_pseudo()

app.mainloop()