import socket


def main():
    print("Welcome to the Andrew Messaging System")
    print("The purpose of this app is to talk during class and learn at the same time")

    ip = input("IP address <b for base>: ")
    if (ip == 'b'):
        ip = "172.29.93.172"
    port_input = input("port number <b for base>: ")
    if (port_input == 'b'):
        port = 27993
    else:
        port = int(port_input)
    choice = ""

    while (choice != 'c' and choice != 's'):
        choice = input("Enter \'c\' for client program, or \'s\' for server: ")

    if (choice == 's'):
        print("you chose server, have your friend run this with client mode")
        server_code(ip, port)
    else:
        print("you chose client, have your friend run this with server mode")
        client_code(ip, port)
    input("Press Enter to exit")

def server_code(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((socket.gethostname(), port))

    
    sock.listen()
    conn, addr = sock.accept()
    print("Connection from", addr)
    while 1:
            print("listening...")
            r_message = conn.recv(1024).decode()
            if not r_message: break
            print(">> " + r_message)
            message = input("send: ")
            conn.sendall(message.encode())
            if (message == 'exit'):
                break
    conn.close()

def client_code(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and TCP
    except socket.error:
        print('failed to connect')
               
    #now i connect the socket to the address and IP
    sock.connect((ip, port))

    #now we can send i beleive
    message = ""
    r_message = ""
    while (message != "exit" and r_message != "exit"):
        message = input("send: ") #will change this later so u dont have to send to receive
        print(">> " + r_message)
        sock.sendall(message.encode())
        r_message = sock.recv(1024).decode()
        if (r_message == 'exit'):
            print("Other user has left")
            break
    sock.close()

#this calls the main function to start the program
if __name__== "__main__":
    main()
