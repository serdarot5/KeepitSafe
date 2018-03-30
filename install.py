import os,shutil,sys
workingDIR = os.path.dirname(os.path.realpath(__file__))
if os.getegid() != 0:
    sys.exit("You must run installation script with root privileges")
shutil.move(workingDIR + "/keepitsafe","/usr/bin/")
os.chmod("/usr/bin/keepitsafe",0550)
