import csv
import os
import time


def follow(filename):
    """
    Follow lines from a file as a generator
    """
    f = open(filename, "r")
    f.seek(0, os.SEEK_END)  # Move file pointer 0 bytes from end of file
    while True:
        line = f.readline()
        if line == "":
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    lines = follow("python-mastery/Data/stocklog.csv")
    rows = csv.reader(lines)
    for row in rows:
        print(row)
