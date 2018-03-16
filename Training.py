# Importing this class because it will likely be useful
# for counting the number of times an item occur in a list.
from collections import Counter
import collections

import os.path
import re

# Gets the first file from pos training folder and
# prints the data. Also, the number of data. Which is one array.

# true if this exists and is a file, false if not.
# print(os.path.isfile("aclImdb/train/pos/0_9.txt"))

# List every file in the pos training folder
# This one might be important. We can split by underscore and retrieve the review score using regex.
from email.mime import base

positive_reviews = os.listdir("aclImdb/train/pos")
#print(positive_reviews)

negative_reviews = os.listdir("aclImdb/train/neg")
#print(negative_reviews)


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

# Get text without worrying about the stupid score.
def retrieve_text(review):
    return " ".join([r.lower() for r in get_content(review)])


def count_text(text):
    # Split text into words based on whitespace.
    words = re.split("\s+", text)
    # Count up the occurence of each word.
    return Counter(words)


def store_words(text):
    counter = Counter()
    words = re.split("\s+", text)
    counter.update(words)


def all_positive_reviews():
    for file in positive_reviews:
        file_path = "aclImdb/train/pos/" + file
        positive = real_get_text(file_path, 1)
        negative = real_get_text(file_path, -1)
        # print("Hopefully some text: {0}".format(positive[:100]))
        # print("Hopefully nothing: {0}".format(negative[:100]))

        # This counts how many times every word is repeated in the given text
        print(count_text(real_get_text(file_path, 1)))


def count_all_positive():
    all_words = []
    for file in positive_reviews:
        file_path1 = "aclImdb/train/pos/" + file
        positive = real_get_text(file_path1, 1)
        words = re.split("\s+", positive)
        all_words += words
    return Counter(all_words)


def count_all_negative():
    all_words = []
    for file in negative_reviews:
        file_path2 = "aclImdb/train/neg/" + file
        negative = real_get_text(file_path2, -1)
        words = re.split("\s+", negative)
        all_words += words
    return Counter(all_words)


# Only retrieve words once.
all_negative_words = count_all_negative()
all_positive_words = count_all_positive()


def total_of_positive_words():
    all_words = []
    for file in positive_reviews:
        file_path1 = "aclImdb/train/pos/" + file
        positive = real_get_text(file_path1, 1)
        words = re.split("\s+", positive)
        if not words.equals("this"):
            all_words += words
        totalNum = len(all_words)
    return totalNum


def total_of_negative_words():
    all_words = []
    for file in negative_reviews:
        file_path2 = "aclImdb/train/neg/" + file
        negative = real_get_text(file_path2, -1)
        words = re.split("\s+", negative)
        if not words.equals("this"):
            all_words += words
        totalNum = len(all_words)
    return totalNum


total_pos = count_all_positive()
total_neg = count_all_negative()


def calculating_neg_weights(word):
    res = (all_negative_words.get(word, 0) + 1) / total_neg
    return res


def calculating_pos_weights(word):
    res = (all_positive_words.get(word, 0) + 1) / total_pos
    return res


#print(calculating_neg_weights("the"))

#print(total_of_positive_words())

#print(total_of_negative_words())

# print((count_all_negative().get("the")) / total_of_negative_words())


test_review = "aclImdb/train/pos/0_9.txt"

def get_y_count(reviews, score):
    # Compute the count of each classification occuring in the data
    return len([r for r in reviews if get_score(r) == score])

positive_review_count = get_y_count(positive_reviews, 1)
negative_review_count = get_y_count(negative_reviews, -1)

prob_positive = positive_review_count / (positive_review_count + negative_review_count)
prob_negative = negative_review_count / (positive_review_count + negative_review_count)


test_pos = "aclImdb/test/pos/0_10.txt"

def make_class_predictions(text, counts, class_prob, class_count):
    prediction = 1
    text_counts = Counter(re.split("\s", text))
    for word in text_counts:
        # For every word in the text, we get the number of times that word occured in the reviews for a given class, add alpha to smooth the value, and divide by the total number of words in the class (plus the class_count to also smooth the denominator).
        # Smoothing ensures that we don't multiply the prediction by 0 if the word didn't exist in the training data.
        # We also smooth the denominator counts to keep things even.
        prediction *= text_counts.get(word) * ((counts.get(word, 0) + 350) / (sum(counts.values()) + class_count))
    return prediction * class_prob


prob_neg = make_class_predictions(retrieve_text(test_pos), all_negative_words, prob_negative, negative_review_count)
prob_pos = make_class_predictions(retrieve_text(test_pos), all_positive_words, prob_positive, positive_review_count)
print(prob_neg)
print(prob_pos)


def pos_or_neg(prob_neg, prob_pos):
    if prob_pos > prob_neg:
        return 1
    elif prob_pos < prob_neg:
        return -1
    else:
        return 0

print(pos_or_neg(prob_neg, prob_pos))

def error_rate(predicted, actual):
    # for file in reviews:
        print("wo")
# get_score(test_pos)


# As you can see, we can now generate probabilities for which class a given review is part of.
# The probabilities themselves aren't very useful -- we make our classification decision based on which value is greater.
# print("Review for test_pos: {0}".format(retrieve_text(test_pos)))
# print("Negative prediction: {0}".format(make_class_predictions(retrieve_text(test_pos), all_negative_words, prob_negative, negative_review_count)))
# print("Positive prediction: {0}".format(make_class_predictions(retrieve_text(test_pos), all_positive_words, prob_positive, positive_review_count)))

# print("Review for test_review: {0}".format(retrieve_text(test_review)))
# print("Negative prediction: {0}".format(make_class_predictions(retrieve_text(test_review), all_negative_words, prob_negative, negative_review_count)))
# print("Positive prediction: {0}".format(make_class_predictions(retrieve_text(test_review), all_positive_words, prob_positive, positive_review_count)))





"""
def real_bayes_pos(text):
    pred1 = 1
    pred2 = 1
    smoothing = 0.1
    text_counts = Counter(re.split("\s+", text))
    for word in text_counts:
        print(word)
        if word in all_positive_words:
            print(pred1)
            pred1 *= calculating_pos_weights(word)
        if word in all_negative_words:
            print(pred2)
            pred2 *= calculating_neg_weights(word)
    res = (pred1*prob_pos)/((pred1*prob_pos) + (pred2*prob_neg))
    return res
"""

print("Where real shit happens")
print()

# print(real_bayes_pos(retrieve_text(test_pos)))


def train_all_positives():
    for file in negative_reviews:
        file_path = "aclImdb/train/neg/" + file
        print()
        print("Negative prediction: {0}".format(make_class_predictions(retrieve_text(file_path), all_negative_words, prob_negative, negative_review_count)))
        print("Positive prediction: {0}".format(make_class_predictions(retrieve_text(file_path), all_positive_words, prob_positive, positive_review_count)))

# Warning: uncomment the sentence below and shit will go on forever.
# train_all_positives()
