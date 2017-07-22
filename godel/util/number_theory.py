from math import sqrt


def prime_smaller(n):
    """
    받은 매개변수보다 적은 소수를 리턴
    """
    if n < 2 : return []

    lng = int((n / 2) - 1 + n % 2) # 짝수 제거 
    sieve = [True] * (lng + 1)  

    for i in range(int(sqrt(n)) >> 1):
        if not sieve[i]: continue
        for j in range( (i * (i + 3) << 1) + 3, lng, (i << 1) + 3):
            sieve[j] = False

    primes = [2] + [(i << 1) + 3 for i in range(lng) if sieve[i]]
    return primes


def factor(n):
  factor = 2
  factors = []
  while factor <= n:
    if n % factor == 0:
      n //= factor
      factors.append(factor)
    else:
      factor += 1
  return factors
