#!/usr/bin/env python3

# file_read_write_test.py
# python script by gsb

# Developed on macos 16.1 (21.6.0 Darwin Kernel Version 21.6.0: root:xnu-8020.240.7~1/RELEASE_X86_64),
# zsh (zsh 5.8.1 (x86_64-apple-darwin21.0), and python 3.9.4

# Version 0.01: adaptation from zsh shell script v0.03 to python 3.10.7

import sys
import os


print()
print("Test script for reading and writing to files in directory")
print()

# Check if proper python version is running script
MIN_PYTHON = (3, 10, 7)
if sys.version_info < MIN_PYTHON:
    print("You are running Python ", sys.version_info)
    sys.exit("Python %s.%s.%s or later is required.\n" % MIN_PYTHON)

# Set up

# Functions

def yesno(question):
    """Simple Yes/No Function."""
    prompt = f'{question}? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno(question)
    if ans == 'y':
        return True
    return False

def update_answer_files():
    print("Wordle is solved. Answer is: ")
    print(" " + ANSWER)
    print()

    if yesno("Update past Wordle answers"):
        # Open as file past_wordle_answers.txt
        try:
            with open('past_wordle_answers.txt.1', 'r') as past_answers_file_h:
                past_answers_list = past_answers_file_h.readlines()
        except Exception as err:
            print(f"Unexpected error opening {fname} is",repr(err))
            sys.exit(1)

        if mode == 2:
            print("First 5 words of past_answers list are:")
            print(past_answers_list[:5])
            print()
            print("Last 5 words of past_answers list are:")
            print(past_answers_list[-5:])
            print()

        if not yesno("Continue"):
            sys.exit()

        # Strip leading \n if present
        if past_answers_list[0] == '\n':
            del past_answers_list[0]

        # Strip trailing \n if present
        if past_answers_list[-1] == '\n':
            del past_answers_list[-1]

        # Strip out newlines and convert to comma separated list
        past_answers_list = [i.strip('\n') for i in past_answers_list]

        if mode == 2:
            print("After stripping \\n's, first 5 words of past_answwers_list are:")
            print(past_answers_list[:5])
            print()
            print("Last 5 words of past_answers list are:")
            print(past_answers_list[-5:])
            print()

        if not yesno("Continue"):
            sys.exit()

        # Check if ANSWER is already in past_answers_list
        if ANSWER in past_answers_list:
            print(ANSWER + " is already in past_answer_list")

        else:

            # Append ANSWER to list
            if mode >= 1:
                a = len(past_answers_list)
                print("past_answers_list has " + str(a) + " entries.")
                print()

                print("Appending " + ANSWER + " to past_answers_list.")
                
            past_answers_list.append(ANSWER)

            if mode >= 1:
                a = len(past_answers_list)
                print("past_answers_list now has " + str(a) + " entries.")
                print()

            if mode == 2:
                print("First 5 words of past_answers list are:")
                print(past_answers_list[:5])
                print()
                print("Last 5 words of past_answers list are:")
                print(past_answers_list[-5:])
                print()

            if not yesno("Continue"):
                sys.exit()

    
            # Sort list alphabetically
            if mode >= 1:
                print("Sorting past_answers_list alphabetically")
                
            past_answers_list.sort()

            if mode == 2:
                print("First 5 words of past_answers list are:")
                print(past_answers_list[:5])
                print()
                print("Last 5 words of past_answers list are:")
                print(past_answers_list[-5:])
                print()

            if not yesno("Continue"):
                sys.exit()

            # Convert list back to newline delimited list
            past_answers_list = [i + '\n' for i in past_answers_list]

            if mode == 2:
                print("First 5 words of past_answers list are:")
                print(past_answers_list[:5])
                print()
                print("Last 5 words of past_answers list are:")
                print(past_answers_list[-5:])
                print()

            if not yesno("Continue"):
                sys.exit()

            # Write list
            try:
                with open("past_wordle_answers.txt.1", "w") as past_answers_file_h:
                    past_answers_file_h.writelines(past_answers_list)
            except Exception as err:
                print(f"Unexpected error opening {fname} is ",repr(err))
                sys.exit(1)

            print("file written")
            print()

        # Update unused_wordle_answers.txt

        # Read unused_answers_list.txt

        print()
        print("Updating unused_wordle_answers_list:")
        print()
        
        try:
            with open("unused_wordle_answers.txt.1", "r") as unused_answers_file_h:
                unused_answers_list = unused_answers_file_h.readlines()
        except Exception as err:
            print(f"Unexpected error opening {fname} is",repr(err))
            sys.exit(1)

        if mode == 2:
            print("First 5 words of unused_answers list are:")
            print(unused_answers_list[:5])
            print()
            print("Last 5 words of unused_answers list are:")
            print(unused_answers_list[-5:])
            print()

        # Strip leading \n if present
        if unused_answers_list[0] == '\n':
            del past_answers_list[0]

        # Strip trailing \n if present
        if unused_answers_list[-1] == '\n':
            del past_answers_list[-1]

        # Strip out newlines and convert to comma separated list
        unused_answers_list = [i.strip('\n') for i in unused_answers_list]

        if mode == 2:
            print("After stripping \\n's, first 5 words of unused_answers_list are:")
            print(unused_answers_list[:5])
            print()
            print("Last 5 words of unused_answers list are:")
            print(unused_answers_list[-5:])
            print()

        if not yesno("Continue"):
            sys.exit()

        if ANSWER in unused_answers_list:
            unused_answers_list.remove(ANSWER)
            #unused_answers_list = [word for word in unused_answers_list if word != ANSWER]

            if mode == 2:
                print("After removing " + ANSWER + ", first 5 words of unused_answers list are:")
                print(unused_answers_list[:5])
                print()
                #print("Last 5 words of unused_answers list are:")
                #print(unused_answers_list[-5:])
                #print()

            # Convert list back to newline delimited list
            unused_answers_list = [i + '\n' for i in unused_answers_list]

            if mode == 2:
                print("After adding \\n's back in, first 5 words of unused_answers list are:")
                print(unused_answers_list[:5])
                print()
                print("Last 5 words of unused_answers list are:")
                print(unused_answers_list[-5:])
                print()

            if not yesno("Continue"):
                sys.exit()


            # Write modified unused_answers_list to file
            try:
                with open("unused_wordle_answers.txt.1", "w") as unused_answers_file_h:
                    unused_answers_file_h.writelines(unused_answers_list)
            except Exception as err:
                print(f"Unexpected error opening {fname} is",repr(err))
                sys.exit(1)

            print("File written")
            print()

            sys.exit("Completed")

        else:
            print("Error: " + ANSWER + " is not in unused_answers.")
            sys.exit("Completed")

    else:
        #print("Be sure to update past_wordle_answers.txt.")
        sys.exit("Completed")

# Begin main program

print("Enter guesses as 5 letter word in lowercase.")
print()
ANSWER = input("Enter ANSWER:")

current_answers_no = 1
mode = 2

if current_answers_no == 1:
    update_answer_files()

sys.exit(0)


