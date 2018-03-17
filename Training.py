import plistlib
from collections import Counter
import os.path
import re

# Tests at the bottom.
# Important variables:
# - test_review for testing stuff
# - all_reviews is an array of every test files. 25 000 files. Uncomment if needed. It's at the top.
# - stopword contains every word we have defined in our stopwords.txt file. Used to filter words from reviews.
# - number_of_positive_reviews is the number of positive reviews. 12 500.
# - number_of_negative_reviews is the number of negative reviews. 12 500.

# An array with every file in the folder.

positive_reviews_folder = "aclImdb/train/pos/"
negative_reviews_folder = "aclImdb/train/neg/"
positive_reviews = os.listdir(positive_reviews_folder)
negative_reviews = os.listdir(negative_reviews_folder)

test_review = "aclImdb/train/pos/0_9.txt"


# # get_text needs this to get direct access to the text
def get_content(review):
    file_text = open(review, 'r', encoding='UTF-8', errors='ignore')
    text_lines = file_text.readlines()
    file_text.close()
    return text_lines


# Read in the training data. Print length gives 25 000. print result gives all text.
def read_training_data():
    all_reviews = []
    print("Reading all training data ...")
    for file in positive_reviews:
        all_reviews += "aclImdb/train/pos/" + file
    for file in negative_reviews:
        all_reviews += get_content("aclImdb/train/neg/" + file)
    return all_reviews


# All reviews can now be retrieved with this variable
# all_reviews = read_training_data()


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


def get_text(reviews):
    # Join together the text in the reviews for a particular tone.
    # We lowercase to avoid "Not" and "not" being seen as different words, for example.
    return " ".join([r.lower() for r in get_content(reviews)])


def get_stopwords():
    with open("aclImdb/stopwords.txt", 'r', encoding="UTF-8", errors="ignore") as myfile:
        stopwords = myfile.read().replace('\n', ' ')
    return stopwords


stopwords = get_stopwords()


def count_text(text):
    # Split text into words based on whitespace.
    words = re.split("\s+", text)
    # Count up the occurence of each word.
    return Counter(words)


def array_to_string(array):
    return " ".join([r.lower() for r in array])


def remove_stopwords(text):
    words = re.split("\s+", get_text(text))
    for word in list(words):
        if word in stopwords:
            words.remove(word)
    return ' '.join(words)


# Retrieving the total number of positive and negative traning reviews
number_of_positive_reviews = (len(positive_reviews))
number_of_negative_reviews = (len(negative_reviews))


def make_class_predictions(text, counts, class_prob, class_count):
    prediction = 1
    text_counts = Counter(re.split("\s", text))
    for word in text_counts:
        # For every word in the text, we get the number of times that word occured in the reviews for a given class,
        # add alpha to smooth the value, and divide by the total number of words in the class
        # (plus the class_count to also smooth the denominator).
        # Smoothing ensures that we don't multiply the prediction by 0 if the word didn't exist in the training data.
        # We also smooth the denominator counts to keep things even.
        prediction *= text_counts.get(word) * ((counts.get(word, 0) + 6453.23) / (sum(counts.values()) + class_count))
    return prediction * class_prob


""" # TESTS - Uncomment for them deep insights.
# Prints the actual text of a review.
print(get_text(test_review))

# Prints the actual text of a review after filtering stopwords
print(remove_stopwords(test_review))

# From 99 to 31 words after filtering.
print("\nNumber of unique words in a given review before and after filtering stopwords:")
print(len(count_text(get_text(test_review))))
print(len(remove_stopwords(test_review)))

# Total amount of words in a review
print("\nTotal amount of words in a given review before and after filtering stopwords:")
print(sum(count_text(get_text(test_review)).values()))
print(sum(count_text(' '.join(remove_stopwords(test_review))).values()))

# Prints every word and how many times it occurres and the total number of words
print("\nUsing count_text and get_text: ")
print(count_text(get_text(test_review)))
print("\nUsing count_text and (equivalent of) get_text after filtering: ")
print(count_text(' '.join(remove_stopwords(test_review))))

# Total amount of words in positive training reviews
print("\nTotal amount of words in positive training reviews:")
total_number_of_words = 0
for review in positive_reviews:
    review_text = get_text(positive_reviews_folder + review)
    total_number_of_words += sum(count_text(review_text).values())
print(total_number_of_words)

# Total amount of words in positive reviews after filtering
print("\nTotal amount of words in positive training reviews after filtering:")
total_number_of_words = 0
for review in positive_reviews:
    review_text = positive_reviews_folder + review
    total_number_of_words += sum(count_text(remove_stopwords(review_text)).values())
print(total_number_of_words)

# Total amount of words in negative training reviews
print("\nTotal amount of words in negative training reviews:")
total_number_of_words = 0
for review in negative_reviews:
    review_text = get_text(negative_reviews_folder + review)
    total_number_of_words += sum(count_text(review_text).values())
print(total_number_of_words)

# Total amount of words in negative reviews after filtering
print("\nTotal amount of words in negative training reviews after filtering:")
total_number_of_words = 0
for review in negative_reviews:
    review_text = negative_reviews_folder + review
    total_number_of_words += sum(count_text(remove_stopwords(review_text)).values())
print(total_number_of_words)

# Get all text in positive reviews
print("\nEvery word in negative training reviews after filtering:")
all_text = []
for review in negative_reviews:
    review_text = negative_reviews_folder + review
    all_text.append(remove_stopwords(review_text))
actual_text = array_to_string(all_text)
print(actual_text)
"""
