# Freddie He
# 1560733
# heyingge

# To run this code, run in this format: python3 hw7.py example.txt
# I used the index convention from the slides.

import sys
import time
import math
import random

Opt = None


def is_pair(base_0, base_1):
    if base_0 == 'A':
        return base_1 == 'U'
    elif base_0 == 'U':
        return base_1 == 'A'
    elif base_0 == 'C':
        return base_1 == 'G'
    elif base_0 == 'G':
        return base_1 == 'C'


def traceback(i, j, seq):
    if j == i:
        return '.'
    elif j < i:
        return ''
    elif Opt[i][j] == Opt[i][j-1]:
        return traceback(i, j-1, seq) + '.'
    else:
        for t in range(i, j-4):
            if is_pair(seq[t], seq[j]):
                if (t == 0 and Opt[i][t-1] + Opt[t+1][j-1] + 1) or (t != 0 and Opt[t+1][j-1] + 1):
                    return traceback(i, t-1, seq) + '(' + traceback(t+1, j-1, seq) + ')'
        return ''


def Nussinov(seq):
    n = len(seq)
    global Opt
    Opt = [[0]*n for x in range(n)]
    for j in range(n):
        for i in reversed(range(j+1)):
            if i >= j-4:
                Opt[i][j] = 0
            else:
                maximum = Opt[i][j-1]
                for t in range(i, j-4):
                    if is_pair(seq[t], seq[j]):
                        if t == 0:
                            maximum = max(1 + Opt[t + 1][j - 1], maximum)
                        else:
                            maximum = max(Opt[i][t - 1] + 1 + Opt[t + 1][j - 1], maximum)
                Opt[i][j] = maximum
    return Opt[0][n-1]


def random_seq(size):
    result = ''
    base = ['A', 'G', 'C', 'U']
    for i in range(size):
        result += base[random.randint(0,3)]
    return result


def main():
    with open(sys.argv[1]) as f:
        seq = f.read().splitlines()
        for i in range(0, len(seq), 2):
            # start timing
            start = time.time()
            pairs = Nussinov(seq[i])
            end = time.time()
            n = len(seq[i])
            print(seq[i])
            print(traceback(0, n-1, seq[i]))
            print('Length = ' + str(n) + ', Pairs = ' + str(pairs) + ', Time = ' + str(end - start) + ' sec')
            # print the Opt Table
            if n <= 12:
                for i in range(n):
                    for j in range(n):
                        print(Opt[i][j], end = ' ')
                    print('')
            print('')

    if False:  # True to execute timing tests, False to skip them
        for k in range(4, 13):
            seq = random_seq(int(math.pow(2, k)))
            # start timing
            start = time.time()
            pairs = Nussinov(seq)
            end = time.time()
            n = len(seq)
            print(seq)
            print(traceback(0, n - 1, seq))
            print('Length = ' + str(n) + ', Pairs = ' + str(pairs) + ', Time = ' + str(end - start) + ' sec\n')


if __name__ == "__main__":
    main()