from nltk import words
import affine_cipher

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

possible_a = []
for i in range(26):
    gcd_value = gcd(i, 26)
    if gcd_value == 1:
        possible_a.append(i)

for b in range(0, 26):
    for a in possible_a:
        print("".join(affine_cipher.decrypt("OYHYJLEVYQBLSRIJLYEC", a, b)))

#ANS : CELEBRATE SPRING BREAK
#UPDATE - AUTOMATE FINDING MEANINGFUL SENTENCE
en_words = words.words()
s = "CELEBRATESPRINGBREAK"
start = 0
end = 1

def is_a_sentence(inp):
    if inp[start:end] in en_words:
        start = end
        end = end + 1
    else:
        end = end + 1