import fractions
import random

class RSA:
    def __init__(self, p, q):
        self.n = p * q
        self.pi_n = (p-1) * (q - 1)
        # find e
        co_prime = [i for i in range(2, self.pi_n) if fractions.gcd(i, self.pi_n) == 1]
        self.e = random.choice(co_prime)

        for i in range(self.pi_n, 2, -1):
            temp = (i * self.e) % self.pi_n
            if temp == 1:
                self.d =  i
        print(self.n, self.d, self.e)

    def encrypt_(self, list_num):
        return [ (each**self.e) % self.n for each in list_num]

    def encrypt(self, text):
        return self.encrypt_([(ord(letter) - 97) for letter in text.lower()])
    
    def decrypt_(self, list_num):
        return [ (each**self.d) % self.n for each in list_num]

    def decrypt(self, cipher):
        return "".join([chr(number + 97) for number in self.decrypt_(cipher)])

r = RSA(59, 17)
cipher = r.encrypt("prasanth")
#print("Cipher : ", cipher)
#print("Text : ", r.decrypt(cipher))
c = cipher
for i in range(r.n):
    prev = c
    c = r.encrypt_(c)
    if c == cipher:
        print("Text : ", "".join([chr(each + 97) for each in prev]))
        break
    