import math


# calculates x ^ y mod z
def pow_mod(x, y, z):
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number


def trial_division(n):

    for i in range(2, int(math.sqrt(n)+1)):
        if n % i == 0:
            return False
    return True


def find_primitive(n):
    if not trial_division(n):
        return -1

    phi = n - 1
    factors = get_prime_factors(phi, fermat_method)

    for i in range(2, phi + 1):
        flag = False
        for factor in factors:
            if pow_mod(i, int(phi / factor), n) == 1:
                flag = True
                break
        if not flag:
            return i


def get_prime_factors(n, is_prime):
    res = []
    for i in range(2, int(math.sqrt(n)+1)):
        if n % i == 0:
            if is_prime(i):
                res.append(i)
                if i != n/i and is_prime(n/i):
                    res.append(n/i)
    return res


def mul_inverse(a, p):
    return pow_mod(a, p-2, p)


def fermat_method(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    a = math.ceil(math.sqrt(n))
    b2 = a*a - n
    while not math.sqrt(b2).is_integer():
        a = a + 1
        b2 = a*a - n
    return (a - math.sqrt(b2)) == 1 # if fermats method returns 1 then number is prime