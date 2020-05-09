#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'oddNumbers' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER l
#  2. INTEGER r
#

def oddNumbers(l, r):
    # Write your code here
    # arr_res = []
    # for i in range(l, r+1):
    #   if i % 2 != 0:
    #     arr_res.append(i)
    arr_res = [i for i in range(l, r+1) if i % 2 != 0]

    return arr_res

if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # l = int(input().strip())
    #
    # r = int(input().strip())

    l = 3
    r = 9
    result = oddNumbers(l, r)

    # fptr.write('\n'.join(map(str, result)))
    # fptr.write('\n')
    #
    # fptr.close()
