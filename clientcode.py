import socket,sys

def main():
    if (len(sys.argv) == 3):
        ip = sys.argv[1]
        port = sys.argv[2]
        print("arguments:", ip, port)
        port = int(port)
    else:
        print("Starting server")
        ip = input("IP address <b for base>: ")
        if (ip == 'b'):
            ip = "3.18.46.249" #this is will not be here in the final version
        elif (ip == 't'):
            ip = socket.gethostbyname(socket.gethostname())
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
    message = input("> ")
    send(connect_value[0], message)
    rec = receive(connect_value[0])
    print(rec)
    while(('finished;' not in rec) and ('closing;' not in rec)):
        rec = receive(connect_value[0])
        print(rec)
    close(connect_value[0])


def connect(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and TCP

        sock.connect((ip, port))
        
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
