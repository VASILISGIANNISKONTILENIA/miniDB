import socket
#from database import Database
PORT = 8181

#load db import Database
#db = Database('vsmdb',load=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    print ("socket binded to %s" %(PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1000)
                #Not in use
                if not data or data==b'stop':
                    conn.close()
                    break
                #In use
                else:
                    clientinput = str(data.decode())
                    print (clientinput)
                    conn.sendall(str.encode('thank you'))
                    print ("---------------")
                    list1 = clientinput.split(",")
                    print(list1)
                    list2 = list1[1:]
                    i = list2.index("@")
                    columns = list2[:i]
                    remain = list2[(i + 1):]
                    print(columns)
                    if list1[0]=='1' :
                        print('case1')
                        #db.select(columns,remain[0])
                    elif list1[0]=='2' :
                        print('case2')
                        i = remain.index("@")
                        table = remain[:i]
                        condition = remain[(i + 1):]
                        print(table)
                        print(condition)
                        #db.select(columns,table[0],condition[0])