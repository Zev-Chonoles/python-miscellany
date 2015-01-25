#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from subprocess import Popen, PIPE


# In the command line, the user should type
#
#  ./pdf-word-stats.py <filename.pdf>
#
filename = sys.argv[1]


# Use the "PDFMiner" module, send resulting text to stdout
# for efficiency (don't capture entire output in string)
# http://www.unixuser.org/~euske/python/pdfminer/index.html
# http://axialcorps.com/2013/09/27/dont-slurp-how-to-read-files-in-python/
proc = Popen(['pdf2txt.py', filename], stdout = PIPE)


# Initializing dictionaries; format will be
#
#   (word or pair) : how many times it occurs
#
word_freqs = {}
pair_freqs = {}


# Words that will be disregarded
irrelevant_words = ['the',  'let',  'such',  'that',  'and',  'hence', 'for',
                    'show', 'are',  'its',   'also',  'from', 'can',   'may',
                    'has',  'but',  'iff',   'this',  'each', 'not',   'all',
                    'any',  'with', 'there', 'therefore']

def is_relevant(my_string):
    if (my_string not in irrelevant_words) and (len(my_string) >= 3):
        return True
    else:
        return False


# Process the piped output from above, line-by-line
# http://stackoverflow.com/q/2804543
# https://docs.python.org/2/library/subprocess.html#subprocess.Popen.stdout
# [TO-DO]: Ask someone who knows what they're doing, check that it really is line-by-line
# [TO-DO]: Save previous line, use it to glue together words split by line breaks
for line in proc.stdout:
    
    # Correct any LaTeX ligatures
    # https://docs.python.org/2/library/re.html#re.sub
    # [TO-DO]: switch to new regex package? https://pypi.python.org/pypi/regex
    line = re.sub('ﬀ','ff', line)
    line = re.sub('ﬁ',  'fi', line)
    line = re.sub('ﬃ','ffi',line)
    line = re.sub('ﬂ',  'fl', line)
    line = re.sub('ﬄ','ffl',line)
    
    # Get rid of newline characters
    line = line.replace("\n", " ")
    
    # [TO-DO]: Get rid of punctuation
    # http://stackoverflow.com/q/265960
    # line = unicode(line, 'ascii', 'ignore')

    # [TO-DO]: Get rid of hexadecimal UTF8 escapes (look like \xHH)
    # Sometimes words are captured with \x0c which seems to be a newline character

    # [TO-DO]: Get rid of PDF CID font references (look like (cid:N))

    # Force lowercase
    line = line.lower()

    # Split into words
    word_list = line.split(" ")

    # Update word frequencies using data from this line
    for word in word_list:
        if is_relevant(word):
            word_freqs[word] = word_freqs.get(word, 0) + 1

    # Update pair frequencies using data from this line
    pair_list = []
    for i in range(len(word_list)-2):
        if is_relevant(word_list[i]) and is_relevant(word_list[i+1]):
            pair_list.append([word_list[i],word_list[i+1]])
    for pair in pair_list:
        pair_as_word = pair[0] + " " + pair[1]
        pair_freqs[pair_as_word] = pair_freqs.get(pair_as_word, 0) + 1

    # [TO-DO]: Combine freqs for plurals


# Sort frequencies lowest to highest
sorted_word_freqs = sorted(word_freqs.items(), key=lambda x: x[1])
sorted_pair_freqs = sorted(pair_freqs.items(), key=lambda x: x[1])


# Sort frequencies highest to lowest
# http://stackoverflow.com/a/12336121
sorted_word_freqs.reverse()
sorted_pair_freqs.reverse()


# Print highest words, highest pairs
def pretty_print_list_of_pairs(my_list):
    max_length = 0
    for i in range(len(my_list)):
        max_length = max(max_length,len(repr(my_list[i][0])))
    for pair in my_list:
        space_length = max_length - len(repr(pair[0])) - len(str(pair[1])) + 3
        space = " " * space_length
        print repr(pair[0]), space, pair[1], "  ", pair[0]

pretty_print_list_of_pairs(sorted_word_freqs[:20])
print("\n---------------------\n")
pretty_print_list_of_pairs(sorted_pair_freqs[:20])










