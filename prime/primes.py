from math import isqrt

if __name__ == '__main__':
    value = int(input('Insert a number: '))
    if value < 2:
        print('Invalid argument')
    if value < 9:
        for x in range(2, value):
            print('Checking ', value, '/', x)
            if (value % x) == 0:
                print('Not a prime number')
                exit(0)
    for x in range(2, isqrt(value)):
        print('Checking ', value, '/', x, '... ', end='')
        if (value % x) == 0:
            print('Not a prime number')
            exit(0)
        print('ok')
    print('A prime number')
    exit(0)
