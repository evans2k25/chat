
// ============================================================
// CHATLOCAL - chat.js
// ============================================================

"use strict";

// ============================================================
// SOCKET.IO
// ============================================================
//
// IMPORTANT :
// On force le transport HTTP polling pour éviter les erreurs
// "xhr post error" / "transport error" sur le réseau local.
//
// Le serveur reste accessible via :
// http://192.168.1.5:5000
//
// ============================================================

const socket = io(window.location.origin, {

    // Transport stable sur réseau local
    transports: ["polling"],

    // Empêche Socket.IO de tenter une mise à niveau WebSocket
    upgrade: false,

    // Reconnexion automatique
    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,

    // Délai maximal de connexion
    timeout: 10000

});


// ============================================================
// ÉTAT DE L'APPLICATION
// ============================================================

let pseudo = "";
let messageCount = 0;
let historiqueCharge = false;


// ============================================================
// ÉLÉMENTS DOM
// ============================================================

const connectionStatus =
    document.getElementById("connectionStatus");

const themeToggle =
    document.getElementById("themeToggle");

const infoButton =
    document.getElementById("infoButton");

const statusDot =
    document.getElementById("statusDot");

const statusTitle =
    document.getElementById("statusTitle");

const statusText =
    document.getElementById("statusText");

const userCount =
    document.getElementById("userCount");

const networkText =
    document.getElementById("networkText");

const messageCountElement =
    document.getElementById("messageCount");

const onlineCount =
    document.getElementById("onlineCount");

const userSearch =
    document.getElementById("userSearch");

const userList =
    document.getElementById("userList");

const clearChatButton =
    document.getElementById("clearChatButton");

const chatStatus =
    document.getElementById("chatStatus");

const messagesContainer =
    document.getElementById("messages");

const typingIndicator =
    document.getElementById("typingIndicator");

const emojiButton =
    document.getElementById("emojiButton");

const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const pseudoModal =
    document.getElementById("pseudoModal");

const pseudoInput =
    document.getElementById("pseudoInput");

const joinButton =
    document.getElementById("joinButton");

const infoModal =
    document.getElementById("infoModal");

const closeInfoButton =
    document.getElementById("closeInfoButton");


// ============================================================
// INITIALISATION
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    chargerTheme();

    mettreAJourEtatConnexion(false);

    if (pseudoInput) {
        pseudoInput.focus();
    }

});


// ============================================================
// SOCKET.IO : CONNEXION
// ============================================================

socket.on("connect", () => {

    console.log(
        "ChatLocal connecté."
    );

    console.log(
        "SID :",
        socket.id
    );

    console.log(
        "Transport :",
        socket.io.engine?.transport?.name || "inconnu"
    );

    console.log(
        "Serveur :",
        window.location.origin
    );


    mettreAJourEtatConnexion(true);


    /*
     * Après une reconnexion Socket.IO,
     * le serveur possède un nouveau SID.
     *
     * On doit donc réidentifier l'utilisateur.
     */

    if (pseudo) {

        socket.emit(
            "connexion",
            {
                pseudo: pseudo
            }
        );

        historiqueCharge = false;

        demanderHistorique();

    }

});


// ============================================================
// SOCKET.IO : DÉCONNEXION
// ============================================================

socket.on("disconnect", (reason) => {

    console.log(
        "ChatLocal déconnecté :",
        reason
    );

    mettreAJourEtatConnexion(false);

});


// ============================================================
// SOCKET.IO : ERREUR DE CONNEXION
// ============================================================

socket.on("connect_error", (error) => {

    console.error(
        "=================================================="
    );

    console.error(
        "ERREUR SOCKET.IO"
    );

    console.error(
        "=================================================="
    );

    console.error(
        "Message :",
        error.message
    );

    console.error(
        "Erreur complète :",
        error
    );

    console.error(
        "Transport utilisé :",
        socket.io.engine?.transport?.name || "inconnu"
    );

    console.error(
        "URL du serveur :",
        window.location.origin
    );


    mettreAJourEtatConnexion(false);


    connectionStatus.textContent =
        "Serveur inaccessible";

    statusDot.classList.remove(
        "online"
    );

    statusDot.classList.add(
        "offline"
    );

    statusTitle.textContent =
        "Hors ligne";

    statusText.textContent =
        "Impossible de joindre le serveur";

    networkText.textContent =
        "Hors ligne";

    chatStatus.textContent =
        "Connexion impossible";

});


