from math import factorial

def comb(n: int, k: int) -> float:
    """Return the binomial coefficient (n, k)"""
    return factorial(n) / factorial(k) / factorial(n-k)

def der(m: int) -> float:
    """Return the number of derangements of m items"""
    s = 0
    for x in range(m+1):
        s += (-1)**x / factorial(x)
    return factorial(m) * s

def prob_fixed_points(n: int, k: int) -> float:
    """Return the probability that there are k fixed points in a permutation of n items"""
    return comb(n, k) * der(n-k) / factorial(n)

def prob_fixed_points_less_than(n: int, k: int) -> float:
    """Return the probability that there less than k fixed points in a permutation of n items"""
    p = 0
    for x in range(k):
        p += prob_fixed_points(n, x)
    return p

def ensure_prob(n: int, p: float) -> int:  
    """
    Find the smallest integer k such that the probability of having less than k fixed points
    in a permutation of n items is greater than p
    """
    for k in range(n+2):
        if prob_fixed_points_less_than(n, k) > p:
            return k
        