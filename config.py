'''
HOST = the server to run against.  Format must be in 'https://364-ova02.domain.com/'
USER = This is the primary user that will be used.  This user and other users are setup with 'addUsers.py' and 'ldap.p'
SOURCE = this is used to set the source box on several import UIs.  Not important what the string is.
LONGRUN = will add a 20 min pause between method runs in each of the setup scripts.  this is used to
WEBDRIVER = Defines which browser will be used across all setup scripts
'''
import subprocess

class CONFIG:

    username = 'clint.hart'

    hostname = 'te-23096'  #Used by setup script to install collection service

    waittime = 4

    graphhost = ["te-22257"]   # use for python server metric collection and graphing

    if '.' in hostname:
        server = hostname
    else:
        server = '%s.domain.com' % hostname.lower()


    HOST = 'https://' + server + '/'             # Used primarily for all scripts

    TIEHOST = 'https://upgrade01.domain.com/'   # Used in ExportCSV.py

    TQUSER = ['user@domain.com', 'ChangeMePlease!']   # Mainly used for initial login and ldap.py setup

    USER = ['user@domain.com', 'ChangeMePlease!']  #Default TQ system user

    users = [
             ["Adversary Reader", "ChangeMePlease!", "user1@domain.com", "Administrative Access", "Adversary Reader Process"],
             ["read-only", "ChangeMePlease!", "user2@domain.com", "Read Only Access", "Wannacry Incident"]
            ]

    SOURCE = 'Jack Reacher'                              # used to set the source text in the scripts

    LONGRUN = False                           # If you wish to add 20 min wait to test auto logout.

    WEBDRIVER = 'Chrome'                  # Chrome or Firefox are the possible values here.

    MYSQLROOT = 'thisismySQLrootpassword'