// ============================================================
// REJOINDRE LE CHAT
// ============================================================

joinButton.addEventListener(
    "click",
    rejoindreChat
);


pseudoInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {

            event.preventDefault();

            rejoindreChat();

        }

    }
);


function rejoindreChat() {

    const valeur =
        pseudoInput.value.trim();


    // --------------------------------------------------------
    // Vérification du pseudo
    // --------------------------------------------------------

    if (!valeur) {

        afficherErreurPseudo();

        return;

    }


    // --------------------------------------------------------
    // Limitation à 30 caractères
    // --------------------------------------------------------

    pseudo =
        valeur.substring(0, 30);


    // --------------------------------------------------------
    // Fermer la fenêtre
    // --------------------------------------------------------

    pseudoModal.classList.add(
        "hidden"
    );


    chatStatus.textContent =
        "Connexion en cours...";


    // --------------------------------------------------------
    // Connexion au serveur
    // --------------------------------------------------------

    if (socket.connected) {

        socket.emit(
            "connexion",
            {
                pseudo: pseudo
            }
        );

        historiqueCharge = false;

        demanderHistorique();

    } else {

        chatStatus.textContent =
            "Connexion au serveur...";

    }


    messageInput.focus();

}


// ============================================================
// ERREUR PSEUDO
// ============================================================

function afficherErreurPseudo() {

    pseudoInput.classList.add(
        "input-error"
    );


    setTimeout(() => {

        pseudoInput.classList.remove(
            "input-error"
        );

    }, 500);


    pseudoInput.focus();

}


// ============================================================
// DEMANDER L'HISTORIQUE
// ============================================================

function demanderHistorique() {

    if (!socket.connected) {
        return;
    }

    socket.emit(
        "demander_historique"
    );

}


// ============================================================
// RÉCEPTION DE L'HISTORIQUE
// ============================================================

socket.on(
    "historique_messages",
    (messages) => {

        if (!Array.isArray(messages)) {
            return;
        }


        /*
         * Évite de charger deux fois
         * le même historique.
         */

        if (historiqueCharge) {
            return;
        }


        historiqueCharge = true;


        // ----------------------------------------------------
        // Nettoyage
        // ----------------------------------------------------

        messagesContainer.innerHTML = "";

        messageCount = 0;


        // ----------------------------------------------------
        // Affichage
        // ----------------------------------------------------

        messages.forEach((message) => {

            afficherMessage(
                message.pseudo,
                message.message,
                message.heure,
                message.pseudo === pseudo
            );

            messageCount++;

        });


        mettreAJourCompteurMessages();


        // ----------------------------------------------------
        // Aucun message
        // ----------------------------------------------------

        if (messages.length === 0) {

            afficherBienvenue();

        }


        faireDefilerVersBas();

    }
);


// ============================================================
// RÉCEPTION D'UN NOUVEAU MESSAGE
// ============================================================

socket.on(
    "nouveau_message",
    (data) => {

        if (!data) {
            return;
        }


        // Si le message de bienvenue est affiché,
        // on le retire.

        const welcome =
            messagesContainer.querySelector(
                ".welcome-message"
            );

        if (welcome) {
            welcome.remove();
        }


        afficherMessage(
            data.pseudo,
            data.message,
            data.heure,
            data.pseudo === pseudo
        );


        messageCount++;


        mettreAJourCompteurMessages();


        faireDefilerVersBas();

    }
);


// ============================================================
// MESSAGE SYSTÈME
// ============================================================

socket.on(
    "message_systeme",
    (data) => {

        if (!data) {
            return;
        }


        afficherMessageSysteme(
            data.message,
            data.heure
        );

    }
);


// ============================================================
// LISTE DES UTILISATEURS
// ============================================================

socket.on(
    "liste_utilisateurs",
    (utilisateurs) => {

        if (!Array.isArray(utilisateurs)) {
            return;
        }


        afficherUtilisateurs(
            utilisateurs
        );

    }
);


