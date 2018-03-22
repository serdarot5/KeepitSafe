import os
import sqlite3 as sql
import getpass
from hashlib import md5  #will be change with sha-256 or sha-512 for security reasons in next commit
from Crypto import Random
from Crypto.Cipher import AES
username = getpass.getuser()
homedir = os.environ['HOME']
db=sql.connect(homedir+'/new/pass')
db.text_factory = str
link=db.cursor()
query = """CREATE TABLE IF NOT EXISTS passwords (service,username,password) """
link.execute(query)
query = """CREATE TABLE IF NOT EXISTS localuser (username,password) """ #Username and password information for Keep it Safe program.
link.execute(query)
query = "SELECT count(*) FROM localuser"
link.execute(query)
(length,)=link.fetchone()
if length==0:
    print"You are not registered with this user\n  "
    upassword = raw_input("Please enter new users password: ")
    hashed=md5(upassword).hexdigest()
    link.execute("insert into localuser (username,password) values( ? , ? )",(username,hashed))
    db.commit()
else:
    print"Welcome To Keep it Safe, Your Passwords encrypted with AES \n"
    upassword=raw_input("Enter Your Keep it Safe Password: ")
    link.execute("select password from localuser where username= ? " , (username,))
    (data,) = link.fetchone()
    login=False
    while(login==False):
        if(data==md5(upassword).hexdigest()):
            print("Login Successful")
            login=True
        else:
            upassword = raw_input("Your password is wrong please try again: ")
if (len(upassword) % 16 != 0):
    if len(upassword)<16: #will be moved to function
        limit=16-len(upassword)
    else:
        limit=len(upassword)-16
    for i in range(limit):
        upassword=upassword+" "
selection = 0
while(selection!=3):
    print"1-) Show login info \n2-) Enter new login info \n3-) Exit"
    selection=eval(raw_input("Please enter your selection: "))
    if(selection==1):
        link.execute("SELECT COUNT(*) FROM passwords")
        (length,) = link.fetchone()
        if(length==0):
            print"You don't have saved login info"
        else:
            link.execute("SELECT count(*) FROM passwords") #queries will be changed with query list or query variables
            (length,)=link.fetchone()
            link.execute("select * from passwords")
            for i in range(length):
                (service,username,password)=link.fetchone()
                for j in range(16):
                    iv=password[:16]
                cipher = AES.new(upassword, AES.MODE_CBC, iv)
                password=cipher.decrypt(password[16:]) 
                print str(i+1)+".  Service: "+service+"  Username: "+username+"  Password: "+password
    elif(selection==2):
        service=raw_input("service name: ")
        username=raw_input("Username: ")
        password=raw_input("Password: ")
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(upassword, AES.MODE_CBC, iv)
        if(len(password)%16!=0):
            if len(password)<16: #will be moved to function
                limit=16-len(password)
            else:
                limit=len(password)-16
            for i in range(limit):
                password=password+" "
        cipherpassword=cipher.encrypt(password)
        link.execute("insert into passwords values( ? , ? , ? )",(service,username,iv+cipherpassword))
        db.commit()
        print"Your Login Info Has Been Saved"

db.close()
