import random
import numpy as np
import nltk

# https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    print (matrix)
    return (matrix[size_x - 1, size_y - 1])

def nouns(input):
  # https://stackoverflow.com/a/33587889
  # function to test if something is a noun
  is_noun = lambda pos: pos[:2] == 'NN'
  # do the nlp stuff
  tokenized = nltk.word_tokenize(lines)
  nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
  word = random.choice(nouns)
  return word


lines = 'lines is some string of words'
n = nouns(lines)
print(n)
a = 'grandma'
b = 'grandmothers'
print('leven',levenshtein(a, b))
arr = [5, 6, 4, 3, 2]
print(min(arr))

