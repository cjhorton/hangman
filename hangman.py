import linecache
import random
from os import path
from gallows import create_gallows

class WordBankError(Exception):
    """Raised when either the word bank or word bank idx files aren't found"""
    pass

def print_round(gallows, round):
    clear_screen()
    for i in gallows[round]:
        print(i)

def word_bank_files_exist(bank_path, idx_path):
    return  path.exists(bank_path) and path.exists(idx_path)

def populate_difficulty_brackets(idx_path):
    """Goes through the word bank idx file and placese the word lines into easy, medium, hard brackets"""
    brackets = {"easy": [3, -1, -1], "medium": [7, -1, -1], "hard": [13, -1, -1]} #diff:[length min, start line, end line]
    with open(idx_path, "r") as f:
        num = 1
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if num == 1: #first line of file contains the first and last word line numbers
                first, last = line.split(":")
                brackets["hard"][2] = int(last)
            else:
                length, start_line = line.split(",")
                length = int(length)
                start_line = int(start_line)
                if length >= brackets["easy"][0] and length < brackets["medium"][0]: #easy
                    if brackets["easy"][1] == -1: #difficulty start line hasn't been set yet
                        brackets["easy"][1] = start_line
                elif length >= brackets["medium"][0] and length < brackets["hard"][0]: #medium
                    if brackets["medium"][1] == -1:
                        brackets["medium"][1] = start_line
                    if brackets["easy"][2] == -1: #difficulty end line hasn't been set yet
                        brackets["easy"][2] = start_line - 1 #easy ends 1 less than first medium start
                else:
                    if brackets["hard"][1] == -1:
                        brackets["hard"][1] = start_line
                    if brackets["medium"][2] == -1:
                        brackets["medium"][2] = start_line - 1
            num += 1
    return brackets

def get_word_on_line(line, word_bank_path):
    """Uses linecache module to return the word on the given line in the hangman_word_bank file"""
    #I am not sure if the cache will be persisted between function calls?
    word = linecache.getline(word_bank_path, line).strip()
    return word

def get_random_word_in_difficulty(word_bank_path, brackets, difficulty):
    #brackets - diff:[length min, start line, end line]
    if difficulty == "easy" or difficulty == "medium" or difficulty == "hard":
        line = random.randint(brackets[difficulty][1], brackets[difficulty][2])
    else: #no difficulty - use entire range 
        line = random.randint(brackets["easy"][1], brackets["hard"][2])
    print(f"line is: {line}")
    return get_word_on_line(line, word_bank_path)

def cleanup():
    linecache.clearcache()

def run(config):
    """Game loop"""
    run = True
    brackets = populate_difficulty_brackets(config["word_bank_idx_path"])
    print(get_random_word_in_difficulty(config["word_bank_path"], brackets, "medium"))
    gallows = create_gallows()
    while run:
        letter = input("Enter a letter or 1 to exit:")
        if len(letter) == 0:
            print("Nothing was entered.  Please try again.")
        else:
            letter = letter[0] #just grab first element of whatever was entered
            if letter ==  "1": #exit
                run = False
                continue
            else:
                if letter.isalpha():
                    print(f"You entered the letter {letter}")
                else:
                    print(f"That was an invalid entry.")


def main():
    config = {"word_bank_path": "hangman_word_bank", "word_bank_idx_path": "hangman_word_bank_idx"}
    try:
        found = word_bank_files_exist(config["word_bank_path"], config["word_bank_idx_path"] )
        if not found:
            raise WordBankError
    except WordBankError:
        print("Could not locate either the hangman_word_bank or hangman_word_bank_idx files")
        return
    run(config)

def clear_screen():
    print("\n" * 50)

if __name__ == "__main__":
    main()
