# Modulo de base de datos
import sqlite3
from datetime import datetime
from config import DB_NAME

# Creacion de la base de datos SQLite
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

     # Crear la tabla de mensajes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_client TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Guardar un mensaje en la base de datos
def save_message(content, ip_client):
    timestamp = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insertar el mensaje en la base de datos
    cursor.execute('''
        INSERT INTO messages (content, sent_date, ip_client)
        VALUES (?, ?, ?)
        ''', (content, timestamp, ip_client)
    )

    conn.commit()
    conn.close()
    return timestamp
