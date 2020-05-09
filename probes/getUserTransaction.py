#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'getUserTransaction' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER uid
#  2. STRING txnType
#  3. STRING monthYear
#
#  https://jsonmock.hackerrank.com/api/transactions/search?txnType=
#

def getUserTransaction(uid, txnType, monthYear):
    # Write your code here

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    uid = int(input().strip())

    txnType = input()

    monthYear = input()

    result = getUserTransaction(uid, txnType, monthYear)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
