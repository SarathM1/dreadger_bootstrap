import socket
import time
import random
import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%d/%m/%Y %H:%M:%S', prop)


def Main():
    host = '127.0.0.1'
    port = 5000

    server = ('127.0.0.1',50001)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    

    #message = "ABC123;" + str(random.randrange(0, 101, 2))+";" + str(time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(None)))
    i=1
    while True:

       	message = str(i)+";"+"ABC123;" + str(random.randrange(100, 900, 2))+";" + randomDate("1/1/2008 1:30:00", "1/1/2009 4:50:00", random.random())
        i=i+1
        #print 'random:'+randomDate("1/1/2008 1:30:00", "1/1/2009 4:50:00", random.random())
	s.sendto(message,server)
	print 'data sent: ' + message
       	time.sleep(1)
    s.close()

if __name__=='__main__':
    Main()
