# Reverse-Baron

This is a set of reverse engineering tools made for the browser puzzle game [WordTwist](https://wordtwist.puzzlebaron.com/). The words folder contains three .txt files each with a different purpose, and then a python file that does a lot of the handling and processing of said files. The `words-o.txt` is the full dictionary of unfiltered words. The `words-n.txt` file contains all possible words for all possible boards. The `words-n-md5.txt` file then contains the MD5 codes for all of the words in the `words-n.txt` file. 

*(It is important to note the MD5 codes in the `words-n-md5.txt` file are all the MD5 codes of the filtered words but in full uppercase. This is important because it is how WordTwist stores the words. They are first converted to fully uppercase and then compared to the list of MD5 codes retrieved when the board is created to check if an inputted word exists.)*

The usage of `refine.py` is not exactly streamlined. To use the different utilities simply write the function you want to run at the bottom of the file. The available functions include:
- `condenseAllPossibleWords()` This sorts all of the words in the full dictionary file and only outputs the ones to the filtered words file that fit the criteria for a valid word guess.
- `translateCondensedIntoMD5()` This translates every single word in the sorted word file into MD5. Once again, when these words are encrypted in MD5, they are not encrypted using their original casing. Every word is fully capitalized and then converted into MD5 before being outputted into the file.
- `getWordInfo(word)` This gets the line number of the inputted word in the sorted word file, and then the MD5 code for the inputted word.