import socket
import time
import random
def Main():
    host = '127.0.0.1'
    port = 5000

    server = ('127.0.0.1',50001)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    

    #message = "ABC123;" + str(random.randrange(0, 101, 2))+";" + str(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(None)))
    while True:
       	message = "ABC123;" + str(random.randrange(100, 900, 2))+";" + str(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(None)))
	s.sendto(message,server)
	print 'data sent: ' + message
       	time.sleep(1)
    s.close()

if __name__=='__main__':
    Main()
