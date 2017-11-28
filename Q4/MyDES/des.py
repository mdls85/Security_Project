import string
from Crypto.Cipher import DES
import random


class MyDES:

    def __init__(self, key, iv):
        if len(key) != 8 or len(iv) != 8:
            raise ValueError("Invalid Key/IV Size!")
        self.key = key
        self.iv = iv

    @staticmethod
    def get_iv():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    def encrypt(self, plain_text):
        return DES.new(self.key, DES.MODE_CFB, self.iv).encrypt(plain_text)

    def decrypt(self, cipher_text):
        return DES.new(self.key, DES.MODE_CFB, self.iv).decrypt(cipher_text)


# Usage
def main():
    key = b'8bytekey'
    iv = MyDES.get_iv()

    print "Random IV: " + iv
    des_obj = MyDES(key, iv)

    iv = raw_input("Enter IV: ")
    key = raw_input("Enter Key: ")

    try:
        des_obj2 = MyDES(key, iv)
        m = des_obj2.decrypt(des_obj.encrypt(plain_text="lol"))
        print m
    except ValueError:
        print "Invalid key/iv size given"


if __name__ == '__main__':
    main()
