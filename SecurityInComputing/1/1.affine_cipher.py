def decrypt(inp, a, b):
    cap = ord('A')
    sml = ord('a')
    return [chr((((26 -  a) * (ord(each) - cap - b)) % 26) + cap) if each.isupper() else chr((((26 - a) * (ord(each) - sml - b)) % 26) + sml) for each in inp]

def encrypt(inp, a, b):
    cap = ord('A')
    sml = ord('a')
    return [chr(((a * (ord(each) - cap) + b ) % 26) + cap) if each.isupper() else chr(((a * (ord(each) - sml) + b) % 26) + sml) for each in inp]

if __name__ == "__main__":
    
    '''
    inp = input("Cipher : ")
    a = int(input("A : "))
    b = int(input("B : "))
    '''
    c = decrypt("WZUSAAL", 5, 8)
    t = encrypt(c, 5, 8)
    print("Decryption of 'WZUSAAL'", c)
    print(t)