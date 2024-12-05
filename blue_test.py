import bluetooth

# Cria um socket Bluetooth
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Define o número da porta e inicia o serviço
port = 1
server_socket.bind(("", port))
server_socket.listen(1)

print("Aguardando conexão...")
client_socket, address = server_socket.accept()
print(f"Conectado a {address}")

try:
    while True:
        # Recebe dados do cliente
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Recebido: {data.decode('utf-8')}")

except OSError:
    pass

print("Desconectado.")
client_socket.close()
server_socket.close()
