# COMP 6901 Project Question 4

from MyDES import MyDES
from MyElgamal import MyElgamal
import json


def write_to_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def read_from_file(filename):
    with open(filename) as json_data:
        return json.load(json_data)


def main():
    key = b'8bytekey'
    iv = MyDES.get_iv()
    des_obj = MyDES(key, iv)

    private_key = "26"

    enc_private_key = des_obj.encrypt(plain_text=private_key)

    # write_to_file("privatekey.dat", [enc_private_key])

    prime = 7127
    el_obj = MyElgamal(prime, int(private_key))

    public_key = el_obj.get_public_key()

    # enc_public_key = des_obj.encrypt(plain_text=key)

    # write_to_file("publickey.dat", [enc_public_key])

    plain_text = "Hi Trump"

    c = el_obj.encrypt(plain_text, public_key)

    print "decrypted message: " + el_obj.decrypt(c, int(private_key))


if __name__ == '__main__':
    main()
