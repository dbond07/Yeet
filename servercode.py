import socket, sys, hashlib, json

def main():
    print("Address:", socket.gethostbyname(socket.gethostname()))
    if (len(sys.argv) == 2):
        ip = sys.argv[0]
        port = sys.argv[1]
        print("arguments:", ip, port)
        port = int(port)
    else:
        print("Starting server")
        ip = socket.gethostbyname(socket.gethostname())#input("IP address <b for base>: ")
        #if (ip == 'b'):
         #   ip = "172.29.93.172"
        port_input = input("port number <b for base>: ")
        if (port_input == 'b'):
            port = 27993
        else:
            port = int(port_input)
    value = start(ip, port)
    #print("connected to:", value[0])
    
    if (value[2] == "socket failed"):
        print(value[2])
        sys.exit()
    first_message = True
    user = ""
    while(1):
        message_pack = listen(value[0])
        #Here I can do string interpritation to get info like user, time, etc...
            #it should only allow you to set your name at the beginning
        if (first_message):
            user = first_recv(message_pack[1])
            if (user == None): #so they were not verified
                print("failed login")
                value[0].close()
                sys.exit()
            first_message = not first_message
        else:
            if (message_pack[0] == "Message Not Found"):
                print(message_pack[1])
                value[0].close()
                sys.exit()
            if (message_pack[1] == 'q'):
                #they are closing their connection
                print('user has quit')
                value[0].close()
                sys.exit()
            print(user + ">>", message_pack[1])
            #all I do is listen here and then print it
                
    value[0].close()

#we are doing it this way so that when we release this nobody can connect to my pi
def start(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((socket.gethostname(), port))
    except socket.error:
        return ((None, None, "socket failed"))

    try:
        sock.listen()#might need to spawn threads to have multiple ones listening
        conn, addr = sock.accept()
        return ((conn, addr, "connection"))
    except socket.error:
        return ((None, None, "could not connect"))

#this will cause an error if they dont give a proper message <ADD SECURITY HERE LATER>
    #otherwise itll just return the name
def first_recv(message):
    values = message.split()
    if (len(values) != 2):
        print("Malformed message")
        return None
    else:
        #heres where we will check for passwords
        if (checkPas(values[0], values[1])):
            return values[0]
        else:
            #incorrect password
            #send data back to them saying it was wrong
            return values[0] #TODO SOMETHING IS WRONG HERE ******

#this will check if a user's password is correct
def checkPas(user, password):
    #first we check if the user already exists
    users = read_json("users.json")
        #we are salting their password so nobody can get the passwords if they gained access to the file
    if (user.lower in users):
        #so it is a user
        #now we check the password
        return (hashlib.sha256(str.encode(password + str(users[user][1]))).hexdigest()
                == users[user][0])
    return False #for now we are just returning true

def write_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def read_json(file):
    with open(file) as infile:
        data = json.load(infile)
    return data


    
def listen(conn):
    r_message = conn.recv(1024).decode()
    if not r_message:
        return (("Message Not Found", "message not found"))
    return (("Message received", r_message))


if __name__ == "__main__":
    main()
