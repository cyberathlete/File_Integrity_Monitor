import os
import platform
import hashlib
import datetime
import time
from colorama import init, Fore, Back

init(autoreset = True)

def hashFile(file):
	h = hashlib.sha1()
	with open(file, 'rb') as f:
		while True:
			data = f.read(65536)
			if not data:
				break
			h.update(data)
	hash = h.hexdigest()
	return(file,hash)

def AddFiles(file):
	
	path,hash = hashFile(file)
	with open('baseLine.txt', 'a') as f:
		f.write(path + '|' + hash + '\n')

def Monitor():
	while True:
		with open('baseLine.txt', 'r') as f:
			lines = f.readlines()
		for l in lines:
			l = l.replace('\n','')
			if(l == ''):
				continue
			path,hash = l.split('|')
			if(not os.path.exists(path)):
				print(f"{Fore.RED}{Back.YELLOW}File" + path + " has been deleted at " + str(datetime.datetime.now()))
				with open('baseLine.txt', 'w') as f:
					for line in lines:
						if(line.strip('\n')) != l:
							f.write(line)
				continue
			p,h = hashFile(path)
			if(h != hash):
				print(f'{Fore.RED}{Back.YELLOW}File' + path + ' has been modified at ' + str(datetime.datetime.now()))
				with open('baseLine.txt', 'w') as f:
					for line in lines:
						if(line != '\n'):
							if(line.strip('\n')) != l:
								f.write(line + '\n')
							else:
								new_hash = line.split('|')
								np, nh = hashFile(new_hash[0])
								f.write(np + '|' + nh + '\n')
		time.sleep(10)

def dirChecker(file):
	if platform.system() == 'windows':
		slash = '\\'
	else:
		slash='/'
	if(not os.path.exists('baseLine.txt')):
		file = open('baseLine.txt','w')
	if(not os.path.exists(file)):
		print("\n" + file + " doesn't exist\n\n")
		print("\t press enter to continue")
		input()
		os.system("clear")
	
	if(os.path.isfile(file)):
		AddFiles(file)
	else:
		if(not file[-1] == slash):
			file = file + slash
		dirList = os.listdir(file)
		for d in dirList:
			if(os.path.isdir(file + d)):
				dirChecker(file + d+slash)
			else:
				AddFiles(file + d)

def Start():
	print("\t1) Add Files/Directories to monitor")
	print("\t2) Start monitoring files")
	choice = input(">")
	if(choice == '1'):
		file = input('Enter the file path >')
		dirChecker(file)
	elif(choice == '2'):
		Monitor()
	else:
		os.system("clear")
		print("Please select a correct option")
		input()
		os.system("clear")
		start()
		
Start()
