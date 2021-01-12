
from gallows import create_gallows

def print_round(gallows, round):
    clear_screen()
    for i in gallows[round]:
        print(i)

def main():
    gallows = create_gallows()
    print_round(gallows, 4)

def clear_screen():
    print("\n" * 50)
if __name__ == "__main__":
    main()
