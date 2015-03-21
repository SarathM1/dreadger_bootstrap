#!/usr/bin/python
from subprocess import call as c

def main():
	com1c = "git remote add ssh https://github.com/SarathM1/dreadger_bootstrap.git"


	c(com1c.split())

if __name__ == '__main__':
	main()