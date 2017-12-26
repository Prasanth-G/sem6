import requests
import itertools

url = "http://127.0.0.1:9000/user=%s&passwd=%s"
username = "hello"

password_length = 4
character_in_password = range(0,10)

for each in itertools.product(character_in_password, repeat = password_length):
    passwd = "".join(map(str, each))
    print(passwd, end=", ")
    resp = requests.get(url%(username, passwd))
    if resp.status_code == 200:
        print("\nThe Password is ", passwd)
        print(resp.text)
        break