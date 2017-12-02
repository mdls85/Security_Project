# COMP 6901 Project Question 4
import sys

from MyDES import MyDES
from MyElgamal import MyElgamal

prime = 7127


def write_cipter(c):
    cfile = open("cipher.dat", "w")
    for item in c:
        cfile.write(str(item[0])+"\n")
        cfile.write(str(item[1])+"\n")
    cfile.close()


def read_cipher():
    cfile = open("cipher.dat", "r")
    words = cfile.readlines()
    c = []
    for i in range(0, len(words)-1, 2):
        c.append((int(words[i]), int(words[i+1])))
    return c


def write_private_key(key):
    key_file = open("privatekey.dat", 'w')
    key_file.write(key)
    key_file.close()


def read_private_key():
    return open("privatekey.dat", 'r').read()


def write_public_key(key):
    pub_file = open("publickey.dat", "w")
    for item in key:
        pub_file.write(str(item)+"\n")


def read_public_key():
    with open("publickey.dat", "r") as g:
        arr = g.readlines()
    return [int(arr[0]), int(arr[1]), int(arr[2])]


def generate_keys(key):
    global prime
    if key is 'nil' or len(key) != 8:
        raise ValueError("Incorrect password size!")
    iv = MyDES.get_iv()
    des_obj = MyDES(key, iv)

    print "Random IV: " + iv
    el_obj = MyElgamal(prime)

    private_key = el_obj.gen_private_key(prime)

    print "Private Key: " + str(private_key)
    enc_private_key = des_obj.encrypt(plain_text=str(private_key))

    public_key = el_obj.get_public_key(private_key)

    print "Public Key:"
    print public_key

    print "Encrypted Private Key: " + enc_private_key

    write_private_key(enc_private_key)
    print("Wrote Pub Key to file privatekey.dat")

    write_public_key(public_key)
    print("Wrote Encrypted Private Key to file publickey.dat")


def encrypt(plain_text):
    public_key = read_public_key()
    print "Read public key from file"
    print public_key
    el_obj2 = MyElgamal(public_key[1])
    c = el_obj2.encrypt(plain_text, public_key)
    print "Cipher"
    print c
    write_cipter(c)
    print "Cipher Written to file"


def decrypt():
    global prime
    el_obj2 = MyElgamal(prime)
    c = read_cipher()
    print ("Cipher Read from file")
    print(c)

    iv = raw_input("Enter IV: ")
    key = raw_input("Enter Key: ")

    des_obj2 = MyDES(key, iv)
    enc_private_key = read_private_key()
    print "Read encrypted private key from file"
    private_key = int(des_obj2.decrypt(enc_private_key))
    print "Decrypted private key from " + enc_private_key + " to " + str(private_key)

    print "Decrypted Message: " + (el_obj2.decrypt(c, private_key))


def main():

    options = {
        'generate-keys': lambda arg: generate_keys(arg),
        'encrypt': lambda arg: encrypt(arg),
        'decrypt': lambda arg: decrypt()
    }

    num_args = len(sys.argv)
    try:
        if num_args == 1:
            print("No arguments supplied! run with flags generate-keys {password}, encrypt {message}, decrypt")
        else:
            if sys.argv[1] in options:
                argm = "nil" if num_args < 3 else sys.argv[2]
                options[sys.argv[1]](argm)  # fancy switch workaround
            else:
                print('invalid option')
    except ValueError:
        print("Bad password, IV or arguments supplied")


if __name__ == '__main__':
    main()
