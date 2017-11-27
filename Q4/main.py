# COMP 6901 Project Question 4

from MyDES import MyDES
from MyElgamal import MyElgamal
import json


def write_private_key(key):
    key_file = open("privatekey.dat", 'w')
    key_file.write(key)


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


def main():
    key = b'8bytekey'
    iv = MyDES.get_iv()
    des_obj = MyDES(key, iv)

    print "Random IV: " + iv

    prime = 7127

    el_obj = MyElgamal(prime)

    private_key = el_obj.gen_private_key(prime)

    print "Private Key: " + str(private_key)

    enc_private_key = des_obj.encrypt(plain_text=str(private_key))

    public_key = el_obj.get_public_key(private_key)

    print "Public Key:"
    print public_key

    print "Encrypted Private Key: " + enc_private_key

    write_private_key(enc_private_key)
    print("Wrote Pub Key to file")

    write_public_key(public_key)
    print("Wrote Encrypted Private Key to file")


    public_key = read_public_key()
    print "Read public key from file"
    print public_key

    el_obj2 = MyElgamal(public_key[1])
    plain_text = "Hi Trump"
    c = el_obj2.encrypt(plain_text, public_key)
    print "Cipher"
    print c

    iv = raw_input("Enter IV: ")
    key = raw_input("Enter Key: ")

    des_obj2 = MyDES(key, iv)
    enc_private_key = read_private_key()
    print "Read encrypted private key from file"
    private_key = int(des_obj2.decrypt(enc_private_key))
    print "Decrypted private key from "+enc_private_key + " to " + str(private_key)

    print "Decrypted Message: " + (el_obj.decrypt(c, private_key))


if __name__ == '__main__':
    main()
