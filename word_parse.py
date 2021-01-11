#!/usr/bin/env python

import re

def parse_words_file(words_path, words):
    """Parses the /usr/share/dict/words file into words usable by the hangman program """
    try:
      with open(words_path, "r") as f:
        #we want words that are 3 or more letters long
        parsed_line = ""
        for line in f:
          parsed_line = parse_word_line(line)
          if word_is_valid(parsed_line):
            #add new line char at the end since will be using writelines()
            words.append(process_word(parsed_line) + "\n")

    except IOError:
      print("Unable to locate the words file.  Please check the path and try again.")
    except EOFError:
      print("This file appears to be empty.  Please check the file contents.")
    print("All done parsing the words file.")

def parse_word_line(line):
    """Do any line parsing here.  Currently, only performing strip()"""
    line = line.strip()
    return line


def word_is_valid(line):
    """Word is valid if it contains only alpha and not all capital (not an acronym)"""
    pattern1 = re.compile(r"[a-zA-Z]{3,}$")
    pattern2 = re.compile(r"[A-Z]{3,}$")
    return re.match(pattern1, line) and not re.match(pattern2, line)

def process_word(word):
    """Performs processing of a valid word.  Currrently converts to lowercase."""
    p_word = word.lower()
    return p_word

def arrange_word_list(words):
    """Sorts the word list alphabetically and by length"""
    words.sort()
    words.sort(key=len)

def create_word_bank_file(words, path):
    """Created the word bank file that will be used for the game"""
    with open(path, "w") as f:
      f.writelines(words)

def main():
    #file = "/usr/share/dict/words"
    input_file = "test_words"
    words = []
    parse_words_file(input_file, words)
    arrange_word_list(words)
    output_file = "hangman_word_bank"
    create_word_bank_file(words, output_file)

if __name__ == "__main__":
  main()
