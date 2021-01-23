#Importing socket to use our sockets and pickle to send objects through sockets
import socket, pickle
#Importing table to use the table function so we can show our table
from table import Table
#Importing regex to check correct user input
import re
#Reserved SQL words
reserved = ['from', 'where', 'select']
#The server's hostname or IP address
HOST = '127.0.0.1'
#The port used by the server
PORT = 8181

#Creating a new socket object
s = socket.socket()
#Connect to the server with our given ip and port
s.connect((HOST, PORT))
while True:
    #Variable used for checking if the user input complies with the conditions
    correct = False
    print('Give an SQL Command or the word #stop# to stop the proccess')
    while(not correct):
        uinput = input()
        #Make all the letters lower case for easier
        uinput = uinput.lower()
        #Stop input stops the client connection
        if(uinput == 'stop'):
            break
        #Checking if the input matches the regex used for the sql command
        pattern = '^select\s(\*|(([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\s?\,\s?)*([a-z]|(\_))([a-z]*[0-9]*(\_)*)+)\sfrom\s(([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\s?\,\s?)*([a-z]|(\_))([a-z]*[0-9]*(\_)*)+(\swhere\s(([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\.)?([a-z]|(\_))([a-z]*[0-9]*(\_)*)+(\=\=|\<|\>|(\>\=)|(\<\=))(((([a-z]|(\_))([a-z]*[0-9]*(\_)*)+\.)?([a-z]|(\_))([a-z]*[0-9]*(\_)*)+)|[0-9]+))?$'
        result = re.match(pattern, uinput)
        #If it does check if there are any reserved words in the command
        if result:
            #Removing the whitespaces and unnecessary comas and putting all the words in a list by splitting them by the necessary comas
            x = uinput.replace(' ', ',')
            x = x.replace(',,', ',')
            x = x.replace(',,', ',')
            words = x.split(',')
            #Checking if any of the words in the list belongs in the reserved list
            wrongex = False;
            for r in reserved:
                count = 0
                for w in words:
                    if (w == r):
                        count +=1
                if (count > 1):
                    wrongex = True
            #If there is, the command is wrong
            if (wrongex):
                print('Wrong Command Please try again!')
            #Else it's correct
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
        #If the word where is on the list, we have the case 2 which means existswhere gets the bool value True. If not we have case1.
        for word in words:
            if (word == 'where'):
                existswhere = True
        #cas2
        if existswhere:
            tosend += '2,'
        #case1
        else:
            tosend += '1,'
        #Changing the rest of the keywords to the selected identifier
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
    elif isinstance(data_variable,BaseException):
        print('It seems there was a problem pulling the data from the database.')
        print(data_variable)
    #Else type the message we received from the server
    else:
        print(data_variable)
        break;
