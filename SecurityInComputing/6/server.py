import SimpleHTTPServer
import BaseHTTPServer
import json
import re
import random
from Crypto.Hash import SHA256
import sys
import os

## user defined class
import challenge


if os.path.exists('user_database.db'):    
    file_ = open('user_database.db')
    database = json.loads(file_.read())
    print(database)

database = {}
challenge_ = challenge.AuthChallenge()
list_of_challenge = {}
session_key = {}

def hash_of(data):
    return SHA256.new(data).hexdigest()

userpassre = re.compile(r'user=(.*)&pass=(.*)')
class handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(database)
        if self.path.startswith('/registration'):
            username, password = userpassre.findall(self.path)[0]
            if username not in database:
                salt = str(random.random())
                database[username] = (hash_of(password.encode('utf-8') + salt) ,salt)
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Registration success")
            else:
                print("User Already Exists ", username)
                self.send_response(400)
                self.end_headers()

        #Get Salt from the server
        elif self.path.startswith('/getsalt'):
            username = re.findall(r'user=(.*)', self.path)[0]
            if username in database:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(database[username][1])

        #Get a Challenge to authenticate
        elif self.path.startswith('/getchallenge'):
            username = re.findall(r'user=(.*)', self.path)[0]
            if username in database:
                list_of_challenge[username] = challenge_.random_challenge()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(list_of_challenge[username])

        #Authenticate user
        elif self.path.startswith('/getauthkey'):
            username, hkey = re.findall(r'user=(.*)&hkey=(.*)', self.path)[0]
            if username in database:
                genhkey = hash_of( database[username][0] + list_of_challenge[username])
                print("Received Hkey : ", hkey)
                print("Server Gen Hkey : ", genhkey)
                if hkey == genhkey:                        
                    session_key[username] = hash_of(str(random.randrange(0, sys.maxint)))
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(session_key[username])
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(400)
            self.end_headers()
        with open('user_database.db', 'w') as f:
            f.write(json.dumps(database))
        

s = BaseHTTPServer.HTTPServer(('', 8001), handler)
print('Server Up')
s.serve_forever()
