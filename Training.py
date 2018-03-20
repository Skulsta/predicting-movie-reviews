import string
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

# An array with every file in the training folders.

positive_train_reviews_folder = "aclImdb/train/pos/"
negative_train_reviews_folder = "aclImdb/train/neg/"
positive_train_reviews = os.listdir(positive_train_reviews_folder)
negative_train_reviews = os.listdir(negative_train_reviews_folder)

test_review = "aclImdb/test/pos/0_10.txt"
test_negative_review = "aclImdb/test/neg/0_2.txt"
test_positive_review = "aclImdb/test/pos/4_10.txt"


# # get_text needs this to get direct access to the text
def get_content(review):
    file_text = open(review, 'r', encoding='UTF-8', errors='ignore')
    text_lines = file_text.readlines()
    file_text.close()
    return text_lines


# Read in the training data. Print length gives 25 000. print result gives all text.
def number_of_reviews():
    all_reviews = 0
    for file in positive_train_reviews:
        # all_reviews += "aclImdb/train/pos/" + file
        all_reviews += 1
    for file in negative_train_reviews:
        # all_reviews += get_content("aclImdb/train/neg/" + file)
        all_reviews += 1
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


def get_vocabulary():
    print("Getting vocabulary from file ...")
    with open("aclImdb/imdb.vocab", 'r', encoding="UTF-8", errors="ignore") as myfile:
        stopwords = myfile.read().replace('\n', ' ')
    return stopwords


# Retrieve stopwords from a seperate text file containing a list of stopwords. These will later be filtered out to
# achieve higher effiency and effectiveness.
def get_stopwords():
    print("Getting stopwords from file ...")
    with open("aclImdb/stopwords.txt", 'r', encoding="UTF-8", errors="ignore") as myfile:
        stopwords = myfile.read().replace('\n', ' ')
    return stopwords


vocabulary = get_vocabulary()

# Instantiate the stopwords into a variable to be used later, so to avoid repeating the process more than necessary.
stopwords = get_stopwords()


# Filters out the stopwords from a given text.
def remove_stopwords(text):
    filtered_words = []
    words = re.split("\s+", get_text(text))
    for word in words:
        if word not in stopwords:
            filtered_words.append(word)
    return ' '.join(filtered_words)

# Split text and counts occurrences of each word in text.
def count_text(text):
    # Split text into words based on whitespace.
    words = re.split("\s+", text)
    # Count up the occurrences of each word.
    return Counter(words)


def array_to_string(array):
    return ' '.join(array)


# Total number of words across all files in a folder after being filtered.
def get_total_number_of_words(folder, folder_path):
    total_number_of_words = 0
    for review in folder:
        review_text = folder_path + review
        total_number_of_words += sum(count_text(get_text(review_text)).values())
    return total_number_of_words


# Get all text accross every file in a folder after being filtered.
def get_every_word_in_a_folder(folder, folder_path):
    all_text = []
    for review in folder:
        review_text = folder_path + review
        all_text.append(remove_stopwords(review_text))
    actual_text = array_to_string(all_text)
    return actual_text


print("Filtering stopwords from every review in training set ...")
every_positive_word = get_every_word_in_a_folder(positive_train_reviews, positive_train_reviews_folder)
every_negative_word = get_every_word_in_a_folder(negative_train_reviews, negative_train_reviews_folder)

# Total number of words in positive and negative reviews after filtering stopwords.
print("Calculating the total number of words within both categories ...")
number_of_positive_words = get_total_number_of_words(positive_train_reviews, positive_train_reviews_folder)
number_of_negative_words = get_total_number_of_words(negative_train_reviews, negative_train_reviews_folder)

# Retrieving the total number of positive and negative training reviews. (12 500 each)
print("Calculating total number of test reviews ...")
number_of_positive_reviews = (len(positive_train_reviews))
number_of_negative_reviews = (len(negative_train_reviews))

# Probability of an arbitrary review being positive or negative. Will be 0.5 for both
print("Calculating the probability of a review being positive or negative ...")
probability_of_positive_reviews = number_of_positive_reviews / number_of_reviews()
probability_of_negative_reviews = number_of_negative_reviews / number_of_reviews()


# When making fast, simple testing.
def remove_uncommon_words(every_word):
    filtered_words = []
    most_common_words = count_text(every_word).most_common(100)
    for word in most_common_words:
        if word[0] in vocabulary:
            filtered_words.append(word[0])
    # for word in count_text(every_negative_word).most_common(100).key():
    #     if filtered_words.__contains__(word):
    #         filtered_words.append(word)
    return filtered_words #' '.join(filtered_words)


# Get all text accross every file in a folder after being filtered.
def get_every_word_in_a_folder(folder, folder_path):
    all_text = []
    for review in folder:
        review_text = folder_path + review
        all_text.append(remove_stopwords(review_text))
    actual_text = array_to_string(all_text)
    return actual_text



