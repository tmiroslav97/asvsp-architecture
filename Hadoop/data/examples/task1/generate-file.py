# /bin/usr/python

import random
import string

ROWS = int(1e6)


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def main():
    with open('sample.csv', 'w') as f:
        for _ in range(ROWS):
            f.write("{},{},{}\n".format(randomString(),
                                       random.uniform(7.5, 9.5), randomString()))


if __name__ == "__main__":
    main()
