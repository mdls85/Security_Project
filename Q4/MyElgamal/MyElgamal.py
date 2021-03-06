from Q4.MyMath import pow_mod, find_primitive, mul_inverse
import random


class MyElgamal:

    def gen_private_key(self, prime):
        return random.randint(1, prime - 2)

    def __init__(self, prime):
        self.prime = prime
        self.group = find_primitive(prime)
        # self.group = group

    def get_public_key(self, private_key):
            y = pow_mod(self.group, private_key, self.prime)
            return [self.group, self.prime, y]

    def encrypt(self, plain_text, public_key):
        group = public_key[0]
        prime = public_key[1]
        y = public_key[2]

        c_arr = []
        for p in plain_text:
            k = random.randint(1, 77)
            c1 = pow_mod(group, k, prime)
            c2 = int(pow_mod(pow(y, k)*ord(p), 1, prime))
            c_arr.append((c1, c2))
        return c_arr

    def decrypt(self, c_arr, private_key):
        plain_text = ""
        for (c1, c2) in c_arr:
            ck_inverse = mul_inverse(pow(c1, private_key), self.prime)
            plain_text += chr(pow_mod((c2 * ck_inverse), 1, self.prime))
        return plain_text
