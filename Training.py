# Importing this class because it will likely be usefull
# for counting the number of times an item occur in a list.
from collections import Counter
import collections

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

# Give it the file path of a text file, and it will read the content.
def get_real_text(file_path):
    # Some files are not encoded correctly, ignoring those who fail to satisfy us.
    file_text = open(file_path, 'r', encoding='UTF-8', errors='ignore')

    text_lines = file_text.readlines()
    print(text_lines)
    file_text.close()


# Iterates through every review in a folder and calls the method to retrieve the content.
def get_all_files():
    for file in positive_reviews:
        file_path = "aclImdb/train/pos/" + file
        get_real_text(file_path)


# Split filename by underscore, then split the second half and retrieve the review score.
def get_score(review):
    split_file = review.split("_")
    score = int(split_file[1].split(".")[0])
    if score < 5:
        return -1
    elif score > 6:
        return 1
    else:
        # Should throw exception instead. Figure out the Python way of doing that whenever.
        return 2


def get_content(review):
    file_text = open(review, 'r', encoding='UTF-8', errors='ignore')

    text_lines = file_text.readlines()
    # print(text_lines)
    file_text.close()
    return text_lines


def real_get_text(reviews, score):
    return " ".join([r.lower() for r in get_content(reviews) if get_score(reviews) == score])


def count_text(text):
    # Split text into words based on whitespace.
    words = re.split("\s+", text)
    # Count up the occurence of each word.
    return Counter(words)


def store_words(text):
    counter = Counter()
    words = re.split("\s+", text)
    counter.update(words)


# Test for one positive review.
# positive = real_get_text("aclImdb/train/pos/0_9.txt", 1)
# negative =  real_get_text("aclImdb/train/pos/0_9.txt", -1)
# print("Hopefully some text: {0}".format(positive[:100]))
# print("Hopefully nothing: {0}".format(negative[:100]))


def all_positive_reviews():
    for file in positive_reviews:
        file_path = "aclImdb/train/pos/" + file
        positive = real_get_text(file_path, 1)
        negative = real_get_text(file_path, -1)
        #print("Hopefully some text: {0}".format(positive[:100]))
        #print("Hopefully nothing: {0}".format(negative[:100]))

        # This counts how many times every word is repeated in the given text
        print(count_text(real_get_text(file_path, 1)))


def count_all_positive():
    all_words = []
    for file in positive_reviews:
        file_path = "aclImdb/train/pos/" + file
        positive = real_get_text(file_path, 1)
        words = re.split("\s+", positive)
        all_words += words
    return Counter(all_words)

print(count_all_positive().most_common(3))




"""
def search(file):
    total_counter = collections.Counter()
    if os.path.isdir(path) == True:
        for root, dirs, files in os.walk(path):
            for file in files:
                words = re.findall('\w+', open(os.path.join(root, file)).read().lower())
                ignore = ('errors', 'undefined')
                counter=collections.Counter(x for x in words if x not in ignore)
                total_counter += counter
                print(total_counter)

    else:
        words = re.findall('\w+', open(path).read().lower())
        counter=collections.Counter(x for x in words)
        total_counter += counter

"""
# path = ("C:/Users/Magnus/Documents/Universitetsarbeid/INFO284/Oblig1/predicting-movie-reviews/aclImdb/train/pos")
# search(path)
