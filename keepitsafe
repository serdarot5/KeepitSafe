#!/usr/bin/python2.7
import os
import sqlite3 as sql
import getpass
import sys
from hashlib import md5
from Crypto import Random
from Crypto.Cipher import AES

def KeyPadding(key):
    if len(key)<16:
        limit=16-len(key)
    elif len(key)<24:
        limit=len(key)-24
    elif len(key)<32: #User Passwords can be within 8-32 characters
        limit=len(key)-32
    for i in range(limit):
        key=key+" "
    return key

def InputPadding(text):
    limit =16-(len(text)%16)
    for i in range(limit):
        text = text + " "
    return text

def LogInToProgram(link,username,uPassword):

        link.execute("select password from localuser where username= ? ", (username,))
        (data,) = link.fetchone()
        if (data == md5(uPassword).hexdigest()):
            print("Login Successful\n")
            return True
        else:
            return False

def ShowLoginInfo(link,id,key):
    link.execute("SELECT COUNT(*) FROM passwords")
    (length,) = link.fetchone()
    if (length == 0):
        sys.exit("You don't have saved login info")
    else:
        if (len(key) % 16 != 0):
            key = KeyPadding(key)
        link.execute("SELECT count(*) FROM passwords where u_id= ? ",(id,))
        (length,) = link.fetchone()
        link.execute("select * from passwords")
        print("Your passwords kept safe with keepitsafe")
        for i in range(length):
            (service, username, password,id) = link.fetchone()
            iv = password[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            password = cipher.decrypt(password[16:])
            print "Record Number: "+str(i + 1) + "  Service: " + service + "  Username: " + username + "  Password: " + password

def ShowDelUpdateInfo(link,id):
    link.execute("SELECT COUNT(*) FROM passwords")
    (length,) = link.fetchone()
    if (length == 0):
        sys.exit("You don't have saved login info")
    else:
        link.execute("SELECT count(*) FROM passwords where u_id= ? ",(id,))
        (length,) = link.fetchone()
        link.execute("select * from passwords")
        for i in range(length):
            (service, username, password,id) = link.fetchone()
            print "Record Number: "+str(i + 1) + "  Service: " + service + "  Username: " + username

def NewLoginInfo(link,id,uPassword):
    service = raw_input("Service name: ")
    username = raw_input("Username: ")
    password = getpass.getpass(prompt='Password: ')
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(uPassword, AES.MODE_CBC, iv)
    if (len(password) % 16 != 0):
        password = InputPadding(password)
    cipherpassword = cipher.encrypt(password)
    link.execute("insert into passwords values( ? , ? , ?, ? )", (service, username, iv + cipherpassword, id))
    db.commit()
    print"Your Login Info Has Been Saved"

def NewUser(link,username,uPassword):
    hashed = md5(uPassword).hexdigest()
    link.execute("select count(*) from localuser ")
    (id,) = link.fetchone()
    link.execute("insert into localuser (id,username,password) values( ?, ? , ? )", (id, username, hashed))
    db.commit()
def GetId(link,username):
    link.execute("select id from localuser where username=?", (username,))
    (id,) = link.fetchone()
    return id
def DeleteLoginInfo(link,id):
    selection=eval(raw_input("Enter the record number you want to delete: "))
    link.execute("SELECT count(*) FROM passwords where u_id= ? ", (id,))
    (length,)=link.fetchone()
    if selection>length:
        sys.exit("Record number you've entered is higher than saved login info count")
    elif(selection<=0):
        sys.exit("Wrong record number")
    else:
        link.execute("select * from passwords where u_id=?",(id,))
        i=0
        while(i<selection):
            (s,u,p,u_id)=link.fetchone()
            i=i+1
        link.execute("delete from passwords where service=? and username=? and password=? and u_id=?",(s,u,p,u_id))
        db.commit()
def UpdateLoginInfo(link,id,uPassword):
    selection = eval(raw_input("Enter the record number you want to update: "))
    link.execute("SELECT count(*) FROM passwords where u_id= ? ", (id,))
    (length,) = link.fetchone()
    if selection > length:
        sys.exit("Record number you've entered is higher than saved login info count")
    elif (selection <= 0):
        sys.exit("Wrong record number")
    else:
        link.execute("select * from passwords where u_id=?",(id,))
        i=0
        while(i<selection):
            (s,u,p,u_id)=link.fetchone()
            i=i+1
        service = raw_input("Service name: ")
        username = raw_input("Username: ")
        password = getpass.getpass(prompt='Password: ')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(uPassword, AES.MODE_CBC, iv)
        if (len(password) % 16 != 0):
            password = InputPadding(password)
        cipherpassword = cipher.encrypt(password)
        link.execute("update passwords set service=? , username=?, password=? where service=? and username=? and password=? and u_id=?", (service,username,iv+cipherpassword,s, u, p, u_id))
        db.commit()
        print"Your Login Info Has Been Saved"


username = getpass.getuser()
homedir = os.environ['HOME']
db=sql.connect(homedir+'/.pass')
db.text_factory = str
link=db.cursor()
link.execute("CREATE TABLE IF NOT EXISTS passwords (service,username,password,u_id) ") #Username and password information stored in Keep it Safe program.
link.execute("CREATE TABLE IF NOT EXISTS localuser (id,username,password) ") #Local Username and passwords information
if(len(sys.argv)==1):
    print "You must run the program with parameters check keepitsafe -h"
elif(len(sys.argv)>2):
    print "Too many parameters check keepitsafe -h"
elif sys.argv[1]=="-h":
    sys.exit("-s for show all login info you've saved \n-n for enter new login info\n-d for delete login info you've saved \n-u for update login info you've saved")
else:
    link.execute("SELECT count(*) FROM localuser where username=?", (username,))
    (length,) = link.fetchone()
    if length == 0:
        print "You are not registered with this user\n  "
        uPassword = getpass.getpass(prompt='Please enter new users password: ')
        while(len(uPassword)>32):
            uPassword = getpass.getpass(prompt='Your password can not be longer than 32 characters\nPlease enter new users password:' )
        NewUser(link,username,uPassword)
    else:
        print"Welcome To Keep it Safe, Your Passwords encrypted with AES \n"
        uPassword = getpass.getpass(prompt='Enter Your Keep it Safe Password: ')
        session = LogInToProgram(link,username,uPassword)
        while (session == False):
            uPassword = getpass.getpass(prompt='Your password is wrong please try again:')
            session = LogInToProgram( link,username, uPassword)
    id = GetId(link, username)
    if (len(uPassword)%16!=0):
        uPassword=KeyPadding(uPassword)
    if sys.argv[1]=="-s":
        ShowLoginInfo(link,id,uPassword)
    elif sys.argv[1] == "-n":
        NewLoginInfo(link,id,uPassword)
    elif sys.argv[1] == "-d":
        ShowDelUpdateInfo(link, id)
        DeleteLoginInfo(link,id)
    elif sys.argv[1] == "-u":
        ShowDelUpdateInfo(link, id)
        UpdateLoginInfo(link,id,uPassword)

    else:
        print "Wrong Parameter Check keepitsafe -h"

db.close()
