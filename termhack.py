"""termhack.py
Find the best candidates for the word finding to hack a terminal in Fallout 3
http://fallout.wikia.com/wiki/Terminal#Hacking_Terminals"""

import sys

def header(text, char="-"):
    print(char*len(text)+'\n'+text+'\n'+char*len(text))

def print_list():
    for i, word in enumerate(wordlist):
        print(str(i) + ':', word) 

def ask_guess(best=False):
    global best_candidate  
    if best:
        default = best_candidate
    else:
        default = 0
    s = raw_input('guess? (default ' + str(default) + ': ' + wordlist[default] + ') ')
    if not s:
        if best:
            s = str(best_candidate)
        else:
            s = '0'
    return int(s)

def ask_result(guess):
    while True:
        s = raw_input('result for ' + wordlist[guess] + '? ')
        if s: return s

def score_word(word1, word2):
    score = 0
    for i, letter in enumerate(word1):
        if letter == word2[i]:
            score = score + 1
    return score

def score_words():
    scores = []
    for i, word in enumerate(wordlist):
        total = 0
        for i2, word2 in enumerate(wordlist):
            total = total + score_word(word, word2)
        scores.append(total)
    return scores

def words_with_score(score, scores):
    s = ''
    best_scores = []
    global best_candidate
    for i, word in enumerate(wordlist):
        if score == scores[i]:
            s = s + ' ' + word
            best_scores.append(i)
    best_candidate = best_scores[0]
    return s.strip()

def diff_words(word1, word2):
    common = 0
    for i, letter in enumerate(word1):
        if letter == word2[i]:
            common = common + 1
    return common

def get_results(guess):
    results = []
    for i, word in enumerate(wordlist):
        #print('common ' + wordlist[guess] + ' ' + wordlist[i] + ' = ' + str(diff_words(wordlist[i], wordlist[guess])) + '/' + str(wordlength))
        results.append(diff_words(wordlist[i], wordlist[guess]))
    return results

def get_candidates(result, results):
    s = ''
    newlist = []
    for i, word in enumerate(wordlist):
        if int(result) == results[i]:
            s = s + wordlist[i] + ' '
            newlist.append(wordlist[i])
    s.strip()
    if not s:
        print('Error: no candidate!')
        sys.exit()
    else:
        print('candidate(s):', s)
    return newlist

def guess_pass(count):
    global wordlist
    if count == 4:
        header('WARNING, last guess before terminal lock!')
    else:
        header('guess ' + str(count))
    scores = score_words()
    print_list()
    print('best candidate(s):', words_with_score(max(scores), scores))
    guess = ask_guess(True)
    results = get_results(guess)
    result = ask_result(guess)
    if result == str(wordlength):
        print('Hack done!')
        sys.exit()
    wordlist = get_candidates(result, results)



header('Fallout 3 terminal hack', '=')

# IMPORTANT :
# a letter is correct only if it is in the right spot.

with open('words.txt') as f:
    wordlist = f.read().split("\n")

wordlength = len(wordlist[0])
results = []
best_candidate = 0

tries = 4
ask_tries = raw_input('# tries? (default ' + str(tries) + ') ')
if ask_tries: tries = ask_tries

for i in range(1,tries+1):
	guess_pass(i)
