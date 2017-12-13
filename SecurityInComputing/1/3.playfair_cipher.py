import string
import collections

def encrypt(msg, key):
    key = key.lower()
    msg = msg.lower()
    key_table, index = create_key_table(key)
    print(key_table)
    msg = replace_duplicates(msg)
    cipher = ""
    for pair in msg:
        x1, y1 = index[pair[0]]
        x2, y2 = index[pair[1]]
        #same column
        if y1 == y2:
            x1 = (x1 + 1) % 5
            x2 = (x2 + 1) % 5
        #same row
        elif x1 == x2:
            y1 = (y1 + 1) % 5
            y2 = (y2 + 1) % 5
        #forms a rectangle
        else:
            y1, y2 = y2, y1
        cipher = cipher + key_table[x1][y1] + key_table[x2][y2]
    return cipher

def create_key_table(key):
    key_list = list(reversed(key))
    key_table = [[None for i in range(5)] for j in range(5)]
    added = collections.OrderedDict([(each, False) for each in string.ascii_lowercase])
    index = {}
    i = 0
    j = 0
    while key_list:
        element = key_list.pop()
        if not added[element]:
            key_table[i][j] = element
            index[element] = (i, j)
            added[element] = True
            if element == 'i':
                added['j'] = True
            j = j + 1
            if j == 5:
                i = i + 1
                j = 0
    for each in added:
        if not added[each]:
            key_table[i][j] = each
            index[each] = (i, j)
            j = j + 1
            if j == 5:
                i = i + 1
                j = 0
    return (key_table, index)

def replace_duplicates(msg):
    #Replacing duplicates with x
    prev = msg[0]
    m = prev
    for i in range(1, len(msg)):
        if prev == msg[i]:
            m = m + "x" + msg[i]
        else:
            m = m + msg[i]
        prev = msg[i]
    msg = []
    for each in [m[i:i+2] for i in range(0, len(m), 2)]:
        if len(each) == 2:
            if each[0] == each[1]:
                msg.append(each[0] + "x")
            else:
                msg.append(each[0]+each[1])
        else:
            msg.append(each + "x")
    return msg

if __name__ == "__main__":
    file = open("plaintext.txt")
    key = file.readline().lower().strip("encipher").strip(" \n")
    msg = "".join([letter for letter in file.read().lower() if letter.isalpha()])
    
    #key = "playfairexample"
    #msg = "Hidethegoldinthetreestump"

    tcipher = encrypt(msg, key)
    cipher = ""
    count = 0
    for each in [tcipher[i:i+5] for i in range(0, len(tcipher),5)]:
        cipher = cipher + " " + each
        count = count + 1
        if count%10 == 0:
            cipher = cipher + "\n"
            count = 0

    print("Mesage :", msg)
    print("Cipher :", cipher)