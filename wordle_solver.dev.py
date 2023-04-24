#!/usr/bin/env python3

# wordle_solver.dev.py
# Wordle solver python script by gsb

# Developed on macos 16.1 (21.6.0 Darwin Kernel Version 21.6.0: root:xnu-8020.240.7~1/RELEASE_X86_64),
# using MacOS system python 3.10.7
# Tested to run on Mint Linux with Python 3.10.6

# Version 0.01: adaptation from zsh shell script v0.03 to python 3.10.6+
# Version 0.02: added analysis section, added verbosity flags, dropped use of re module, bugfixes.
# Version 0.03: further bug fixes, last version with old valid word lists and answer list.

# Dev: Between Nov 2022 and Feb 2023, NYTimes editors changed the valid word lists and answers lists.
# Now the answers are "curated" which means? Perhaps any word from total (valid) word list can be used
# as the answer - like "snafu" on Apr 9. Or, for that matter, any word at all.
# Dev version changed so both valid guess list and potential answer list are analyzed and can be checked.

import sys
import os
import os.path

print()
print("Welcome to wordle_solver, your assistant at playing Wordle.")
print("(wordle_solver.dev.py)")
print()

# Check if proper python version is running script
MIN_PYTHON = (3, 10, 6)
if sys.version_info < MIN_PYTHON:
    print("You are running Python ", sys.version_info)
    sys.exit("Python %s.%s.%s or later is required.\n" % MIN_PYTHON)

# Set up

# Functions

# Simple yes/no function

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

# Function to check if word is in list

def check(word, list):
    if word in list:
        # print("The word is in the list!")
        return True
    else:
        # print("The word is not in the list!")
        return False

# Update past_wordle_answers.txt file

def update_past_answer_list():
    if yesno("Update past Wordle answers"):
        # Open as file past_wordle_answers.txt
        try:
            with open('past_wordle_answers.txt', 'r') as past_answers_file_h:
                past_answers_list = past_answers_file_h.readlines()
        except Exception as err:
            print(f"Unexpected error opening {fname} is",repr(err))
            sys.exit("Error, line 57")

        if mode == 2:
            print("First 5 words of past_answers list are:")
            print(past_answers_list[:5])
            print()
            print("Last 5 words of past_answers list are:")
            print(past_answers_list[-5:])
            print()

            if not yesno("Continue"):
                sys.exit("update_answer_files aborted, line 71")

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
                sys.exit("update_answer_files aborted, line 94")

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
                print()
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
                    sys.exit("update_answer_files aborted, line 127")
    
            # Sort list alphabetically
            if mode == 2:
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
                    sys.exit("update_answer_files aborted, line 144")

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
                    sys.exit("update_answer_files aborted, line 158")

            # Write list
            try:
                with open("past_wordle_answers.txt", "w") as past_answers_file_h:
                    past_answers_file_h.writelines(past_answers_list)
            except Exception as err:
                print(f"Unexpected error opening {fname} is ",repr(err))
                sys.exit("Error in update_answer_files, line 166")

            if mode == 2:
                print("Updated past_answers_list file written")
                print()

        update_unused_answer_list()
        
    else:
        print("Be sure to update past_wordle_answers.txt.")

# Update unused_sordle_answers.txt file       

def update_unused_answer_list():

    if yesno("Update unused Wordle answers"):
        # Open as file unused_wordle_answers.txt

        print()
        if mode >= 1:
            print("Updating unused_wordle_answers_list:")
            print()
        
        try:
            with open("unused_wordle_answers.txt", "r") as unused_answers_file_h:
                unused_answers_list = unused_answers_file_h.readlines()
        except Exception as err:
            print(f"Unexpected error opening {fname} is",repr(err))
            sys.exit("Error in update_answer_files, line 185")

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
                sys.exit("update_answer_files aborted, line 215")

        if ANSWER in unused_answers_list:

            if mode >= 1:
                a = len(unused_answers_list)
                print("unused_answers_list has " + str(a) + " entries.")
                print()

                print("Removing " + ANSWER + " from unused_answers_list.")
                
            unused_answers_list.remove(ANSWER)

            if mode >= 1:
                a = len(unused_answers_list)
                print()
                print("unused_answers_list now has " + str(a) + " entries.")
                print()

            if mode == 2:
                print("After removing " + ANSWER + ", first 5 words of unused_answers list are:")
                print(unused_answers_list[:5])
                print()

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
                    sys.exit("update_answer_files aborted, line 251")


            # Write modified unused_answers_list to file
            try:
                with open("unused_wordle_answers.txt", "w") as unused_answers_file_h:
                    unused_answers_file_h.writelines(unused_answers_list)
            except Exception as err:
                print(f"Unexpected error opening {fname} is",repr(err))
                sys.exit("Error in update_answer_files, line 260")

            if mode >= 1:
                print("File written")
                print()

            sys.exit("Completed update of answer files")

        else:
            print(ANSWER + " is not in unused_answers.")
            sys.exit("Error in update_answer_files, line 269")

    else:
        print("Be sure to update unused_wordle_answers.txt.")

