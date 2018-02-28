# Importing this class because it will likely be usefull
# for counting the number of times an item occur in a list.
from collections import Counter

import os.path

# Gets the first file from pos training folder and
# prints the data.
text_file = open("aclImdb/train/pos/0_9.txt", 'r')
lines = text_file.readlines()
print(lines)
print(len(lines))
text_file.close()

# true if this exists and is a file, false if not.
print(os.path.isfile("aclImdb/train/pos/0_9.txt"))


# List every file in the pos training folder
positive_reviews = os.listdir("aclImdb/train/pos")
print(positive_reviews)


# Counting every file in the folder
counter = 1
for file in positive_reviews:
   print(counter)
   counter += 1


