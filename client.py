import socket
import re
reserved = ['from', 'where', 'select']
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8181       # The port used by the server

s = socket.socket()
s.connect((HOST, PORT))
while True:
    correct = False
    print('Give a SQL Command!')
    while  (not correct):
        uinput = input()
        pattern = '^select\s(\*|([a-z]([a-z]*[0-9]*)+\s?\,\s?)*[a-z]([a-z]*[0-9]*)+)\sfrom\s([a-z]([a-z]*[0-9]*)+\s?\,\s?)*[a-z]([a-z]*[0-9]*)+(\swhere\s([a-z]([a-z]*[0-9]*)+\.)?[a-z]([a-z]*[0-9]*)+(\s)?(\=|\<|\>|(\<\>)|(\>\=)|(\<\=))(\s)?([a-z]([a-z]*[0-9]*)+\.)?[a-z]([a-z]*[0-9]*)+)?$'
        result = re.match(pattern, uinput)
        if result:
            x = uinput.replace(' ', ',')
            x = x.replace(',,', ',')
            words = x.split(',')
            wrongex = False;
            for r in reserved:
                count = 0
                for w in words:
                    if (w == r):
                        count +=1
                if (count > 1):
                    wrongex = True
            if (wrongex):
                print('Wrong Command Please try again!')
            else:
                print('Correct')
                correct = True
        else:
            print('Wrong Command Please try again!')
    tosend = ''
    existswhere = False
    for word in words:
        if (word == 'where'):
            existswhere = True
    if existswhere:
        tosend += '2,'
    else:
        tosend += '1,'
    for word in words:
        if (word == 'select'):
            pass
        elif (word in reserved):
            tosend += '@,'
        else:
            tosend = tosend + word + ','
    s.sendall(str.encode(tosend))
    data = s.recv(1024)
    if data:
        print('Received', repr(data))
    else:
        print("Connection closed")
        break
