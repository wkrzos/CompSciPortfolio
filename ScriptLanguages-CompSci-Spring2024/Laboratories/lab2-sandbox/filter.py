# filter.py
import sys
import re

def filter_lines(keyword):
    pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
    for line in sys.stdin:
        if pattern.search(line):
            print(line, end='')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filter.py <keyword>")
        sys.exit(1)
    keyword = sys.argv[1]
    filter_lines(keyword)
