import socket
PORT = 8181

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    print ("socket binded to %s" %(PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(19)
                if not data or data==b'stop':
                    conn.close()
                    break
                else:
                    print (data.decode())
                    conn.sendall(str.encode('thank you'))
                    print ("---------------")
