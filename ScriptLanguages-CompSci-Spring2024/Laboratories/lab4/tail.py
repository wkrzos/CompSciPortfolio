import sys

def tail(file_path=None, lines=10):
    # Read from stdin if no directory is given
    if file_path is None:
        content = sys.stdin.readlines()
    else:
        with open(file_path, 'r') as file:
            content = file.readlines()
    
    # Write last n lines
    for line in content[-lines:]:
        print(line, end='')

def parse_args(args):
    lines = 10
    file_path = None
    for arg in args:
        if arg.startswith('--lines='):
            lines = int(arg.split('=')[1])
        elif arg == '--follow':
            # Base version ommits --follow
            pass
        else:
            file_path = arg
    
    return file_path, lines

if __name__ == "__main__":
    file_path, lines = parse_args(sys.argv[1:])
    tail(file_path, lines)