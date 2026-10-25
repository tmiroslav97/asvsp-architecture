#!/usr/bin/env python3

import random
import string
import os

ROWS = int(os.environ.get("ROWS", "1000000"))


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def main():
    with open(os.environ.get("OUTPUT_FILE", "sample.csv"), 'w') as f:
        for _ in range(ROWS):
            f.write("{},{},{}\n".format(randomString(),
                                       random.uniform(7.5, 9.5), randomString()))


if __name__ == "__main__":
    main()
