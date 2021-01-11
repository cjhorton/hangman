#!/usr/bin/env python

import re

def parse_words_file(words_path, words):
    """Parses the /usr/share/dict/words file into words usable by the hangman program """
    try:
      with open(words_path, "r") as f:
        #we want words that are 3 or more letters long
        pattern = re.compile(r"[a-zA-Z]{3,}$")
        parsed_line = ""
        for line in f:
          parsed_line = parse_word_line(line)
          #print(parsed_line)
          if word_is_valid(parsed_line, pattern):
            #add new line char at the end since will be using writelines()
            words.append(parsed_line + "\n")
            #print(parsed_line)
    except IOError:
      print("Unable to locate the words file.  Please check the path and try again.")
    except EOFError:
      print("This file appears to be empty.  Please check the file contents.")
    print("All done parsing the words file.")

def parse_word_line(line):
    """Do any line parsing here.  Currently, only performing strip()"""
    line = line.strip()
    return line


def word_is_valid(line, pattern):
    line = line.strip()
    return re.match(pattern, line)

def create_word_bank_file(words, path):
    with open(path, "w") as f:
      f.writelines(words)

def main():
    #file = "/usr/share/dict/words"
    input_file = "test_words"
    words = []
    parse_words_file(input_file, words)
    #print(words)
    output_file = "hangman_word_bank"
    create_word_bank_file(words, output_file)

if __name__ == "__main__":
  main()
