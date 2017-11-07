# COMP 6901 Project Question 4

from MyMath import pow_mod, find_primitive
from MyDES import MyDES


def main():
    key = b'8bytekey'
    iv = MyDES.get_iv()
    des_obj = MyDES(key, iv)
    print des_obj.decrypt(des_obj.encrypt(plain_text="hello"))


if __name__ == '__main__':
    main()