# Function to display remaining valid guesses

def display_valid_guesses():

    print("Abridged valid guess list contains " + str(len(abridged_valid_guesses)) + " words")

    if yesno("Display abridged valid guess list"):
        for word in abridged_valid_guesses:
            print(word)
        print()

    # Show letter frequency in abridged valid guess list

    if yesno("Print letter frequency in possible guesses from abridged valid guess list"):

        # Convert abdidged_guess_list to string
        abridged_guess_string = ' '.join(abridged_valid_guesses)
        
        # Create dict containing letter frequency    
        letter_frequency = {}
        from string import ascii_lowercase as alc
        for k in alc:
            a = abridged_guess_string.count(k)
            if a >= 1:
                letter_frequency[k] = a
     
        from collections import Counter
        c = Counter(letter_frequency)
        abridged_guesses_sorted = c.most_common()

        print("List of letters by frequency")
        for k, v in abridged_guesses_sorted:
            print(k, ' ', v)

   
## Start-up
        
# Clear old tmp files from prior runs

# Choose whether hard mode is enabled
hard = 0
if yesno("Enable hard mode?"):
    hard = 1

# Choose whether to run in quiet, verbose, or debug mode
mode = 0
prompt = f'Quiet mode is default. Enable verbose (v) or debug (d) mode?:'
ans = input(prompt).strip().lower()
if ans == 'v':
    print("Verbose mode selected.")
    mode = 1
elif ans == 'd':
    print("Debug mode selected")
    mode = 2
else:
    print("Continue in quiet mode.")

# Preload current_answers_list with new Wordle answer list

with open('new_answer_list.txt', 'r') as my_file:
    current_answers_list = my_file.readlines()

# Strip leading \n if present
if current_answers_list[0] == '\n':
    del current_answers_list[0]

# Strip trailing \n if present
if current_answers_list[-1] == '\n':
    del current_answers_list[-1]

# Strip out newlines and convert to comma separated list
current_answers_list = [i.strip('\n') for i in current_answers_list]

# Remove blank lines/items
current_answers_list = list(filter(None, current_answers_list))

# Check that all entires in current_answer_list have 5 characters
for word in current_answers_list:
    if len(word) != 5:
        print("Error - item(s) in current_answers_list do not contain 5 letters.")
        print("Possible error/corruption in wordle_answers.txt file.")
        sys.exit("Error, line 322")

# Read file 'valid_guess_list.txt' and convert to list
with open('new_total_word_list.txt', 'r') as my_file:
    valid_guesses = my_file.readlines()

# Strip leading \n if present
if valid_guesses[0] == '\n':
    del valid_guesses[0]

# Strip trailing \n if present
if valid_guesses[-1] == '\n':
    del valid_guesses[-1]

# Strip out newlines and convert to comma separated list
valid_guesses = [i.strip('\n') for i in valid_guesses]

# Remove blank lines/items
valid_guesses = list(filter(None, valid_guesses))

# Check that all entires in current_answer_list have 5 characters
for word in valid_guesses:
    if len(word) != 5:
        print("Error - item(s) in valid_guesses do not contain 5 letters.")
        print("Possible error/corruption in valid_guess_list.txt file.")
        sys.exit("Error, line 347")

# Create abridged_valid_guesses list
abridged_valid_guesses = valid_guesses

# Count number of words in initial_answer_list

total_answers = len(current_answers_list)
print("Starting number of possible answers is " + str(total_answers))

# Create ANSWER with 5 dots
ANSWER = "....."

# Main loop through guesses 1-6

