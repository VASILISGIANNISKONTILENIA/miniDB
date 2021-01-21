import socket, pickle
from database import Database
import sys
PORT = 8181

#Load db import Database
db = Database('vsmdb',load=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    print ('socket binded to %s' %(PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1000)
                #Check if the client wants to stop the connection
                if not data or data==b'stop':
                    conn.sendall('Thank you for accessing our database')
                    conn.close()
                    break
                #Else start the proccess
                else:
                    clientinput = str(data.decode())
                    print (clientinput)
                    print ('---------------')
                    #We split the client input for easier checking
                    list1 = clientinput.split(',')
                    list2 = list1[1:]
                    i = list2.index('@')
                    columns = list2[:i]
                    remain = list2[(i + 1):]
                    if columns == ['*']:
                        columns = '*'
                    #Check which select command the user chose
                    if list1[0]=='1' :
                        print('case1')
                        utable = db.select(remain[0],columns, return_object = True)
                        #If there was a table returned, pickle it and then send it
                        if(bool(utable):
                            table_string = pickle.dumps(utable)
                            conn.sendall(table_string)
                            print('The table has been sent')
                        #Else send a message that there was no table found
                        else:
                            message_string = pickle.dumps('There was no table found')
                            conn.sendall(message_string)
                    elif list1[0]=='2':
                        print('case2')
                        i = remain.index('@')
                        table = remain[:i]
                        condition = remain[(i + 1):]
                        utable = db.select(table[0],columns,condition[0],return_object = True)
                        #If there was a table returned, pickle it and then send it
                        if(bool(utable):
                            table_string = pickle.dumps(utable)
                            conn.sendall(table_string)
                            print('The table has been sent')
                        #Else send a message that there was no table found
                        else:
                            message_string = pickle.dumps('There was no table found')
                            conn.sendall(message_string)
