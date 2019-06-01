from __future__ import division
from past.utils import old_div
from math import gcd

import numpy as np

# def lcm(a, b):
#     return old_div(abs(a * b), gcd(a, b))
def lcm(a, b):
    np.lcm(np.int64(a), np.int64(b), dtype=int64)


def lcm_list(l):
    lcm_v = l[0]
    for i in l[1:]:
        lcm_v = lcm(i, lcm_v)
    return lcm_v