print()
if mode == 2:
    print("Main loop")

guess = []

for i in range(6):
    if mode == 2:
        print(i)
        print()
        print("Guess", i+1)
        print()

    # Guess selector: display guesses which contain desired letters

    # Entry section
    while True:
        print("Enter guesses as 5 letter word in lowercase.")
        print()
        guess_word = input("Enter guess:")

        # Trap null entries
        if len(guess_word) == 0:
            print("Guess is null - try again")

        # Trap guesses containing blanks/spaces
        elif ' ' in guess_word:
            print("Guess contains spaces or blanks - try again.")  

        # Trap enties =/= to 5 letters
        elif len(guess_word) != 5:
            print("Guess must be 5 letters long")

        # Check if numerals or special characters are in guess_word
        elif not guess_word.isalpha():
            print("No numerals or special characters allowed.")
            
        # Check if guess contains uppercase and changes to lowercase with alert
        elif not guess_word.islower():
            print("Entry error. Entries should be all in lowercase")
        
        # Confirm entry
        elif not yesno("You entered " + guess_word + ". Correct"):
            print("You entered n")
            print("Error in entering guess.")

        else:
            if mode >= 1:
                print("You entered y")

            # Check if entry is in valid guess list
            if mode >= 1:
                print("Checking whether guess is in valid guess list")
            print()
            
            if not guess_word in valid_guesses:
                print(guess_word + " is not a Wordle's valid guess list")
                print()
                
            else:
                if hard == 0:
                    print(guess_word + " is a valid guess")
                    print()
                    break

                else:
                    if i == 0:
                        if mode == 2:
                            print("First interation: abridged_valid_guesses not yet defined")
                        print(guess_word + " is a valid guess.")
                        
                    else:
                        if not guess_word in abridged_valid_guesses:
                            print(guess_word + " is not a valid guess (hard mode).")
                
                break
        
    # End of entry section
        
    # Add entry to to guess - list of guesses
    guess.append(guess_word)
    if mode == 2:
        print("Guess #", i+1, "1s ", guess[i])
    print()

    # Analysis section

    #
    # Step 1: Select words that contain matched letters in correct position.
    #
    
    if mode >= 1:
        print("Step 1: Selecting words that contain letters matched in correct position.")

    # Enter and validate letters which match exactly (green square)

    while True:
        print("Enter letters which exactly match (green square).")
        print("Enter letters in lowercase in any order.")
        print("Enter nothing (hit return key) if no letters exactly match.")
        correct = input("Enter letter(s) > ")

        # Trap null entry
        if len(correct) == 0:
            if not yesno("No letters correctly matched (green square). Correct"):
                if mode == 2:
                    print("'n' was entered.")
                print()
            else:
                if mode == 2:
                    print("'y' was entered")
                # Skip to Step 2
                print("No correctly matching letters. Moving to step 2.")
                break

        # Check if all entered letters actually are in guess_word
        elif len(correct) >=1:
            # Remove duplicate letters from correct
            correct = "".join(set(correct))

            # Iterate through letters in correct to confirm they are in guess_word
            invalid = 0
            for letter in correct:
                if not letter in guess_word:
                    print(letter + " does not appear in guess.")
                    invalid +=1
                else:
                    print(letter + " appears in guess.")

            if invalid == 0:
                print("All letters are found in guess.")
                break

    # Count number of times each letter occurs in guess_word and deal with count

    wrong = guess_word

    if len(correct) >= 1:

        for letter in correct:
            count = guess_word.count(letter)

            if count == 0:
                print("Error. Letter " + letter + " does not appear in guess")
                sys.exit("Error, line 491")
                
            elif count == 1:
                if mode >= 1:
                    print("Letter " + letter + " appears once in guess.")
                j = guess_word.index(letter)
                if mode == 2:
                    print("index is " + str(j))
                if mode >= 1:
                    print("Position of " + letter + " is " + str(j))

                ANSWER = ANSWER[:j] + letter + ANSWER[j+1:]
                wrong = wrong[:j] + "." + wrong[j+1:]

                if mode == 2:
                    print("ANSWER is now " + ANSWER)
                    print("wrong is now " + wrong)

                temp_list = []
                temp_list = [ word for word in current_answers_list if letter == word[j] ]
                              
                if mode == 2:
                    print("After solving for " + letter + " in position " + str(j) + ", " + str(len(temp_list)) + " words remain.")
                    print()

                current_answers_list = temp_list

                # Now do the same for valid guesses
                temp_guess_list = []
                temp_guess_list = [ word for word in abridged_valid_guesses if letter == word[j] ]
                    
                if mode == 2:
                    print("After solving for " + letter + " in position " + str(j) + ", " + str(len(temp_guess_list)) + " valid guesses remain.")
                    print()

                abridged_valid_guesses = temp_guess_list

            elif count > 1:
                if mode >= 1:
                    print("Letter " + letter + " appears " + str(count) + " times in guess.")
                # For each occurrence of letter, determine if it is an exact match or not
                for j, v in enumerate(guess_word):
                    if mode == 2:
                        print(j, '  ', v)
                    if letter == v:
                        print(letter + " occurs in position " + str(j) + ".")
                        if yesno("Is this an exact match (green square)"):
                            ANSWER = ANSWER[:j] + letter + ANSWER[j+1:]
                            wrong = wrong[:j] + "." + wrong[j+1:]

                            if mode == 2:
                                print("ANSWER is now " + ANSWER)
                                print("wrong is now " + wrong)

                            temp_list = []
                            temp_list = [ word for word in current_answers_list if letter == word[j] ]
                            
                            if mode == 2:
                                print("After solving for " + letter + " in position " + str(j) + ", ", str(len(temp_list)), " words remain.")
                                print()

                            current_answers_list = temp_list

                            # Now do the same for valid guesses
                            temp_guess_list = []
                            temp_guess_list = [ word for word in abridged_valid_guesses if letter == word[j] ]
                    
                            if mode == 2:
                                print("After solving for " + letter + " in position " + str(j) + ", " + str(len(temp_guess_list)) + " valid guesses remain.")
                                print()

                            abridged_valid_guesses = temp_guess_list

        # Tabulate results
        current_answers = len(current_answers_list)
        print("After matching for answers which contain " + correct + ",")
        print(str(current_answers) + " words are left from initial " + str(total_answers) )

        # If answer is found ( len(current_answers) = 1 ), write to ANSWER, and update past answer lists
        if current_answers == 1:
            ANSWER = ''.join(current_answers_list)
            print("Wordle may be solved - assuming editors are using a word from the answer list.")
            print("Answer is: ")
            print(" " + ANSWER)
            print()
            print("Best to check and see if this solution actually solved the puzzle online. If so, proceed.")

            if yesno("Did " + ANSWER + " solve the Wordle puzzle"):
                update_past_answer_list()
                sys.exit("Program completed")
            else:
                print("Perhaps this is a 'curated' answer which could be found in the valid guess list?")
                if yesno("Print the current valid guess list for other possible solutions"):
                    for word in abridged_valid_guesses:
                         print(word)
                    sys.exit("Program completed")


        # Display results
        if mode >= 1:
            if yesno("Display current answer list"):
                for word in current_answers_list:
                    print(word)
            print()

    else:
        # No letters entered
        if mode >= 1:
            print("No letters exactly matching")

            if mode == 2:
                print("With null entry,type of current_answers_list is now ", type(current_answers_list))

            print()

    if mode >= 1:
        print("Done with step 1")
        
    if mode == 2:
        print("ANSWER is now " + ANSWER)
        print("wrong is now " + wrong)
        
    print()

    # End of Step 1

    #
    # Step 2: Select all words containing letters matched but in wrong position (yellow square)
    #
    
    if mode >= 1:
        print("Step 2: Select all words containing letters matched but in wrong position.")

    # Enter and validate letters matching in wrong position (yellow square)
    while True:
        print("Enter letters which match in wrong position (yellow square).")
        print("Enter letters in lowercase in any order.")
        print("Enter nothing (hit return key) if no letters match.")
        partial = input("Enter letter(s) > ")

        # Trap null entry
        if len(partial) == 0:
            if not yesno("No letters matched in wrong position (yellow square). Correct"):
                print("'n' was entered.")
                # Entry error. Go back to entry
            else:
                print("'y' was entered")
                # Skip to Step 3
                print("No correctly matching letters. Moving to step 3.")
                break
        
        # Check if all entered letters actually are in guess_word
        elif len(partial) >=1:
            # Remove duplicate letters from partial
            partial = "".join(set(partial))

            # Iterate through letters to confirm they are in guess_word
            invalid = 0
            for letter in partial:
                if not letter in guess_word:
                    print(letter + " does not appear in guess.")
                    invalid +=1
                else:
                    print(letter + " appears in guess.")

            if invalid == 0:
                print("All letters are found in guess.")
                print()
                break

    # Iterate through letters partially matched to eliminate possible answers

    current_answers = len(current_answers_list)

    if mode ==2:
        print("Partial matches \('partial'\) are " + partial + ".")
        print()

    for letter in partial:
        if mode == 2:
            print("Solving for  " + letter)
            print()
            print("current_answers_list contains " + str(len(current_answers_list)) + " words.")
            print()
    
        # Find words in answer list which contain letter in any position
        temp_list = []
        temp_list = [ word for word in current_answers_list if letter in word ]

        temp_answers = len(temp_list)

        wrong = wrong.replace(letter, '.')

        if mode >= 1:
            # Tabulate and display results of initial selection of possible answers
            print("After selecting all current answers containing " + letter + ", " + str(len(temp_list)) + " words are left")
            print()

        current_answers_list = temp_list

        # Now do the same for valid guesses
        temp_guess_list = []
        temp_guess_list = [ word for word in abridged_valid_guesses if letter in word ]
                    
        if mode == 2:
            print("After selecting valid guesses containing " + letter + ", " + str(len(temp_guess_list)) + " valid guesses remain.")
            print()

        abridged_valid_guesses = temp_guess_list

        if mode == 2:
            if yesno("Print current list of answers"):
                for word in current_answers_list:
                    print(word)
                print()

        # Count number of times each letter occurs in guess_word and deal with count
        count = guess_word.count(letter)
        
        if count == 0:
            print("Letter " + letter + " does not appear in guess")
            sys.exit("Error, line 657")
                 
        elif count >= 1:
            if mode == 2:
                print("Letter " + letter + " appears " + str(count) + " times in guess.")
                print()

            # Logic here is provisional. It is true in some examples but not in all?
            temp_list = []
            # if count > 1, and letter is also in correct, find all words with this number of the letter in question
            if correct.count(letter) and count > correct.count(letter):
                temp_list = [ word for word in current_answers_list if word.count(letter) == count ]

                # Tabulate and display results of selecting these possible answers
                if mode >= 1:
                    temp_answers = len(temp_list)
                    print("After selecting for those answers containing " + str(count) + " instances of " + letter + ",")
                    print(str(temp_answers) + " words are left out of " + str(current_answers) + ".")
                    print()

                if mode == 2:
                    current_answers_list = temp_list
                    print(type(current_answers_list))

                if mode >= 1:
                    if yesno("Print current list of answers"):
                        for word in current_answers_list:
                            print(word)
                    print()

            # For each occurrence of letter, determine if it is already in ANSWER or not
            for j, v in enumerate(guess_word):
                if mode == 2:
                    print(j, '  ', v)
                if letter == v:
                    if mode ==2:
                        print(letter + " occurs in position " + str(j) + ".")
                    if ANSWER[j] == letter:
                        print("letter " + letter + " already in ANSWER in this position") 
                    else:
                        # Find words in answer list which do not contain letter in this position j
                        temp_list = []
                        temp_list = [ word for word in current_answers_list if letter != word[j] ]

                        # Now do the same for valid guesses
                        temp_guess_list = []
                        temp_guess_list = [ word for word in abridged_valid_guesses if letter != word[j] ]
                    
                    # Tabulate and display results of this letter in this position
                    if mode >= 1:
                        print("After selecting for those remaining answers not containing " + letter + " at index " + str(j) +", " + str(len(temp_list)) + " words are left.")
                        print()
                            
                    current_answers_list = temp_list

                    if mode == 2:
                        print("After solving for guesses not containing " + letter + " in position " + str(j) + ", " + str(len(temp_guess_list)) + " valid guesses remain.")
                        print()

                    abridged_valid_guesses = temp_guess_list


                    if mode >= 1:
                        if yesno("Print current list of answers"):
                            for word in current_answers_list:
                                print(word)
                        print()

            # If letter occurs more than once, tabulate final results for letter in all positions of guess
            current_answers = len(current_answers_list)
            if count > 1:
                if mode >= 1:
                    print("After selecting answers which partially match " + letter + " in any position in " + guess_word + ",")
                    print(str(current_answers) + " words are left from initial " + str(total_answers) )
                    print()

    
    # Tabulate results from Step 2 if more than one letter was entered
    if len(partial) >= 1:
        print("After selecting answers which partially match '" + partial + "',")
        print(str(current_answers) + " words are left from initial " + str(total_answers) + ".")
        print()

    # If answer is found ( len(current_answers) = 1 ), write to ANSWER, and update past answer lists
    if current_answers == 1:
        ANSWER = ''.join(current_answers_list)
        print("Wordle may be solved - assuming editors are using a word from the answer list.")
        print("Answer is: ")
        print(" " + ANSWER)
        print()
        print("Best to check and see if this solution actually solved the puzzle online. If so, proceed.")

        if yesno("Did " + ANSWER + " solve the Wordle puzzle"):
            update_past_answer_list()
            sys.exit("Program completed")
        else:
            print("Perhaps this is a 'curated' answer which could be found in the valid guess list?")
            if yesno("Print the current valid guess list for other possible solutions"):
                for word in abridged_valid_guesses:
                    print(word)
                sys.exit("Program completed")

 
    # Display results if desired
    if mode >= 1:
        if yesno("Display current answer list"):
            for word in current_answers_list:
                print(word)
            print()
   
    if mode >= 1:
        print("Done with step 2")
        print()

    if mode == 2:
        print("wrong is now " + wrong)
        print()

    #
    # Step 3: Eliminate words containing unmatched letters
    #

    if mode >= 2:
        print("Step 3: Eliminate words containing unmatched letters")
    print()

    wrong = wrong.replace('.', '')

    if mode == 2:
        print("wrong is " + wrong)
        print()

    # Iterate by letters in wrong
    for letter in wrong:
        
        # Check if letter appears in ANSWER
        count = ANSWER.count(letter)
        if count == 0:
            # If not, eliminate words containing letter
            temp_list = []
            temp_list = [ word for word in current_answers_list if not letter in word ]

            if mode == 2:
                print("After solving for words which do not contain " + letter + ", " + str(len(temp_list)) + " possible answers remain.")
                print()

            current_answers_list = temp_list
            

            # Now do the same for valid guesses
            temp_guess_list = []
            temp_guess_list = [ word for word in abridged_valid_guesses if not letter in word ]
                    
            if mode == 2:
                print("After solving for guesses which do not contain " + letter + ", " + str(len(temp_guess_list)) + " valid guesses remain.")
                print()

            abridged_valid_guesses = temp_guess_list
       
        else:
            # Iterate through ANSWER and eliminate words with letter in same position as "."
            for j, v in enumerate(ANSWER):
                if mode == 2:
                    print(j, ' ', v)
                if v == '.':
                    if mode == 2:
                        print(ANSWER[j] + " is .")
                # If so, find words not containing letter in this position
                    temp_list = []
                    temp_list = [ word for word in current_answers_list if not letter in word[j] ]

                    if mode == 2:
                        print("After solving for " + letter + " in position " + str(j) + ", " + str(len(temp_list)) + " possible answers remain.")
                 
                    current_answers_list = temp_list

                # Now do the same for valid guesses
                    temp_guess_list = []
                    temp_guess_list = [ word for word in abridged_valid_guesses if not letter in word[j] ]
                    
                    if mode == 2:
                        print("After solving for " + letter + " in position " + str(j) + ", " + str(len(temp_guess_list)) + " valid guesses remain.")

                    abridged_valid_guesses = temp_guess_list

        # Tabulate and display results by letter
        current_answers = len(current_answers_list)
        if mode >= 1:
            print("After selecting answers which do not contain " + letter + ",")
            print(str(current_answers) + " words are left.")
            print()

    # Tabulate and display results for Step 3
    current_answers = len(current_answers_list)
    count = len(wrong)
    if count > 1:
        print("After selecting answers which do not match '"  + wrong + "' ,")
        print(str(current_answers) + " words are left from initial " + str(total_answers) )
        print()

    if mode >= 1:
        print("Done with Step 3.")
    print()

    # If answer is found ( len(current_answers) = 1 ), write to ANSWER, and update past answer lists
    if current_answers == 1:
        ANSWER = ''.join(current_answers_list)
        print("Wordle may be solved - assuming editors are using a word from the answer list.")
        print("Answer is: ")
        print(" " + ANSWER)
        print()
        print("Best to check and see if this solution actually solved the puzzle online. If so, proceed.")

        if yesno("Did " + ANSWER + " solve the Wordle puzzle"):
            update_past_answer_list()
            sys.exit("Program completed")
        else:
            print("Perhaps this is a 'curated' answer which could be found in the valid guess list?")
            if yesno("Print the current valid guess list for other possible solutions"):
                for word in abridged_valid_guesses:
                    print(word)
                sys.exit("Program completed")
 
    # Display results for guess
    if yesno("Display current answer list after guess[" + str(i) + "]"):
        for word in current_answers_list:
            print(word)
        print()

    # Show letter frequency in current answer list

    if yesno("Print letter frequency in possible answers from current answers list"):

        # Convert current_answers_list to string
        current_answers_string = ' '.join(current_answers_list)
        
        # Create dict containing letter frequency    
        letter_frequency = {}
        from string import ascii_lowercase as alc
        for k in alc:
            a = current_answers_string.count(k)
            if a >= 1:
                letter_frequency[k] = a
     
        from collections import Counter
        c = Counter(letter_frequency)
        current_answers_sorted = c.most_common()

        print("List of letters by frequency")
        for k, v in current_answers_sorted:
            print(k, ' ', v)


    #
    # Step 4: Check against unused answers, show remaining possible answers and letter frequencies.
    #
    
    if mode >= 1:
        print("Step 4: Check against unused answers, show remaining possible answers and letter frequencies.")
    print()

    # Read unused_answers_list.txt
    try:
        with open("unused_wordle_answers.txt", "r") as unused_answers_file_h:
            unused_answers_list = unused_answers_file_h.readlines()
    except Exception as err:
            print(f"Unexpected error opening {fname} is",repr(err))
            sys.exit("Error, line 819")

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
            sys.exit("Part 4 aborted at line 853")

    # Check current_answers_list against unused_answers_list
    temp_list = []
    for word in current_answers_list:
        if word in unused_answers_list:
            temp_list.append(word)

    #temp_list = [ word for word in current_answers_list if word in unused_answers_list ]

    temp_answers = len(temp_list)
    print("Abridged answer list contains " + str(temp_answers) + " words.")
    print()

    # If answer is found ( temp_answers = 1 ), write to ANSWER, and update past answer lists
    if temp_answers == 1:
        ANSWER = ''.join(temp_list)
        print("Wordle may be solved - assuming editors are using a word from the answer list.")
        print("Answer is: ")
        print(" " + ANSWER)
        print()
        print("Best to check and see if this solution actually solved the puzzle online. If so, proceed.")

        if yesno("Did " + ANSWER + " solve the Wordle puzzle"):
            update_past_answer_list()
            sys.exit("Program completed")
        else:
            print("Perhaps this is a 'curated' answer which could be found in the valid guess list?")
            if yesno("Print the current valid guess list for other possible solutions"):
                for word in abridged_valid_guesses:
                    print(word)
                sys.exit("Program completed")

    if yesno("Print list of possible answers from unused_answers_list"):
        for word in temp_list:
            print(word)
        print()
        
    # Tabulation of letter frequency of words in temp_list

    if yesno("Print letter frequency in possible answers from unused_answers_list"):

        # Convert temp_list to string
        abridged_answers_string = ' '.join(temp_list)
        
        # Create dict containing letter frequency    
        letter_frequency = {}
        from string import ascii_lowercase as alc
        for k in alc:
            a = abridged_answers_string.count(k)
            if a >= 1:
                letter_frequency[k] = a
     
        from collections import Counter
        c = Counter(letter_frequency)
        abridged_answers_sorted = c.most_common()

        print("List of letters by frequency")
        for k, v in abridged_answers_sorted:
            print(k, ' ', v)

    print()
    print("End of Step 4")
    print()


    #
    # Step 5 - Checking list of valid guesses
    #

    # Display remaining valid guesses

    if hard == 1:
        print("You are playing in hard mode.")

    display_valid_guesses()

    # End of Step 5
    

    print("Guesses so far:")
    print(*guess, sep='\n')
    print()

# End of main loop


print ("exiting...")
sys.exit("Program completed")
