from pathlib import Path
from collections import Counter
from itertools import dropwhile
import re
import pickle
import math

def get_stop_words():
    stop_words = []
    filepath = Path('aclImdb/stopwords.txt').read_text()
    return re.split('\s+', filepath)


def prepare_text(text):
    return re.split('\s+', re.sub(r'[^\w\s]','', text).lower())


stop_words = get_stop_words()


def prepare_data(directory):
    data = []
    dirpath = Path(directory)
    assert(dirpath.is_dir())
    for x in dirpath.iterdir():
        if x.is_file() and re.search('^\d+?_([1-9]|10)\.txt$', x.name):
            data.append(re.split('\s+',
            re.sub(r'[^\w\s]','',Path(x).read_text()).lower()))
        elif x.is_dir():
            data.extend(prepare_data(x))
    return data


# Every review. Array of arrays. Punctuation removed. Everything is lower case.
pos_reviews = prepare_data('aclImdb/train/pos')
neg_reviews = prepare_data('aclImdb/train/neg')
all_reviews = pos_reviews + neg_reviews

pos_test_reviews = prepare_data('aclImdb/test/pos')
neg_test_reviews = prepare_data('aclImdb/test/neg')

# Logprior. Probability of an arbritrary review being positive or negative. Using log.
pos_logprior = len(pos_reviews) / len(all_reviews)
neg_logprior = len(neg_reviews) / len(all_reviews)

def remove_uncommon_words(counter):
    for key, count in dropwhile(lambda key_count: key_count[1] > 10, counter.most_common()):
        del counter[key]
    return counter


def remove_stop_words(counter):
    for word in stop_words:
        del counter[word]
    return counter


def make_counter(array_of_arrays):
    counter = Counter()
    for review in array_of_arrays:
        counter.update(review)
    remove_uncommon_words(counter)
    remove_stop_words(counter)
    return counter


# Create Counters and remove uncommon words.
counter_all_reviews = make_counter(all_reviews)
counter_pos_reviews = make_counter(pos_reviews)
counter_neg_reviews = make_counter(neg_reviews)

def get_word_weight():
    pos_word_weights = 0
    neg_word_weights = 0
    for word in counter_all_reviews:
        pos_word_weights += (counter_pos_reviews.get(word, 0) +
                1)
        neg_word_weights += (counter_neg_reviews.get(word, 0) +
                1)
    return pos_word_weights, neg_word_weights


def get_loglikelihood():
    pos_word_weights, neg_word_weights = get_word_weight()
    pos_loglikelihood = dict()
    neg_loglikelihood = dict()
    for word in counter_all_reviews:
        pos_loglikelihood[word] = ((counter_pos_reviews.get(word, 0) + 0.1) /
            pos_word_weights)
    for word in counter_all_reviews:
        neg_loglikelihood[word] = ((counter_neg_reviews.get(word, 0) + 0.1) /
            neg_word_weights)
    return pos_loglikelihood, neg_loglikelihood


def save_obj(obj, name):
    with open('loglikelihoods/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('loglikelihoods/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


pos_loglikelihood, neg_loglikelihood = get_loglikelihood()
save_obj(pos_loglikelihood, 'pos_loglikelihood')
save_obj(neg_loglikelihood, 'neg_loglikelihood')

pos_loglikelihood = load_obj('pos_loglikelihood')
neg_loglikelihood = load_obj('neg_loglikelihood')


def get_prediction(review):
    pos_prediction = 0
    neg_prediction = 0
    for word in review:
        if word in counter_pos_reviews and word in counter_neg_reviews:
            pos_prediction += (math.log(pos_logprior) +
                    math.log(pos_loglikelihood.get(word, 0)))
            neg_prediction += (math.log(neg_logprior) +
                    math.log(neg_loglikelihood.get(word, 0)))
    if max(pos_prediction, neg_prediction) is pos_prediction:
        return 1
    elif max(pos_prediction, neg_prediction) is neg_prediction:
        return 0
    else:
        print('Something went very wrong when predicting class of: ' + review)


def calculate_error():
    correct_pos_prediction = 0
    correct_neg_prediction = 0

    for review in pos_test_reviews:
        if (get_prediction(review) == 1):
            correct_pos_prediction += 1

    for review in neg_test_reviews:
        if (get_prediction(review) == 0):
            correct_neg_prediction += 1

    print("Predicted correctly on: " + str(correct_pos_prediction) + " out of "
            + str(len(pos_reviews)) + " positive reviews")
    print("Error rate for positive reviews: " + str(correct_pos_prediction /
        len(pos_reviews)))
    print("Predicted correctly on: " + str(correct_neg_prediction) + " out of "
            + str(len(neg_reviews)) + " negative reviews")
    print("Error rate for negative reviews: " + str(correct_neg_prediction /
        len(neg_reviews)))
    return ((correct_pos_prediction + correct_neg_prediction) /
            (len(pos_reviews) + len(neg_reviews)))


print("Calculating test reviews ...")
print(calculate_error())


def temporary_tests():
    sample_text = 'such an awesome and wonderful movie. Just great.'
    print(prepare_text(sample_text))
    print(get_prediction(prepare_text(sample_text)))

    print(pos_loglikelihood.get('amazing'))
    print(neg_loglikelihood.get('amazing'))

    for review in pos_test_reviews[:2]:
        print(review)


temporary_tests()
