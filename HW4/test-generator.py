# Freddie He
# heyingge
# 1560733
# test case file generator
import sys
import random as rm


# uniform square case generator: generate x random points with d digits precision
def us_gen(f, x, d):
    for i in range(x):
        f.write(str(round(rm.uniform(-0.5, 0.5), d)))
        f.write(' ')
        f.write(str(round(rm.uniform(-0.5, 0.5), d)))
        f.write('\n')


# worst case generator: generate x random points with d digits precision
def wc_gen(f, x, d):
    for i in range(x):
        f.write('0 ')
        f.write(str(round(rm.uniform(0, 1), d)))
        f.write('\n')


def main():
    f = open(sys.argv[1], "w")
    while True:
        case = input("Type 1 to generate uniform square case; Type 2 to generate worst case.")
        if case == '1':
            us_gen(f, int(sys.argv[2]), int(sys.argv[3]))
            break
        elif case == '2':
            wc_gen(f, int(sys.argv[2]), int(sys.argv[3]))
            break
        else:
            continue


if __name__ == '__main__':
    main()