// ============================================================
// AFFICHER UN MESSAGE
// ============================================================

function afficherMessage(
    auteur,
    contenu,
    heure,
    estMoi = false
) {

    const messageElement =
        document.createElement("div");


    messageElement.className =
        estMoi
            ? "message message-me"
            : "message message-other";


    // --------------------------------------------------------
    // AVATAR
    // --------------------------------------------------------

    const avatar =
        document.createElement("div");

    avatar.className =
        "message-avatar";

    avatar.textContent =
        obtenirInitiales(auteur);


    // --------------------------------------------------------
    // CONTENU
    // --------------------------------------------------------

    const content =
        document.createElement("div");

    content.className =
        "message-content";


    // --------------------------------------------------------
    // AUTEUR
    // --------------------------------------------------------

    const author =
        document.createElement("div");

    author.className =
        "message-author";

    author.textContent =
        estMoi
            ? "Vous"
            : auteur;


    // --------------------------------------------------------
    // BULLE
    // --------------------------------------------------------

    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble";


    /*
     * textContent au lieu de innerHTML :
     * protège l'application contre l'injection HTML.
     */

    bubble.textContent =
        contenu;


    // --------------------------------------------------------
    // HEURE
    // --------------------------------------------------------

    const time =
        document.createElement("span");

    time.className =
        "message-time";

    time.textContent =
        heure || "";


    // --------------------------------------------------------
    // CONSTRUCTION
    // --------------------------------------------------------

    content.appendChild(
        author
    );

    content.appendChild(
        bubble
    );

    content.appendChild(
        time
    );


    messageElement.appendChild(
        avatar
    );

    messageElement.appendChild(
        content
    );


    messagesContainer.appendChild(
        messageElement
    );

}


// ============================================================
// MESSAGE SYSTÈME
// ============================================================

function afficherMessageSysteme(
    contenu,
    heure
) {

    const element =
        document.createElement("div");

    element.className =
        "system-message";


    const text =
        document.createElement("span");

    text.textContent =
        contenu;


    const time =
        document.createElement("small");

    time.textContent =
        heure || "";


    element.appendChild(
        text
    );

    element.appendChild(
        time
    );


    messagesContainer.appendChild(
        element
    );


    faireDefilerVersBas();

}


// ============================================================
// MESSAGE DE BIENVENUE
// ============================================================

function afficherBienvenue() {

    messagesContainer.innerHTML = `

        <div class="welcome-message">

            <div class="welcome-icon">
                ✦
            </div>

            <h3>
                Bienvenue sur ChatLocal
            </h3>

            <p>
                Aucun message pour le moment.
                Soyez le premier à écrire !
            </p>

        </div>

    `;

}


// ============================================================
// UTILISATEURS
// ============================================================

function afficherUtilisateurs(
    utilisateurs
) {

    userList.innerHTML = "";


    const nombre =
        utilisateurs.length;


    // --------------------------------------------------------
    // Compteurs
    // --------------------------------------------------------

    userCount.textContent =
        nombre;

    onlineCount.textContent =
        `${nombre} ${
            nombre > 1
                ? "utilisateurs"
                : "utilisateur"
        } en ligne`;


    // --------------------------------------------------------
    // Aucun utilisateur
    // --------------------------------------------------------

    if (nombre === 0) {

        userList.innerHTML = `

            <div class="empty-state">
                Aucun utilisateur connecté.
            </div>

        `;

        return;

    }


    // --------------------------------------------------------
    // Liste
    // --------------------------------------------------------

    utilisateurs.forEach(
        (nom) => {

            const userElement =
                document.createElement("div");

            userElement.className =
                "user-item";


            userElement.dataset.name =
                nom.toLowerCase();


            // ------------------------------------------------
            // Avatar
            // ------------------------------------------------

            const avatar =
                document.createElement("div");

            avatar.className =
                "user-avatar";

            avatar.textContent =
                obtenirInitiales(nom);


            // ------------------------------------------------
            // Informations
            // ------------------------------------------------

            const info =
                document.createElement("div");

            info.className =
                "user-info";


            const name =
                document.createElement("strong");

            name.textContent =
                nom === pseudo
                    ? `${nom} (Vous)`
                    : nom;


            const status =
                document.createElement("span");

            status.textContent =
                "En ligne";


            // ------------------------------------------------
            // Indicateur
            // ------------------------------------------------

            const dot =
                document.createElement("span");

            dot.className =
                "user-online-dot";


            // ------------------------------------------------
            // Construction
            // ------------------------------------------------

            info.appendChild(
                name
            );

            info.appendChild(
                status
            );


            userElement.appendChild(
                avatar
            );

            userElement.appendChild(
                info
            );

            userElement.appendChild(
                dot
            );


            userList.appendChild(
                userElement
            );

        }
    );

}


