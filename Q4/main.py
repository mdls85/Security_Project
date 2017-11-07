# COMP 6901 Project

from MyMath import pow_mod
from MyDES import MyDES



def main():
    key = b'8bytekey'
    iv = MyDES.get_iv()
    des_obj = MyDES(key, iv)
    print des_obj.decrypt(des_obj.encrypt(plain_text="hello"))


if __name__ == '__main__':
    main()
