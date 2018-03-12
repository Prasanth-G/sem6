import requests
from Crypto.Hash import SHA256

def hash_of(data):
    return SHA256.new(data).hexdigest()

#Registration phase
username = "prasanth"
password = "1234"

resp = requests.get(r'http://127.0.0.1:8001/registration/user=%s&pass=%s'%(username, password))
print(resp)

#Get Salt from server
resp1 = requests.get(r'http://127.0.0.1:8001/getsalt/user=%s'%username)
salt = resp1.text
print("Salt : ", salt)

#Get random Challenge
resp2 = requests.get(r'http://127.0.0.1:8001/getchallenge/user=%s'%username)
challenge = resp2.text.decode()
print("Challenge : ", challenge)

x = hash_of(password.encode('utf-8') + salt)
hkey = hash_of(x + str(challenge))
print("Hash Value : ", hkey)

#Send hkey to get authkey from server
print(str('http://127.0.0.1:8001/getauthkey/user=' + username + '&hkey='+ hkey))
resp3 = requests.get(str('http://127.0.0.1:8001/getauthkey/user=' + username + '&hkey='+ hkey))
authkey = resp3.text

print("Session Key : ", authkey)