// ============================================================
// RECHERCHE DES UTILISATEURS
// ============================================================

userSearch.addEventListener(
    "input",
    () => {

        const recherche =
            userSearch.value
                .trim()
                .toLowerCase();


        const utilisateurs =
            userList.querySelectorAll(
                ".user-item"
            );


        utilisateurs.forEach(
            (utilisateur) => {

                const nom =
                    utilisateur.dataset.name ||
                    "";


                utilisateur.style.display =
                    nom.includes(recherche)
                        ? "flex"
                        : "none";

            }
        );

    }
);


// ============================================================
// ENVOYER UN MESSAGE
// ============================================================

sendButton.addEventListener(
    "click",
    envoyerMessage
);


messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            envoyerMessage();

        }

    }
);


function envoyerMessage() {

    const message =
        messageInput.value.trim();


    // --------------------------------------------------------
    // Message vide
    // --------------------------------------------------------

    if (!message) {
        return;
    }


    // --------------------------------------------------------
    // Vérification pseudo
    // --------------------------------------------------------

    if (!pseudo) {

        pseudoModal.classList.remove(
            "hidden"
        );

        pseudoInput.focus();

        return;

    }


    // --------------------------------------------------------
    // Vérification connexion
    // --------------------------------------------------------

    if (!socket.connected) {

        afficherMessageSysteme(
            "Impossible d'envoyer le message : serveur déconnecté.",
            obtenirHeure()
        );

        console.error(
            "Tentative d'envoi alors que Socket.IO est déconnecté."
        );

        return;

    }


    // --------------------------------------------------------
    // Envoi
    // --------------------------------------------------------

    socket.emit(
        "message",
        {
            message: message.substring(
                0,
                2000
            )
        }
    );


    // --------------------------------------------------------
    // Nettoyage
    // --------------------------------------------------------

    messageInput.value = "";

    messageInput.focus();

}


// ============================================================
// EFFACER L'AFFICHAGE
// ============================================================

clearChatButton.addEventListener(
    "click",
    () => {

        messagesContainer.innerHTML = "";

        messageCount = 0;

        mettreAJourCompteurMessages();

        afficherBienvenue();

    }
);


// ============================================================
// COMPTEUR DE MESSAGES
// ============================================================

function mettreAJourCompteurMessages() {

    messageCountElement.textContent =
        messageCount;

}


// ============================================================
// ÉTAT DE CONNEXION
// ============================================================

function mettreAJourEtatConnexion(
    connecte
) {

    if (connecte) {

        connectionStatus.textContent =
            "Connecté au serveur";


        statusDot.classList.remove(
            "offline"
        );

        statusDot.classList.add(
            "online"
        );


        statusTitle.textContent =
            "En ligne";


        statusText.textContent =
            "Serveur accessible";


        networkText.textContent =
            "En ligne";


        chatStatus.textContent =
            pseudo
                ? "Connexion active"
                : "Prêt à rejoindre";


    } else {

        connectionStatus.textContent =
            "Déconnecté";


        statusDot.classList.remove(
            "online"
        );

        statusDot.classList.add(
            "offline"
        );


        statusTitle.textContent =
            "Hors ligne";


        statusText.textContent =
            "Connexion au serveur...";


        networkText.textContent =
            "Hors ligne";


        chatStatus.textContent =
            "En attente de connexion";

    }

}


// ============================================================
// DÉFILEMENT
// ============================================================

