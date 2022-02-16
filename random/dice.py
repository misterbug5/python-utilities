from random import choice
import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You must put at least one argument")
        exit(1)
    options = sys.argv
    del options[0]
    print(choice(options))