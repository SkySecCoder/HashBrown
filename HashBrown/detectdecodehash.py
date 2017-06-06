#!/usr/bin

import optparse
import sys
import zipfile
import crypt
from termcolor import colored

def main():
	parser = optparse.OptionParser("usage %prog -f <zipfile> -d <dictionary>")
	parser.add_option('-f', dest='zname', type='string',help='Specify zip file')
	parser.add_option('-d', dest='dname', type='string',help='Specify dictionary file')
	(options, args) = parser.parse_args()
	if (options.dname == None) | (options.zname ==None):
		#makeBanner("HashBrown");
		print "1. Hash breaking.\n2. Generate hash\n3. Extract Zip file"
		choice=raw_input("Enter your choice(1-3): ")
		if str(choice)=="1":	
			filename=raw_input("Enter the file that contains user's name and hashes: ")	
			file=open(filename,"r")
			for list in file.readlines():
				user=list.split(":")[0]
				hash = list.strip(user+":")
				#hash=list.split(":")[1]
				#hash=hash.split(":")[0]
				crack(user,hash)
		elif str(choice)=="2":
			genHash()
		else:
			zipopener("test.zip","dictionary.txt")
	else:
		zname = options.zname
		dname = options.dname
		zipopener(zname,dname)
	print "\nThank you."

def zipopener(ftoopen,passfile):
	file=open(passfile,"r")
	for line in file.readlines():
		line=line.strip('\n')
		line=line.strip(" ")
		try:
			zfile=zipfile.ZipFile(str(ftoopen))
        		zfile.extractall(pwd=str(line))
			print "["+colored("+","green")+"] File successfully extracted with password "+colored(line,"green")
		except Exception,e:
			print "["+colored("-","red")+"] Error for password "+colored(line,"red")+": "+str(e)

def crack(user,hash):
	type=hash[1:2]
	salt=hash[0:11]
	hash1 = hash.strip("$"+type)
	hash1 = hash1.strip("$"+salt)
	filename="dictionary.txt"
	f=open(filename,"r")
	if str(type)=="6":
                print "This is SHA512"
	elif str(type)=="5":
		print"This is SHA256"
	elif str(type)=="2a":
		print "This is Blowfish"
	else:
		print "This is MD5"
	for word in f.readlines():
		word=word.strip("\n")
		word=word.strip(" ")
		#temp=hashlib.sha512(word).hexdigest()
		temp= crypt.crypt(word,salt)
		comp = str(temp)
		if comp in hash:
			print "["+colored("+","green")+"] Password match found for "+colored(user,"green")+": "+colored(word,"green")
			return
	print "["+colored("-","red")+"] Password match not found for "+colored(user,"red")

def genHash():
	salt = raw_input("Enter salt for your SHA512 hash(must be 8 characters): ")
	toHash = raw_input("Enter string to be hashed: ")
	Hash = crypt.crypt(toHash,("$6$"+salt))
	print "\nSalt used for your hash is: "+colored(salt,"green")
	print "Hashed string: "+colored(toHash,"green")
	print "Hash Value: "+colored(Hash,"green")

def makeBanner(name):
    i=j=0
    while j!= 15:
        if j==0 or j==14:
            while i != 40:
                if i==0:
                    print "*",
                elif i==39:
                    print "*"
                else:
                    print "=",
                i = i+1
        i = 0
        if j>0 and j<12:
            if j == 7:
                k = 30
            elif j == 6:
                k = 40 - len(name) + 5
            else:
                k = 40
            while i != k:
                if i == 0:
                    print "|",
                elif i == k-1:
                    print "|"
                elif i == k/2 and j == 7:
                    print "- by Aakash Prasad   ",
                elif i == k/2 and j == 6:
                    print name,
                else:
                    print " ",
                i = i + 1
        j = j + 1


if __name__=="__main__":
	main()
