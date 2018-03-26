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
            print("Login Successful")
            return True
        else:
            return False

def ShowLoginInfo(link,id,key):
    link.execute("SELECT COUNT(*) FROM passwords")
    (length,) = link.fetchone()
    if (length == 0):
        print"You don't have saved login info"
    else:
        if (len(key) % 16 != 0):
            key = KeyPadding(key)
        link.execute("SELECT count(*) FROM passwords where u_id= ? ",(id,))
        (length,) = link.fetchone()
        link.execute("select * from passwords")

        for i in range(length):
            (service, username, password,id) = link.fetchone()
            iv = password[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            password = cipher.decrypt(password[16:])
            print str(i + 1) + ".  Service: " + service + "  Username: " + username + "  Password: " + password

def NewLoginInfo(link,id,uPassword):
    service = raw_input("service name: ")
    username = raw_input("Username: ")
    password = raw_input("Password: ")
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
if sys.argv[1]=="-h":
    print "-s for show all login info you've saved \n-n for enter new login info"
    sys.exit()
username = getpass.getuser()
homedir = os.environ['HOME']
db=sql.connect(homedir+'/new/pass')
db.text_factory = str
link=db.cursor()
link.execute("CREATE TABLE IF NOT EXISTS passwords (service,username,password,u_id) ") #Username and password information stored in Keep it Safe program.
link.execute("CREATE TABLE IF NOT EXISTS localuser (id,username,password) ") #Local Username and passwords information
if(len(sys.argv)==1):
    print "You must run the program with parameters check keepitsafe -h"
elif(len(sys.argv)>2):
    print "Too many parameters check keepitsafe -h"
else:
    link.execute("SELECT count(*) FROM localuser where username=?", (username,))
    (length,) = link.fetchone()
    if length == 0:
        print "You are not registered with this user\n  "
        uPassword = raw_input("Please enter new users password: ")
        NewUser(link,username,uPassword)
    else:
        print"Welcome To Keep it Safe, Your Passwords encrypted with AES \n"
        uPassword = raw_input("Enter Your Keep it Safe Password: ")
        session = LogInToProgram(link,username,uPassword)
        while (session == False):
            uPassword = raw_input("Your password is wrong please try again: ")
            session = LogInToProgram( link,userame, uPassword)
    id = GetId(link, username)
    if (len(uPassword)%16!=0):
        uPassword=KeyPadding(uPassword)
    if sys.argv[1]=="-s":
        ShowLoginInfo(link,id,uPassword)
    elif sys.argv[1] == "-n":
        NewLoginInfo(link,id,uPassword)
    else:
        print "Wrong Parameter Check keepitsafe -h"

db.close()
