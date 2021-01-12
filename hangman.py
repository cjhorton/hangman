import linecache
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

def run():
    """Game loop"""
    pass

def populate_difficulty_brackets(idx_path):
    brackets = {"easy": [3, -1, -1], "medium": [7, -1, -1], "hard": [13, -1, -1]} #diff:[length min, start line, end line]
    with open(idx_path, "r") as f:
        num = 1
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if num == 1:
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
    print(brackets)

def main():
    word_bank_path = "hangman_word_bank"
    word_bank_idx_path = "hangman_word_bank_idx"
    try:
        found = word_bank_files_exist(word_bank_path, word_bank_idx_path)
        if not found:
            raise WordBankError
    except WordBankError:
        print("Could not locate either the hangman_word_bank or hangman_word_bank_idx files")
        return

    populate_difficulty_brackets(word_bank_idx_path)
    #gallows = create_gallows()
    #print_round(gallows, 4)

def clear_screen():
    print("\n" * 50)

if __name__ == "__main__":
    main()
