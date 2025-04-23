import socket
from config import HOST, PORT

def run_client():
    # Crear un socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conectar el socket al servidor
    client_socket.connect((HOST, PORT))
    print(f"Conectado al servidor en {HOST}:{PORT}")

    try:
        while True:
            # Leer el mensaje del usuario
            message = input("Ingrese su mensaje (o 'exit' para salir): ")
            # Enviar el mensaje al servidor
            client_socket.sendall(message.encode('utf-8'))
            # Si el mensaje es exit, cerrar la conexión
            if message.lower() == 'exit':
                break
            # Recibir la respuesta del servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor: {response}")
    except KeyboardInterrupt:
        print("\nCliente detenido.")
    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_client()