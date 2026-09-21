import sqlite3
import os
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE = os.path.join(
    BASE_DIR,
    "chat.db"
)


# ============================================================
# CONNEXION À LA BASE
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALISATION
# ============================================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            message TEXT NOT NULL,
            date_message TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()

    print("Base de données initialisée.")


# ============================================================
# ENREGISTRER UN MESSAGE
# ============================================================

def enregistrer_message(pseudo, message):

    connection = get_connection()

    cursor = connection.cursor()

    date_message = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO messages (
            pseudo,
            message,
            date_message
        )
        VALUES (?, ?, ?)
    """, (
        pseudo,
        message,
        date_message
    ))

    connection.commit()

    message_id = cursor.lastrowid

    connection.close()

    return message_id


# ============================================================
# RÉCUPÉRER LES MESSAGES
# ============================================================

def recuperer_messages(limite=50):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            pseudo,
            message,
            date_message
        FROM messages
        ORDER BY id DESC
        LIMIT ?
    """, (limite,))

    messages = cursor.fetchall()

    connection.close()

    return list(reversed(messages))