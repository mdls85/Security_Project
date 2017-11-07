from Q4.MyMath import pow_mod, find_primitive
import random


class MyElgamal:

    def __init__(self, prime):
        self.prime = prime
        self.group = find_primitive(prime)
        self.private_key = random.randint(1, prime-2)
        self.public_key = {self.group, self.prime, pow_mod(self.group, self.private_key, self.prime)}

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def encrypt(self, plain_text):
        k = random.randint(1, 77)
        c1 = pow_mod(self.group, k, self.prime)

    def decrypt(self, cipher_text):
        print "packet switching"