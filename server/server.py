import socket
import threading
from server.database import init_db, save_message
from config import HOST, PORT
import sqlite3
import sys

def handler_client(conn, addr): 
    try:
        print(f"Conexión establecida con cliente de ip {addr[0]}:{addr[1]}")
        while True:
            try:
                # Recibir el mensaje del cliente
                message = conn.recv(1024).decode('utf-8')
                # si el mensaje es exit, cerrar la conexión
                if not message or message.lower() == 'exit':
                    print(f"Cliente {addr[0]}:{addr[1]} ha cerrado la conexión.")
                    break
                try:
                    # Guardar el mensaje en la base de datos
                    ip_client = f'{addr[0]}:{addr[1]}'
                    timestamp = save_message(message, ip_client)
                    response = f"Message recived at {timestamp}"
                    # Enviar la fecha y hora de envío al cliente
                    conn.sendall(response.encode('utf-8'))
                except sqlite3.Error as db_error:
                    print(f"Error al guardar el mensaje en la base de datos: {db_error}")
                    conn.sendall(b"Error al guardar el mensaje en la base de datos.")
            except ConnectionResetError:
                print(f"Conexión cerrada por el cliente {addr[0]}:{addr[1]}")
                break
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        conn.close()
        print(f"Conexión cerrada con {addr[0]}:{addr[1]}")

def start_server():
    try:
        # Inicializar la base de datos
        init_db()
    except sqlite3.Error as db_error:
        print(f"Error al inicializar la base de datos: {db_error}")
        sys.exit(1)

    # Configuracion de un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
    except OSError as e:
        print(f"\nError: No se pudo bindear al puerto {PORT}")
        print(f"Causa: {e}")
        print("Posibles soluciones:")
        print("1. Cierra cualquier otro servidor que esté usando este puerto")
        print("2. Espera 1-2 minutos para que el sistema libere el puerto")
        print("3. Cambia el puerto en config.py")
        sys.exit(1)
    try:
        server_socket.listen()    
        print(f"Servidor escuchando en {HOST}:{PORT}")
        print("Presiona Ctrl+C para detener el servidor")
        
        while True:
            try:
                # Esperar a que un cliente se conecte
                conn, addr = server_socket.accept()
                # Crear un hilo para manejar al cliente
                client_thread = threading.Thread(target=handler_client, args=(conn, addr), daemon=True)
                client_thread.start()
            except OSError:
                break
    except KeyboardInterrupt:
        print("Servidor detenido. Esperando que los hilos terminen...")
    finally:
        server_socket.close()
        print("Socket cerrado correctamente.")

if __name__ == "__main__":
    start_server()