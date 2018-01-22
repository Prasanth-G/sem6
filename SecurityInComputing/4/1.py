'''
Constraints : 
    Lenght - 4, contains only first n lowercase letters
'''

import string
import itertools
import random
from Crypto.Hash import SHA256
import base64
import re

n = 4
n_lower = 5
n_times_hashed = 10


def hashof(x):
    return SHA256.new(x.encode()).hexdigest()

def reduced_str(h):
    return "".join([chr(ord(each)%n_lower + 97) for each in h.lower()[:n_lower]])

characters = [each for each in string.ascii_lowercase[:n_lower]]
all_per = list(itertools.permutations(characters, n))

no_of_entries_in_rainbow_tbl = int(0.5 * len(all_per))
rand_per = ["".join(list(each)) for each in random.choices(all_per, k = no_of_entries_in_rainbow_tbl)]
rainbow_table = {}

for item in rand_per:
    each = item
    h = hashof(item)
    for i in range(n_times_hashed):
        # hash may contains other than a-e ("allowed character")
        item = reduced_str(h)
        h = hashof(item)
        #print(item, " ", h)
    rainbow_table[h] = "".join(list(item))


hash_value = '11a92b734c0469ea19fe6a44a1b7db7618aa41908ad846181016ddc55e5a0a68'
temp_hash = hash_value

for i in range(1000):
    if hash_value in rainbow_table:
        key = rainbow_table[hash_value]
        break
    rs = reduced_str(hash_value)
    hash_value = hashof(rs)

print("Key : ", key, " ", hash_value)
for i in range(n_times_hashed+100):
    hash_value = hashof(key)
    print(key, " ", hash_value)
    key = reduced_str(hash_value)


# baade acbce   11a92b734c0469ea19fe6a44a1b7db7618aa41908ad846181016ddc55e5a0a68