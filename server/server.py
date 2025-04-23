import socket
import threading
from server.database import init_db, save_message
from config import HOST, PORT

def handler_client(conn, addr): 
    try:
        print(f"Conexión establecida con cliente de ip {addr[0]}:{addr[1]}")
        while True:
            # Recibir el mensaje del cliente
            message = conn.recv(1024).decode('utf-8')
            # si el mensaje es exit, cerrar la conexión
            if not message or message.lower() == 'exit':
                print(f"Cliente {addr[0]}:{addr[1]} ha cerrado la conexión.")
                break
            # Guardar el mensaje en la base de datos
            ip_client = addr[0]
            timestamp = save_message(message, ip_client)
            response = f"Message recived at {timestamp}"
            # Enviar la fecha y hora de envío al cliente
            conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"Conexión cerrada con {addr[0]}:{addr[1]}")

def start_server():
    # Inicializar la base de datos
    init_db()
    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    try:
        while True:
            # Esperar a que un cliente se conecte
            conn, addr = server_socket.accept()
            # Crear un hilo para manejar al cliente
            client_thread = threading.Thread(target=handler_client, args=(conn, addr), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("Servidor detenido. Esperando que los hilos terminen...")
    finally:
        server_socket.close()
        print("Socket cerrado correctamente.")

if __name__ == "__main__":
    start_server()