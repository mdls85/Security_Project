from Crypto import Random
from Crypto.Cipher import DES


class MyDES:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    @staticmethod
    def get_iv():
        return Random.get_random_bytes(8)

    def encrypt(self, plain_text):
        return DES.new(self.key, DES.MODE_CFB, self.iv).encrypt(plain_text)

    def decrypt(self, cipher_text):
        return DES.new(self.key, DES.MODE_CFB, self.iv).decrypt(cipher_text)

