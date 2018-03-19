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
test_negative_review = "aclImdb/train/neg/1_1.txt"
test_positive_review = "aclImdb/train/pos/5_10.txt"

# # get_text needs this to get direct access to the text
def get_content(review):
    file_text = open(review, 'r', encoding='UTF-8', errors='ignore')
    text_lines = file_text.readlines()
    file_text.close()
    return text_lines


# Read in the training data. Print length gives 25 000. print result gives all text.
def number_of_reviews():
    all_reviews = 0
    for file in positive_reviews:
        # all_reviews += "aclImdb/train/pos/" + file
        all_reviews += 1
    for file in negative_reviews:
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


def get_stopwords():
    print("Getting stopwords from file ...")
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
    return ' '.join(array)


def remove_stopwords(text):
    words = re.split("\s+", get_text(text))
    for word in list(words):
        if word in stopwords:
            words.remove(word)
    return ' '.join(words)

# Total number of words across all files in a folder after being filtered.
def get_total_number_of_words(folder, folder_path):
    total_number_of_words = 0
    for review in folder:
        review_text = folder_path + review
        total_number_of_words += sum(count_text(remove_stopwords(review_text)).values())
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
every_positive_word = get_every_word_in_a_folder(positive_reviews, positive_reviews_folder)
every_negative_word = get_every_word_in_a_folder(negative_reviews, negative_reviews_folder)

# Total number of words in positive and negative reviews after filtering stopwords.
print("Calculating the total number of words within both categories ...")
number_of_positive_words = get_total_number_of_words(positive_reviews, positive_reviews_folder)
number_of_negative_words = get_total_number_of_words(negative_reviews, negative_reviews_folder)

# Retrieving the total number of positive and negative training reviews. (12 500 each)
print("Calculating total number of test reviews ...")
number_of_positive_reviews = (len(positive_reviews))
number_of_negative_reviews = (len(negative_reviews))

# Probability of an arbitrary review being positive or negative. Will be 0.5 for both
print("Calculating the probability of an arbitrary review being positive or negative")
probability_of_positive_reviews = number_of_positive_reviews / number_of_reviews()
probability_of_negative_reviews = number_of_negative_reviews / number_of_reviews()


# Where we left of. Testing.
fake_review = "the world is lovely amazing"
def get_word_weight(text):
    text_counts = Counter(re.split("\s", text))
    product_of_positive = 1
    product_of_negative = 1
    accepted_word = False
    print("Throwing Bayes magic around. This will take some time ...")
    for word in text_counts:
        print(word)
        print(text_counts.get(word))
        print(count_text(every_positive_word).get(word))
        print(count_text(every_negative_word).get(word))
        word_occurences_in_positive_review = count_text(every_positive_word).get(word)
        word_occurences_in_negative_review = count_text(every_negative_word).get(word)
        if word_occurences_in_positive_review.get is None:
            word_occurences_in_positive_review = 100
        if word_occurences_in_negative_review is None:
            word_occurences_in_negative_review = 100
            if word_occurences_in_positive_review > 100 or word_occurences_in_negative_review > 100:
                positive_word_weight = ((word_occurences_in_positive_review) / number_of_positive_words) ** text_counts.get(word)
                product_of_positive *= positive_word_weight
                negative_word_weight = ((word_occurences_in_negative_review) / number_of_negative_words) ** text_counts.get(word)
                product_of_negative *= negative_word_weight
                print("Was checked in both")
    print("Product of weight of positive and negative")
    print(product_of_positive)
    print(product_of_negative)
    print("Result: ")
    # Multinomial Bayes going down here
    prediction = (product_of_positive * probability_of_positive_reviews) / \
                 (product_of_positive * probability_of_positive_reviews + product_of_negative * probability_of_negative_reviews)
    return prediction
        # positive_word_weight * probability_of_positive_reviews
    # prediction_positive = positive_word_weight / (positive_word_weight + negative_word_weight)
    # prediction_negative = negative_word_weight / (negative_word_weight + positive_word_weight)
    # print("Probability positive: " + str(prediction_positive))
    # print("Probability negative: " + str(prediction_negative))
    # return (probability_of_positive_reviews * prediction_positive) - (probability_of_negative_reviews * prediction_negative)


print(get_word_weight(fake_review))


def make_class_prediction(text):
    prediction = 1
    text_counts = Counter(re.split("\s", text))
    for word in text_counts:
        print(word)
        print(text_counts.get(word))
        print(count_text(every_positive_word).get(word))
        print(count_text(every_negative_word).get(word))
        # For every word in the text, we get the number of times that word occured in the reviews for a given class,
        # add alpha to smooth the value, and divide by the total number of words in the class
        # (plus the class_count to also smooth the denominator).
        # Smoothing ensures that we don't multiply the prediction by 0 if the word didn't exist in the training data.
        # We also smooth the denominator counts to keep things even.
        # print(every_positive_word.get(word) + 1)
        # prediction *= (positive_word_weight / (positive_word_weight + negative_word_weight))
        # print(text_counts.get(word) * ((every_positive_word.get(word) + 1) / (sum(every_positive_word.values()))))
    return prediction * probability_of_positive_reviews

# print(make_class_prediction(remove_stopwords(test_review)))


# print("Review: {0}".format(remove_stopwords(test_negative_review)))
# print("Positive prediction: {0}".format(make_class_prediction(remove_stopwords(test_negative_review), every_positive_word, probability_of_positive_reviews, number_of_positive_reviews)))
# print("Negative prediction: {0}".format(make_class_prediction(remove_stopwords(test_negative_review), every_negative_word, probability_of_negative_reviews, number_of_negative_reviews)))


def make_decision(text):
    # Compute the negative and positive probabilities.
    positive_prediction = make_class_prediction(text, every_positive_word, probability_of_positive_reviews, number_of_positive_reviews)
    negative_prediction = make_class_prediction(text, every_negative_word, probability_of_negative_reviews, number_of_negative_reviews)
    print(positive_prediction)
    print(negative_prediction)

    # We assign a classification based on which probability is greater.
    if negative_prediction > positive_prediction:
      return -1
    return 1


# print(make_decision(remove_stopwords(test_negative_review)))


def get_predictions(folder_file, folder_path):
    for review in folder_file[:5]:
        review_file = folder_path + review
        positive_prediction = make_class_prediction(remove_stopwords(review_file), every_positive_word, probability_of_positive_reviews, number_of_positive_reviews)
        negative_prediction = make_class_prediction(remove_stopwords(review_file), every_negative_word, probability_of_negative_reviews, number_of_negative_reviews)
        print(positive_prediction)
        print(negative_prediction)

        # We assign a classification based on which probability is greater.
        if negative_prediction > positive_prediction:
            print(-1)
        else:
            print(1)


# get_predictions(negative_reviews, negative_reviews_folder)

"""
# TESTS - Uncomment for them deep insights.
# Prints the actual text of a review.
print("Review text before filtering: " + get_text(test_review))

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

# Get all text in negative reviews
print("\nEvery word in negative training reviews after filtering:")
all_text = []
for review in negative_reviews:
    review_text = negative_reviews_folder + review
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