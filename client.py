import socket, pickle
from table import Table
import re
reserved = ['from', 'where', 'select']
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8181       # The port used by the server

s = socket.socket()
s.connect((HOST, PORT))
while True:
    #Variable used for checking if the user input complies with the conditions
    correct = False
    print('Give an SQL Command or the word #stop# to stop the proccess')
    while(not correct):
        uinput = input()
        uinput = uinput.lower()
        if(uinput == 'stop'):
            break
        #Checking if the input matches the regex used for the sql command
        pattern = '^select\s(\*|(([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\s?\,\s?)*([a-z]|(\_))([a-z]*[0-9]*(\_)*)+)\sfrom\s(([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\s?\,\s?)*([a-z]|(\_))([a-z]*[0-9]*(\_)*)+(\swhere\s(([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\.)?([a-z]|(\_))([a-z]*[0-9]*(\_)*)+(\=\=|\<|\>|(\>\=)|(\<\=))(((([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\.)?([a-z]|(\_))([a-z]*[0-9]*(\_)*)+)|[0-9]+))?$'
        result = re.match(pattern, uinput)
        #If it does check if there are any reserved words in the command
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
        #It does not match the pattern
        else:
            print('Wrong Command Please try again!')
    #Checking which command we have so we send an appropriate code to the server while also preparing the command for easier use on the server
    if(uinput != 'stop'):
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
        tosend = tosend[:-1]
    else:
        tosend = 'stop'
    #Send the command through the socket
    s.sendall(str.encode(tosend))
    #We receive data from the server
    data = s.recv(4096)
    data_variable = pickle.loads(data)
    #If it's an object with the Table type, we have our correct table
    if isinstance(data_variable,Table):
        print('Received a table:')
        data_variable.show()
    #If it's an error type that there was an error found in the database and type the error keyword
    elif isinstance(data_variable,KeyError):
        print('It seems there was a problem pulling the data from the database.')
        print(data_variable)
    #Else type the message we received from the server
    else:
        print(data_variable)
        break;
