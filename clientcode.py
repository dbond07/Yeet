import socket,sys

def main():
    if (len(sys.argv) == 2):
        ip = sys.argv[0]
        port = sys.argv[1]
        print("arguments:", ip, port)
        port = int(port)
    else:
        print("Starting server")
        ip = input("IP address <b for base>: ")
        if (ip == 'b'):
            ip = "172.29.93.172"
        port_input = input("port number <b for base>: ")
        if (port_input == 'b'):
            port = 27993
        else:
            port = int(port_input)

    connect_value = connect(ip, port)
    if (connect_value[1] == 'failed to connect'):
        print(connect_value[1])
        sys.exit()
    print("Connection Successful")
    while(1):
        message = input("> ")
        send(connect_value[0], message)
        if (message == "q"):
            close(connect_value[0])
            print("quitting")
            sys.exit()


def connect(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and TCP

        sock.connect((ip, port))
        #after this I might want to have the server do a few connection things for verification
        #along with login and password shiz
        
        return ((sock, 'connection successful'))
    except socket.error:
        return (None, 'failed to connect')

def send(sock, message):
    sock.sendall(message.encode())

def receive(sock):
    m = sock.recv(1024)
    return m.decode()

def close(sock):
    sock.close()


if __name__ == "__main__":
    main()
