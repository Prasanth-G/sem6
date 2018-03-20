import fractions
import random

class RSA:
    def __init__(self, p, q):
        self.n = p * q
        self.pi_n = (p-1) * (q - 1)
        self.co_prime = [i for i in range(2, self.pi_n) if fractions.gcd(i, self.pi_n) == 1]
        self.e = random.choice(self.co_prime)

        for i in range(self.pi_n, 2, -1):
            if ((i * self.e) % self.pi_n) == 1:
                self.d =  i
                break
        print(self.n, self.d, self.e)
    
    def reconfigure(self, e):
        if e not in self.co_prime:
            return None
        self.e = e
        for i in range(self.pi_n, 2, -1):
            if ((i * self.e) % self.pi_n) == 1:
                self.d =  i
                break

    def encrypt_(self, list_num):
        return [ (each**self.e) % self.n for each in list_num]

    def encrypt(self, text):
        return self.encrypt_([(ord(letter) - 97) for letter in text.lower()])
    
    def decrypt_(self, list_num):
        return [ (each**self.d) % self.n for each in list_num]

    def decrypt(self, cipher):
        return "".join([chr(number + 97) for number in self.decrypt_(cipher)])

def generate_primes(n):
    prime = [True for i in range(n+1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * 2, n+1, p):
                prime[i] = False
        p += 1
    return [p for p in range(2, n) if prime[p]]


def cyclic_attack(encryption_function, n, cipher):
    curr_cipher = cipher
    for i in range(n):
        prev_cipher = curr_cipher
        curr_cipher = encryption_function(curr_cipher)
        if curr_cipher == cipher:
            return "".join([chr(each + 97) for each in prev_cipher])

def factorization(n, e, cipher):
    prime_upto_n = generate_primes(n)
    for each_prime in prime_upto_n:
        if (n % each_prime) == 0:
            p = each_prime
    q = n//p
    pi_n = (p-1)*(q-1)
    for i in range(pi_n, 2, -1):
        temp = (i * e) % pi_n
        if temp == 1:
            d = i
    return "".join([chr(((each**d) % n) + 97) for each in cipher])

def chosen_cipher_text(decrypt, encrypt, n, cipher):
    my_msg = [2]
    my_cipher = encrypt(my_msg)    
    new_cipher = [(each * my_cipher[0]) % n for each in cipher]
    P = decrypt(new_cipher)
    return "".join([chr(((each // my_msg[0]) % n) + 97) for each in P])

def broadcast(a, cipher):
    pass


rsa = RSA(59, 17)

# cyclic attack
plain_text = cyclic_attack(rsa.encrypt_, rsa.n, rsa.encrypt("plaintext"))
print(plain_text)

# factorization
plain_text = factorization(rsa.n, rsa.e, rsa.encrypt("plaintext"))
print(plain_text)

# chosen cipher text
def decrypt_otherthan_plaintext(cipher):
    if cipher != rsa.encrypt("plaintext"):
        return rsa.decrypt_(cipher)
    return None

plain_text = chosen_cipher_text(decrypt_otherthan_plaintext, rsa.encrypt_, rsa.n, rsa.encrypt("plaintext"))
print(plain_text)

# broadcast 
# e = 1237
# p = 59, q = 233, d = 2317, n = 13747
# p = 53, q = 331, d = 1237, n = 17543
# p = 451, q = 193, d = 21373, n = 87043
e = 1237
rsa1 = RSA(59, 233)
rsa1.reconfigure(e)
rsa2 = RSA(53, 331)
rsa2.reconfigure(e)
rsa3 = RSA(451, 193)
rsa3.reconfigure(e)

a1 = rsa1.encrypt("plaintext")
a2 = rsa2.encrypt("plaintext")
a3 = rsa3.encrypt("plaintext")
print(a1,a2,a3)

a1 = [(ord(each)**e) % rsa1.n for each in "plaintext"]
a2 = [(ord(each)**e) % rsa2.n for each in "plaintext"]
a3 = [(ord(each)**e) % rsa3.n for each in "plaintext"]

M = rsa1.n * rsa2.n * rsa3.n
M1 = M // rsa1.n
M2 = M // rsa2.n
M3 = M // rsa3.n

for i in range(rsa1.n, 2, -1):
    if ((i * M1) % rsa1.n) == 1:
        M1inv = i
        break
for i in range(rsa2.n, 2, -1):
    if ((i * M2) % rsa2.n) == 1:
        M2inv = i
        break
for i in range(rsa3.n, 2, -1):
    if ((i * M3) % rsa3.n) == 1:
        M3inv = i
        break
#print(M1, M1inv, M2, M2inv, M3, M3inv)
#print(rsa1.n, rsa2.n, rsa3.n)
print(a1,a2,a3)
p_e = [((a1[i] * M1 * M1inv) + (a2[i] * M2 * M2inv) + (a3[i] * M3 * M3inv) ) % M for i in range(len(a1))]
print("PE", p_e)
print([each**(1/e) for each in p_e])
#print([ ((ord(i)-97) ** e) for i in "plaintext"])