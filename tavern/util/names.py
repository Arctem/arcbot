import os

SHAKESPEARE_NAMES = [line.strip() for line in open(os.path.join(
    os.getcwd(), "tavern", "util", "shakespeare_names.txt"), 'r')]
