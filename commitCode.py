#!/usr/bin/python

from subprocess import Popen as p
from subprocess import call as c
from time import sleep
com1c = 'git init' 
com2p = 'git status'
com3c = 'git add --all'
com4c = 'git commit -m "Done"'
com5c = 'git push ssh master'


p1 = c(com1c.split())

print "-------------------------------"

#sleep(2)
p2 = p(com2p.split())
p2.wait()

print "-------------------------------"

#sleep(2)
p3 = c(com3c.split())

print "-------------------------------"

#sleep(2)
p4 = c(com4c.split())

print "-------------------------------"

#sleep(2)
p5 = c(com5c.split())


if __name__ == '__main__':
	main()