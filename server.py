#Importing socket to use our sockets and pickle to send objects through sockets
import socket, pickle
#Importing database to use the respective functions the client sends to access the database.
from database import Database
#Importing sys to handle errors
import sys
#The port the server uses.
PORT = 8181

#Asking the server user for the database name and loading it
print('Give me the database name:')
db_name = input()
db = Database(db_name,load=True)
#Create a socket object with the name s
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #Bind the port 8181 to the socket s
    s.bind(('', PORT))
    print ('socket binded to %s' %(PORT))
    #Make the socket listen to max 5 connections
    s.listen(5)
    #Keep it working
    while True:
        #When a connection comes, accept it and name it conn
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            #Keep receiving data until stopped
            while True:
                #Receive the first 1000 bytes
                data = conn.recv(1000)
                #Check if the client wants to stop the connection
                if not data or data==b'stop':
                    #Pickle and send a message back
                    message_string = pickle.dumps('Thank you for accessing our database')
                    conn.sendall(message_string)
                    print('Closing the connection')
                    conn.close()
                    break
                #Else start the proccess
                else:
                    clientinput = str(data.decode())
                    print (clientinput)
                    print ('---------------')
                    #We split the client input for easier checking by using the unique identifier
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
                        #Try to find the client requested table from the database
                        try:
                            #Get the table and then send it after pickling it
                            utable = db.select(remain[0],columns, return_object = True)
                            table_string = pickle.dumps(utable)
                            conn.sendall(table_string)
                            #Message of confirmation
                            print("The table has been sent")
                        #If it's not found send the key error to the client
                        except:
                            #Get the error, pickle it and send it
                            e = sys.exc_info()[1]
                            print(e)
                            db.unlock_table('classroom')
                            error_string = pickle.dumps(e)
                            conn.sendall(error_string)
                            #Message of confirmation
                            print("The error message has been sent")
                    elif list1[0]=='2':
                        print('case2')
                        i = remain.index('@')
                        table = remain[:i]
                        condition = remain[(i + 1):]
                        #Try to find the client requested table from the database
                        try:
                            #Get the table and then send it after pickling it
                            utable = db.select(table[0],columns,condition[0],return_object = True)
                            table_string = pickle.dumps(utable)
                            conn.sendall(table_string)
                            #Message of confirmation
                            print("The table has been sent")
                        #If it's not found send the key error to the client
                        except:
                            #Get the error, pickle it and send it
                            e = sys.exc_info()[1]
                            print(e)
                            db.unlock_table('classroom')
                            error_string = pickle.dumps(e)
                            conn.sendall(error_string)
                            #Message of confirmation
                            print("The error message has been sent")
