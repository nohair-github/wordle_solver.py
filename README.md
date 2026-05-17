Wordle Solver (wordle_solver.py

This is an assistant to solving Wordle written in python. I basically takes your guesses and eliminates words from the valid guess list and answer list.

Use:
1. Download/clone repository
2.  Execute by 'python3 wordle_solver.py' in terminal.

Versions:
Developed on MacOS 16.1 (21.6.0 Darwin Kernel Version 21.6.0: root:xnu-8020.240.7~1/RELEASE_X86_64),
using MacOS system python 3.10.7
Tested to run on Mint Linux with Python 3.10.6

Version 0.01: adaptation from zsh shell script v0.03 to python 3.10.6+
Version 0.02: added analysis section, added verbosity flags, dropped use of re module, bugfixes.
Version 0.03: further bug fixes, last version with old valid word lists and answer list.
Version 0.04: between Nov 2022 and Feb 2023, NYTimes editors changed the valid word lists and answers lists.
#   Now the answers are "curated" which means? Perhaps any word from original answer list can be used again
#   as the answer - like "snafu" on Apr 9 - or perhaps any word from the valid guess list, or any word at all.
#   Version 0.04 changed so both valid guess list, complete answer list, and unused answer list are analyzed, displayed,
#   and can be checked.

Changes after 10/10/25 for version 0.05:
   Corrected typos
   Moved entry section to function "enter_guess()"
   Debug testing of enter_guess()
   Made quiet mode quieter:
       removed alert in Step 1 that letters are found in guess line 578 & 582
       removed alert in Step 2 that letters are found in guess line 737 & 744
   Cleaned up logic once solution for repeated answers and curated answers is apparent

Changes since 4/27/26: 
   Automatically update answer lists in quiet mode
   Edited update_past_answer_list() and update_unused_answers_list() to exit with warning if answer is apparent repeat
   Kept dev as a procedural script and wrote dev1 version using main() idiom.
