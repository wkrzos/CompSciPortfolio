import fileinput
   
def read_and_print_file(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            print(line.strip())
    
def main():
    read_and_print_file('NASA100LINES')
    
if __name__ == "__main__":
    main()