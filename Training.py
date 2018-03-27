from collections import Counter
import os.path
import re

# Tests at the bottom.
# Important variables:
# - stopword contains every word we have defined in our stopwords.txt file. Used to filter words from reviews.
# - vocabulary contains every word defined in the imdb.vocab file. Used to filter words from reviews.
# - number_of_positive_reviews is the number of positive reviews. 12 500.
# - number_of_negative_reviews is the number of negative reviews. 12 500.

# Increase will improve accuracy and increase time consumption
# Time estimates: 50 = 3 min, 100 = 6 min and so on
number_of_most_common_words = 50

positive_train_reviews_folder = "aclImdb/train/pos/"
negative_train_reviews_folder = "aclImdb/train/neg/"
positive_train_reviews = os.listdir(positive_train_reviews_folder)
negative_train_reviews = os.listdir(negative_train_reviews_folder)

positive_test_reviews_folder = "aclImdb/test/pos/"
negative_test_reviews_folder = "aclImdb/test/neg/"
positive_test_reviews = os.listdir(positive_test_reviews_folder)
negative_test_reviews = os.listdir(negative_test_reviews_folder)


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
        all_reviews += 1
    for file in negative_train_reviews:
        all_reviews += 1
    return all_reviews


# Split filename by underscore, then split the second half and retrieve the review score.
def get_score(review):
    split_file = review.split("_")
    score = int(split_file[1].split(".")[0])
    if score < 5:
        return -1
    elif score > 5:
        return 1
    else:
        return 2


def get_text(reviews):
    # Join together the text in the reviews for a particular tone.
    # We lowercase to avoid "Not" and "not" being seen as different words, for example.
    return " ".join([r.lower() for r in get_content(reviews)])


def get_vocabulary():
    print("Getting vocabulary from file ...")
    with open("aclImdb/imdb.vocab", 'r', encoding="UTF-8", errors="ignore") as myfile:
        vocabulary = myfile.read().replace('\n', ' ')
    return vocabulary


# Retrieve stopwords from a separate text file containing a list of stopwords. These will later be filtered out to
# achieve higher efficiency and effectiveness.
def get_stopwords():
    print("Getting stopwords from file ...")
    with open("aclImdb/stopwords.txt", 'r', encoding="UTF-8", errors="ignore") as myfile:
        stopwords = myfile.read().replace('\n', ' ')
    return stopwords


# Instantiate the vocabulary.
vocabulary = get_vocabulary()

# Instantiate the stopwords into a variable to be used later.
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


# Total number of words across all files in a folder after being filtered.
def get_total_number_of_words(folder, folder_path):
    total_number_of_words = 0
    for review in folder:
        review_text = folder_path + review
        total_number_of_words += sum(count_text(get_text(review_text)).values())
    return total_number_of_words


# Get all text across every file in a folder after being filtered.
def get_every_word_in_a_folder(folder, folder_path):
    all_text = []
    for review in folder:
        review_text = folder_path + review
        all_text.append(remove_stopwords(review_text))
    actual_text = ' '.join(all_text)
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


# When making fast, simple testing. Increase most_common for more accuracy, decrease for more speed.
def remove_uncommon_words(every_word, number_of_common_words):
    filtered_words = []
    most_common_words = count_text(every_word).most_common(number_of_common_words)
    for word in most_common_words:
        if word[0] in vocabulary:
            filtered_words.append(word[0])
    return filtered_words


# Get all text across every file in a folder after being filtered.
def get_every_word_in_a_folder(folder, folder_path):
    all_text = []
    for review in folder:
        review_text = folder_path + review
        all_text.append(remove_stopwords(review_text))
    actual_text = ' '.join(all_text)
    return actual_text


def filter_words(text):
    result = []
    words = re.split("\s+", get_text(text))
    for word in words:
        if word in most_common_positive_words or word in most_common_negative_words:
            result.append(word)
    return ' '.join(result)


print("Retrieving the most common positive words.")
most_common_positive_words = remove_uncommon_words(every_positive_word, number_of_most_common_words)
print("Retrieving the most common negative words.")
most_common_negative_words = remove_uncommon_words(every_negative_word, number_of_most_common_words)


def word_weights(words, every_word, number_of_words):
    words_and_weights = dict()
    for word in words:
        word_weight = count_text(every_word).get(word) / number_of_words
        words_and_weights[word] = word_weight
    return words_and_weights


print("Calculating word weights for positive words ... ")
positive_word_weights = word_weights(most_common_positive_words, every_positive_word, number_of_positive_words)
print("Calculating word weights for negative words ... ")
negative_word_weights = word_weights(most_common_negative_words, every_negative_word, number_of_negative_words)


def get_prediction(text):
    if not text:
        return 0.5
    text_counts = Counter(re.split("\s", text))
    product_of_positive = 1
    product_of_negative = 1
    for word in text_counts:
        product_of_positive *= positive_word_weights.get(word, 0) + 1 ** text_counts.get(word)
        product_of_negative *= negative_word_weights.get(word, 0) + 1 ** text_counts.get(word)
    prediction = (product_of_positive * probability_of_positive_reviews) / \
                 (product_of_positive * probability_of_positive_reviews + product_of_negative * probability_of_negative_reviews)
    return prediction


def calculate_error(folder, folder_path):
    correct_prediction = 0
    for review in folder:
        actual_score = get_score(review)
        prediction = get_prediction(filter_words(folder_path + review))
        if (prediction > 0.5 and actual_score == 1) or (prediction < 0.5 and actual_score == -1):
            correct_prediction += 1
    print("------------")
    print("Predicted correctly on: " + str(correct_prediction) + " of " + str(len(folder))
          + " reviews")
    print("Error rate:")
    return correct_prediction / len(folder)


# Calling the main functions
print("Calculating positive test reviews ...")
print(calculate_error(positive_test_reviews, positive_test_reviews_folder))

print("Calculating negative test reviews ...")
print(calculate_error(negative_test_reviews, negative_test_reviews_folder))
