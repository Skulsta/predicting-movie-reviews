# Importing this class because it will likely be usefull
# for counting the number of times an item occur in a list.
from collections import Counter

import os.path
import re

# Gets the first file from pos training folder and
# prints the data. Also, the number of data. Which is one array.
text_file = open("aclImdb/train/pos/0_9.txt", 'r')
lines = text_file.readlines()
print(lines)
print(len(lines))
text_file.close()

# true if this exists and is a file, false if not.
print(os.path.isfile("aclImdb/train/pos/0_9.txt"))


# List every file in the pos training folder
# This one might be important. We can split by underscore and retrieve the review score using regex.
positive_reviews = os.listdir("aclImdb/train/pos")
print(positive_reviews)


def get_real_text(file_path):
    # Some files are not encoded correctly, ignoring those who fail to satisfy us.
    file_text = open(file_path, 'r', encoding='UTF-8', errors='ignore')

    text_lines = file_text.readlines()
    print(text_lines)
    file_text.close()


def get_all_files():
    file_path = "aclImdb/train/pos/" + file
    get_real_text(file_path)


# Split every filename by underscore, then split the second half and retrieve the review score.
counter = 1
for file in positive_reviews:
    splitfile = file.split("_")
    print(splitfile[1].split(".")[0])


def get_text(positive_reviews, score):
    # Join together the text in the reviews for a particular tone.
    # Use lowercase to avoid "Not" and "not" being seen as different words.
    return " ".join([r[0].lower() for r in positive_reviews if r[1] == str(score)])


def count_text(text):
    # Split text into words based on whitespace.
    words = re.split("\s+", text)
    # Count up the occurence of each word.
    return Counter(words)


negative_text = get_text(positive_reviews, -1)
positive_text = get_text(positive_reviews, 1)
# Generate word counts for negative tone.
negative_counts = count_text(negative_text)
# Generate word counts for positive tone.
positive_counts = count_text(positive_text)

# Test stuff
print(negative_text)
print(positive_text)

print("Negative text sample: {0}".format(negative_text[:100]))
print("Positive text sample: {0}".format(positive_text[:100]))