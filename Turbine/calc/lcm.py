from __future__ import division
from past.utils import old_div
from fractions import gcd


def lcm(a, b):
    return old_div(abs(a * b), gcd(a, b))


def lcm_list(l):
    lcm_v = l[0]
    for i in l[1:]:
        lcm_v = lcm(i, lcm_v)
    return lcm_v
