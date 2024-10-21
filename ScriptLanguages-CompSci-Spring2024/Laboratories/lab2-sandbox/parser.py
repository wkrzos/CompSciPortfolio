# parser.py
def parse_line(line):
    tokens = line.strip().split()
    if len(tokens) == 2:
        number, category = tokens
        return f"{number}: {category}\n"
    else:
        return None

def main(input_file):
    with open(input_file, 'r') as f:
        for line in f:
            parsed_line = parse_line(line)
            if parsed_line:
                print(parsed_line, end='')

if __name__ == "__main__":
    input_file = 'input.txt'  # This would be your input file
    main(input_file)