def filter_words(text):
    result = []
    words = re.split("\s+", get_text(text))
    for word in words:
        if word in most_common_positive_words or word in most_common_negative_words:
            result.append(word)
    return ' '.join(result)


most_common_positive_words = remove_uncommon_words(every_positive_word)
most_common_negative_words = remove_uncommon_words(every_negative_word)

fake_review = "worst crap"


def get_prediction(text):
    text_counts = Counter(re.split("\s", text))
    product_of_positive = 1
    product_of_negative = 1
    print("Throwing Bayes magic around. This will take some time ...")
    for word in text_counts:
        # print(text_counts.get(word))
        # print(count_text(every_positive_word).get(word))
        # print(count_text(every_negative_word).get(word))
        word_occurrences_in_positive_reviews = count_text(every_positive_word).get(word)
        word_occurrences_in_negative_reviews = count_text(every_negative_word).get(word)
        print(word)
        positive_word_weight = (word_occurrences_in_positive_reviews / number_of_positive_words) ** text_counts.get(word)
        product_of_positive *= positive_word_weight
        negative_word_weight = (word_occurrences_in_negative_reviews / number_of_negative_words) ** text_counts.get(word)
        product_of_negative *= negative_word_weight
        # print("Was checked in both")
    # print("Product of weight of positive and negative")
    # print(product_of_positive)
    # print(product_of_negative)
    print("Result: ")
    # Multinomial Naive Bayes going down here
    prediction = (product_of_positive * probability_of_positive_reviews) / \
                 (product_of_positive * probability_of_positive_reviews + product_of_negative * probability_of_negative_reviews)
    return prediction


"""
# Prints the actual text of a review after filtering stopwords
print("Review text after filtering: " + remove_stopwords(test_review))

# From 99 to 31 words after filtering.
print("\nNumber of unique words in a given review before and after filtering stopwords:")
print(len(count_text(get_text(test_review))))
print(len(remove_stopwords(test_review)))

# Total amount of words in a review
print("\nTotal amount of words in a given review before and after filtering stopwords:")
print(sum(count_text(get_text(test_review)).values()))
print(sum(count_text(remove_stopwords(test_review)).values()))

# Prints every word and how many times it occurres and the total number of words
print("\nUsing count_text and get_text: ")
print(count_text(get_text(test_review)))
print("\nUsing count_text and (equivalent of) get_text after filtering: ")
print(count_text(remove_stopwords(test_review)))

# Total amount of words in positive training reviews
print("\nTotal amount of words in positive training reviews:")
total_number_of_words = 0
for review in positive_train_reviews:
    review_text = get_text(positive_train_reviews_folder + review)
    total_number_of_words += sum(count_text(review_text).values())
print(total_number_of_words)

# Total amount of words in positive reviews after filtering
print("\nTotal amount of words in positive training reviews after filtering:")
total_number_of_words = 0
for review in positive_train_reviews:
    review_text = positive_train_reviews_folder + review
    total_number_of_words += sum(count_text(remove_stopwords(review_text)).values())
print(total_number_of_words)

# Total amount of words in negative training reviews
print("\nTotal amount of words in negative training reviews:")
total_number_of_words = 0
for review in negative_train_reviews:
    review_text = get_text(negative_train_reviews_folder + review)
    total_number_of_words += sum(count_text(review_text).values())
print(total_number_of_words)

# Total amount of words in negative reviews after filtering
print("\nTotal amount of words in negative training reviews after filtering:")
total_number_of_words = 0
for review in negative_train_reviews:
    review_text = negative_train_reviews_folder + review
    total_number_of_words += sum(count_text(remove_stopwords(review_text)).values())
print(total_number_of_words)

# Get all text in negative reviews
print("\nEvery word in negative training reviews after filtering:")
all_text = []
for review in negative_train_reviews:
    review_text = negative_train_reviews_folder + review
    all_text.append(remove_stopwords(review_text))
actual_text = array_to_string(all_text)
print(actual_text)

print("Most common positive words: ")
print(count_text(every_positive_word).most_common(5))
print("Most common negative words: ")
print(count_text(every_negative_word).most_common(5))

print("Positive text sample: {0}".format(every_positive_word[:100]))
print("Negative text sample: {0}".format(every_negative_word[:100]))
"""

# Predict whether a review is positive or negative.
# Use either get_text, remove_stopwords or remove_uncommon_words on the input review.
# New changes has made remove_uncommon obsolete.
# test_positive_review takes 5:30 minutes when using get_text. 3:30 minutes when using remove_stopwords.
# print("Filtering words in review (if using a filtering method) ...")
print(get_prediction(filter_words(test_positive_review)))
