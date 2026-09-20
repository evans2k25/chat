
/* =========================================================
   CHAT LOCAL
   Socket.IO + Bootstrap
========================================================= */


document.addEventListener("DOMContentLoaded", function () {

    "use strict";


    /* =====================================================
       SOCKET.IO
    ====================================================== */

    const socket = io();


    /* =====================================================
       VARIABLES
    ====================================================== */

    let pseudo = "";

    let connected = false;


    /* =====================================================
       ELEMENTS
    ====================================================== */

    const messagesContainer =
        document.getElementById("messagesContainer");

    const messages =
        document.getElementById("messages");

    const messageInput =
        document.getElementById("messageInput");

    const sendButton =
        document.getElementById("sendButton");

    const pseudoInput =
        document.getElementById("pseudoInput");

    const joinButton =
        document.getElementById("joinButton");

    const pseudoError =
        document.getElementById("pseudoError");

    const usersList =
        document.getElementById("usersList");

    const usersCount =
        document.getElementById("usersCount");

    const connectionText =
        document.getElementById("connectionText");

    const onlineStatus =
        document.getElementById("onlineStatus");

    const logoutButton =
        document.getElementById("logoutButton");

    const openSidebar =
        document.getElementById("openSidebar");

    const closeSidebar =
        document.getElementById("closeSidebar");

    const sidebar =
        document.getElementById("sidebar");

    const infoButton =
        document.getElementById("infoButton");


    /* =====================================================
       MODAL PSEUDO
    ====================================================== */

    const pseudoModalElement =
        document.getElementById("pseudoModal");

    const pseudoModal =
        new bootstrap.Modal(
            pseudoModalElement
        );


    /* =====================================================
       MODAL INFO
    ====================================================== */

    const infoModalElement =
        document.getElementById("infoModal");

    const infoModal =
        new bootstrap.Modal(
            infoModalElement
        );


    /* =====================================================
       AFFICHER MODAL PSEUDO
    ====================================================== */

    pseudoModal.show();


    setTimeout(function () {

        pseudoInput.focus();

    }, 500);


    /* =====================================================
       CONNEXION SOCKET
    ====================================================== */

    socket.on("connect", function () {

        connected = true;

        connectionText.textContent =
            "Connecté au serveur";

        onlineStatus.innerHTML =
            '<span class="online-dot"></span> En ligne';

        console.log(
            "[SOCKET] Connecté :",
            socket.id
        );

    });


    /* =====================================================
       DECONNEXION SOCKET
    ====================================================== */

    socket.on("disconnect", function () {

        connected = false;

        connectionText.textContent =
            "Déconnecté";

        onlineStatus.innerHTML =
            '<span style="color:#ef4444;">●</span> Hors ligne';

        console.log(
            "[SOCKET] Déconnecté"
        );

    });


    /* =====================================================
       REJOINDRE LE CHAT
    ====================================================== */

    function rejoindreChat() {

        const valeur =
            pseudoInput.value.trim();


        if (!valeur) {

            pseudoError.classList.add("show");

            pseudoInput.focus();

            return;
        }


        pseudoError.classList.remove("show");


        pseudo =
            valeur.substring(0, 30);


        localStorage.setItem(
            "chat_pseudo",
            pseudo
        );


        socket.emit(
            "connexion",
            {
                pseudo: pseudo
            }
        );


        pseudoModal.hide();


        messageInput.focus();


        console.log(
            "[CHAT] Pseudo :",
            pseudo
        );
    }


    /* =====================================================
       BOUTON REJOINDRE
    ====================================================== */

    joinButton.addEventListener(
        "click",
        rejoindreChat
    );


    /* =====================================================
       ENTER DANS PSEUDO
    ====================================================== */

    pseudoInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                rejoindreChat();
            }

        }
    );


    /* =====================================================
       MESSAGE
    ====================================================== */

    function envoyerMessage() {

        const message =
            messageInput.value.trim();


        if (!message) {

            return;
        }


        if (!connected) {

            afficherMessageSysteme(
                "Vous n'êtes pas connecté au serveur."
            );

            return;
        }


        if (!pseudo) {

            pseudoModal.show();

            return;
        }


        socket.emit(
            "message",
            {
                message: message
            }
        );


        messageInput.value = "";

        messageInput.focus();

    }


    /* =====================================================
       BOUTON ENVOYER
    ====================================================== */

    sendButton.addEventListener(
        "click",
        envoyerMessage
    );


    /* =====================================================
       ENTER POUR ENVOYER
    ====================================================== */

    messageInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                envoyerMessage();
            }

        }
    );


    /* =====================================================
       RECEVOIR UN MESSAGE
    ====================================================== */

    socket.on(
        "nouveau_message",
        function (data) {

            if (!data) {

                return;
            }


            supprimerBienvenue();


            const estMoi =
                data.pseudo === pseudo;


            afficherMessage(
                data.pseudo || "Utilisateur",
                data.message || "",
                data.heure || obtenirHeure(),
                estMoi
            );

        }
    );


    /* =====================================================
       MESSAGE SYSTEME
    ====================================================== */

    socket.on(
        "message_systeme",
        function (data) {

            if (!data) {

                return;
            }


            supprimerBienvenue();


            afficherMessageSysteme(
                data.message || "",
                data.heure || obtenirHeure()
            );

        }
    );


    /* =====================================================
       LISTE DES UTILISATEURS
    ====================================================== */

    socket.on(
        "liste_utilisateurs",
        function (utilisateurs) {

            afficherUtilisateurs(
                utilisateurs || []
            );

        }
    );


    /* =====================================================
       AFFICHER MESSAGE
    ====================================================== */

    function afficherMessage(
        expediteur,
        texte,
        heure,
        estMoi
    ) {

        const row =
            document.createElement("div");


        row.className =
            "message-row " +
            (estMoi ? "mine" : "other");


        const content =
            document.createElement("div");


        content.className =
            "message-content";


        if (!estMoi) {

            const sender =
                document.createElement("div");


            sender.className =
                "message-sender";


            sender.textContent =
                expediteur;


            content.appendChild(sender);

        }


        const bubble =
            document.createElement("div");


        bubble.className =
            "message-bubble";


        /*
         * textContent est volontairement utilisé
         * pour empêcher l'injection de HTML/JS.
         */

        bubble.textContent =
            texte;


        const time =
            document.createElement("div");


        time.className =
            "message-time";


        time.textContent =
            heure;


        content.appendChild(bubble);

        content.appendChild(time);

        row.appendChild(content);

        messages.appendChild(row);


        faireDefilerVersBas();

    }


    /* =====================================================
       MESSAGE SYSTEME
    ====================================================== */

    function afficherMessageSysteme(
        texte,
        heure = ""
    ) {

        const wrapper =
            document.createElement("div");


        wrapper.className =
            "system-message";


        const message =
            document.createElement("span");


        message.textContent =
            texte +
            (heure ? " • " + heure : "");


        wrapper.appendChild(message);

        messages.appendChild(wrapper);


        faireDefilerVersBas();

    }


    /* =====================================================
       UTILISATEURS
    ====================================================== */

    function afficherUtilisateurs(
        utilisateurs
    ) {

        usersList.innerHTML = "";


        usersCount.textContent =
            utilisateurs.length;


        if (utilisateurs.length === 0) {

            const empty =
                document.createElement("div");


            empty.className =
                "empty-users";


            empty.innerHTML =
                `
                <i class="bi bi-person"></i>
                <span>Aucun utilisateur</span>
                `;


            usersList.appendChild(empty);

            return;
        }


        utilisateurs.forEach(
            function (nom) {

                const item =
                    document.createElement("div");


                item.className =
                    "user-item";


                const avatar =
                    document.createElement("div");


                avatar.className =
                    "user-avatar";


                avatar.textContent =
                    obtenirInitiales(nom);


                const info =
                    document.createElement("div");


                info.className =
                    "user-info";


                const name =
                    document.createElement("span");


                name.className =
                    "user-name";


                name.textContent =
                    nom;


                const status =
                    document.createElement("span");


                status.className =
                    "user-online";


                status.innerHTML =
                    `
                    <span class="status-dot">
                    </span>
                    En ligne
                    `;


                info.appendChild(name);

                info.appendChild(status);

                item.appendChild(avatar);

                item.appendChild(info);


                usersList.appendChild(item);

            }
        );

    }


    /* =====================================================
       INITIALLES
    ====================================================== */

    function obtenirInitiales(nom) {

        if (!nom) {

            return "?";
        }


        const mots =
            nom.trim().split(/\s+/);


        if (mots.length === 1) {

            return mots[0]
                .substring(0, 2)
                .toUpperCase();

        }


        return (
            mots[0][0] +
            mots[mots.length - 1][0]
        ).toUpperCase();

    }


    /* =====================================================
       HEURE
    ====================================================== */

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


    /* =====================================================
       SCROLL
    ====================================================== */

    function faireDefilerVersBas() {

        requestAnimationFrame(
            function () {

                messagesContainer.scrollTo(
                    {
                        top:
                            messagesContainer.scrollHeight,

                        behavior:
                            "smooth"
                    }
                );

            }
        );

    }


    /* =====================================================
       SUPPRIMER BIENVENUE
    ====================================================== */

    function supprimerBienvenue() {

        const welcome =
            document.querySelector(
                ".welcome-message"
            );


        if (welcome) {

            welcome.remove();
        }

    }


    /* =====================================================
       MENU MOBILE
    ====================================================== */

    openSidebar.addEventListener(
        "click",
        function () {

            sidebar.classList.add(
                "open"
            );

        }
    );


    closeSidebar.addEventListener(
        "click",
        function () {

            sidebar.classList.remove(
                "open"
            );

        }
    );


    /* =====================================================
       INFORMATIONS
    ====================================================== */

    infoButton.addEventListener(
        "click",
        function () {

            infoModal.show();

        }
    );


    /* =====================================================
       DECONNEXION
    ====================================================== */

    logoutButton.addEventListener(
        "click",
        function () {

            if (connected) {

                socket.disconnect();

            }


            connected = false;

            pseudo = "";

            usersList.innerHTML = "";


            usersCount.textContent =
                "0";


            connectionText.textContent =
                "Déconnecté";


            pseudoInput.value = "";


            pseudoModal.show();

        }
    );


    /* =====================================================
       EMOJI
    ====================================================== */

    document
        .getElementById("emojiButton")
        .addEventListener(
            "click",
            function () {

                const emojis = [
                    "😀",
                    "😂",
                    "😍",
                    "👍",
                    "❤️",
                    "🔥",
                    "🎉",
                    "👏",
                    "😊",
                    "😎"
                ];


                const emoji =
                    emojis[
                        Math.floor(
                            Math.random() *
                            emojis.length
                        )
                    ];


                messageInput.value +=
                    emoji;


                messageInput.focus();

            }
        );


    /* =====================================================
       PIECE JOINTE
    ====================================================== */

    document
        .getElementById("attachmentButton")
        .addEventListener(
            "click",
            function () {

                afficherMessageSysteme(
                    "Le partage de fichiers sera ajouté prochainement."
                );

            }
        );


    /* =====================================================
       PSEUDO EXISTANT
    ====================================================== */

    const ancienPseudo =
        localStorage.getItem(
            "chat_pseudo"
        );


    if (ancienPseudo) {

        pseudoInput.value =
            ancienPseudo;

    }


    /* =====================================================
       FERMER SIDEBAR APRÈS CLIC
       SUR MOBILE
    ====================================================== */

    document.addEventListener(
        "click",
        function (event) {

            if (
                window.innerWidth <= 768 &&
                sidebar.classList.contains("open") &&
                !sidebar.contains(event.target) &&
                !openSidebar.contains(event.target)
            ) {

                sidebar.classList.remove(
                    "open"
                );

            }

        }
    );


    /* =====================================================
       LOG
    ====================================================== */

    console.log(
        "Chat Local initialisé."
    );

});