function faireDefilerVersBas() {

    messagesContainer.scrollTo({

        top:
            messagesContainer.scrollHeight,

        behavior:
            "smooth"

    });

}


// ============================================================
// INITIALES
// ============================================================

function obtenirInitiales(nom) {

    if (!nom) {
        return "?";
    }


    const morceaux =
        nom
            .trim()
            .split(/\s+/);


    if (morceaux.length === 1) {

        return morceaux[0]
            .substring(0, 2)
            .toUpperCase();

    }


    return (
        morceaux[0].charAt(0) +
        morceaux[1].charAt(0)
    ).toUpperCase();

}


// ============================================================
// HEURE
// ============================================================

function obtenirHeure() {

    const maintenant =
        new Date();


    return maintenant.toLocaleTimeString(
        "fr-FR",
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


// ============================================================
// THÈME
// ============================================================

themeToggle.addEventListener(
    "click",
    () => {

        document.body.classList.toggle(
            "dark"
        );


        const modeSombre =
            document.body.classList.contains(
                "dark"
            );


        localStorage.setItem(
            "chatlocal-theme",
            modeSombre
                ? "dark"
                : "light"
        );


        themeToggle.textContent =
            modeSombre
                ? "☀"
                : "☼";

    }
);


// ============================================================
// CHARGER LE THÈME
// ============================================================

function chargerTheme() {

    const theme =
        localStorage.getItem(
            "chatlocal-theme"
        );


    if (theme === "dark") {

        document.body.classList.add(
            "dark"
        );

        themeToggle.textContent =
            "☀";

    } else {

        document.body.classList.remove(
            "dark"
        );

        themeToggle.textContent =
            "☼";

    }

}


// ============================================================
// MODALE INFORMATIONS
// ============================================================

infoButton.addEventListener(
    "click",
    () => {

        infoModal.classList.remove(
            "hidden"
        );

    }
);


closeInfoButton.addEventListener(
    "click",
    () => {

        infoModal.classList.add(
            "hidden"
        );

    }
);


infoModal.addEventListener(
    "click",
    (event) => {

        if (
            event.target === infoModal
        ) {

            infoModal.classList.add(
                "hidden"
            );

        }

    }
);


// ============================================================
// ESCAPE
// ============================================================

document.addEventListener(
    "keydown",
    (event) => {

        if (event.key !== "Escape") {
            return;
        }


        if (
            !infoModal.classList.contains(
                "hidden"
            )
        ) {

            infoModal.classList.add(
                "hidden"
            );

        }

    }
);


// ============================================================
// EMOJI
// ============================================================

emojiButton.addEventListener(
    "click",
    () => {

        const emojis = [

            "😀",
            "😂",
            "😊",
            "😍",
            "👍",
            "❤️",
            "🔥",
            "🎉",
            "👏",
            "😎",
            "🙌",
            "😉",
            "🤝",
            "💯",
            "✨"

        ];


        const emoji =
            emojis[
                Math.floor(
                    Math.random() *
                    emojis.length
                )
            ];


        const start =
            messageInput.selectionStart;


        const end =
            messageInput.selectionEnd;


        const texte =
            messageInput.value;


        messageInput.value =
            texte.substring(
                0,
                start
            ) +
            emoji +
            texte.substring(
                end
            );


        messageInput.focus();


        const nouvellePosition =
            start + emoji.length;


        messageInput.setSelectionRange(
            nouvellePosition,
            nouvellePosition
        );

    }
);


// ============================================================
// TYPING INDICATOR
// ============================================================

function afficherTyping() {

    typingIndicator.classList.add(
        "visible"
    );

}


function masquerTyping() {

    typingIndicator.classList.remove(
        "visible"
    );

}


// Actuellement désactivé.
// La fonctionnalité pourra être connectée
// à Socket.IO ultérieurement.

masquerTyping();


// ============================================================
// LIMITATION DU MESSAGE
// ============================================================

messageInput.addEventListener(
    "input",
    () => {

        if (
            messageInput.value.length >
            2000
        ) {

            messageInput.value =
                messageInput.value.substring(
                    0,
                    2000
                );

        }

    }
);


