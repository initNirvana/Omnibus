"""
1. n을 입력한다.
2. 집합 {1,2,3, ... , n-1}에서 무작위로 m까지의 정수 w1, w2, ... ,wm을 선택한다.
3. wi가 증거를 가지고 있는지 테스트 한다.
4. 정수 m에 증거가 없다면 출력을 yes로 없다면 no를 출력

합성수인지 확인해주는 증거 w의 조건

1. w^{n-1} != mod n 
2. m = \frac{n-1}{2^k} is integer, 1 < gcd(w^m, n) < n

"""

def composite(a,d,n,s):
    """
    pow(2,5)는 2의 5승
    pow(2,5,2)는 2의 5승을 2로 나눈 나머지
    """
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True

def is_prime(n):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0

    while not d % 2:
        d, s = d >> 1, s + 1

    if n < 1373653:
        return not any(composite(a,d,n,s) for a in (2, 3))

if __name__ == "__main__":
    _known_primes = [2, 3]
    _known_primes += [x for x in range(5, 500, 1) if is_prime(x)]
    print(_known_primes)

    
