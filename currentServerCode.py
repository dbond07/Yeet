import socket, sys, hashlib, json, time

isRunning = True
def main():
    serverName = "Drew's server" #<- this is what you want to name the server, can change it later

    print("Address:", socket.gethostbyname(socket.gethostname()))
    if (len(sys.argv) == 3):
        ip = sys.argv[1]
        if (ip == 'b'):
            ip = socket.gethostbyname(socket.gethostname())
        port = int(sys.argv[0])
        print("arguments:", ip, port)
    else:
        print("Starting server")
        ip = socket.gethostbyname(socket.gethostname())#input("IP address <b for base>: ")
        #print(ip)#if (ip == 'b'):
         #   ip = "172.29.93.172"
        port_input = input("port number <b for base>: ")
        if (port_input == 'b'):
            port = 27993
        else:
            port = int(port_input)

    if (input('new file? y/n:') == 'y'):
        with open('MESSAGE_FILE.json', mode='w', encoding='utf-8') as f:
            json.dump([], f)

    value = start(ip, port)
    #print("connected to:", value[0])

    while (value[2] == "socket failed"):
        print(value[2])
        sys.exit()
    user = ""
    first_command = True
    global isRunning
    while(isRunning):
        message_pack = listen(value[0])

        #Here I can do string interpritation to get info like user, time, etc...
        if (message_pack[0] == "Message Not Found"):
            #might change to \x00 or some other character that they cant put in
            pass
        else:
            commands = message_pack[1].split(';') #we are seperating it by ';' for each command
                #POSSIBLE SECURITY FLAW:: if someone inserts a ';' inside a command like 'l admin passwo;rd'
            #print(commands)
            for command in commands:
                #print(command)
                if (len(command) == 0):
                    reply(value[0], 'no command')
                elif (first_command):
                    if (str(command) == 'T'):
                        #testing connection
                        reply(value[0], 'Connected to:' + serverName)
                        break
                    first_command = False
                    attempt = login(command)
                    if (attempt[1] == "F"):
                        #failed login
                        reply(value[0], 'failed login')
                        break
                    reply(value[0], 'login successful')
                    user = attempt[0]
                else:
                    ret_message = do_command(command, user, value[0])
                    if (ret_message == 'MASTER CLOSE COMMAND 018927497'):
                        reply(value[0], 'closing')
                        isRunning = False
                        value[0].close()
                        print('done')
                        sys.exit()
                        break
                    else:
                        #send data back to the user about permissions for each command
                        reply(value[0], ret_message)
            #so we've now gone through the list
                        #now we tell them that we are done
            reply(value[0], 'finished') #possible security flaw*********************if someone sends this then they could crash it

        value[0].close() #closing out the connection to start the next one
        first_command = True
        #restart while waiting for a different connection
        value = start(ip, port)
        while (value[2] == "socket failed"):
            #print(value[2] + " : " + value[0])
            value = start(ip, port)
    #value[0].close()
    print('done')


#------------------------------------------------------server commands----------------------

def do_command(command, user, sock):
    if (command.split(' ')[0] not in ['q', 'p', 'g']):
        return 'not valid command'
    #something weird is going on here with p vs g


    #commands to add in the future:
        #a user password:    adds a user
        #c old new:          change password from old to new
        #k n:                keep connection open for n more commands
        #y time              you can 'yeet' a message
    if (command.split(' ')[0] == 'g'):#because this has issues for some reason
        return get_messages(command, user, sock)

    return {
        'p': post(command, user), #posts a message
        'q': stop_running(command, user)
        }.get(command.split(' ')[0])

def login(command):
    #form is: l user password
    m = command.split(' ')
    if (len(m) != 3 or command[0] != 'l'):
        return ("failed","F") #failed login
    return (m[1], "A") #login accepted
def stop_running(command, user):
    if (command[0] != 'q'):
        return '' #this is a really weird bug
    if (user == 'admin'):
        global isRunning
        isRunning = False
        return 'MASTER CLOSE COMMAND 018927497'
    else:
        return 'close failed'

def get_messages(command, user, sock):
    get_list('MESSAGE_FILE.json')
    timesense = 0
    if (len(command.split(' ')) == 2):
        #possible security issue here
        timesense = float(command.split(' ')[1])
    messages = get_list('MESSAGE_FILE.json')
    time_after_messages = [m for m in messages if (m['time'] > timesense)]
    for m in time_after_messages:
        #we are doing a special reply pattern here
        sock.sendall((m['user'] + ' likes:' + str(len(m['likes'])) + ' >>'
                      + m['message']
                      + '\n').encode())
    total_messages = len(time_after_messages)
    return "total messages: " + str(total_messages) + " @" + str(time.time())


def post(command, user):
    #we will assume we have a file already
    #first we want to get the message out of the command
    message = command[2:] #because we just want everything after the first space

    #now we build our dictionary to add
    out_dic = {'user': user,
               'likes': [],
               'message' : message,
               'time': time.time()}#the current time in unix sense epoch
    append_json(out_dic, 'MESSAGE_FILE.json')
    return "posted message @" + str(time.time())

#-----------------------------------------------------------password stuff----------------------

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

#------------------------------------------------------------------------files----------------------

def append_json(data, filename):
    #need to first get all the data
    feeds = get_list(filename)
    with open(filename, mode='w', encoding='utf-8') as feedsjson:
        entry = data #so we have a dictionary for data
        feeds.append(entry)
        json.dump(feeds, feedsjson)

def get_list(filename):
    with open(filename, 'r') as infile:
        dic = json.load(infile)
    return dic

def write_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def read_json(file):
    with open(file) as infile:
        data = json.load(infile)
    return data

#----------------------------------------------------------------------TCP network things-------------

def reply(conn, message):
    conn.sendall((str(message) + ';').encode())

def listen(conn):
    r_message = conn.recv(1024).decode()
    if not r_message:
        return (("Message Not Found", "message not found"))
    return (("Message received", r_message))


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
            return values[0]

if __name__ == "__main__":
    main()
