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
            data.append(re.split('\s+', re.sub(r'[^\w\s]','',Path(x).read_text(errors='ignore')).lower()))
        elif x.is_dir():
            data.extend(prepare_data(x))
    return data

# Every review. Array of arrays. Punctuation removed. Everything is lower case.
pos_reviews = prepare_data('aclImdb/train/pos')
neg_reviews = prepare_data('aclImdb/train/neg')
all_reviews = pos_reviews + neg_reviews

# Logprior. Probability of an arbritrary review being positive or negative. Using log.
pos_logprior = len(pos_reviews) / len(all_reviews)
neg_logprior = len(neg_reviews) / len(all_reviews)

def remove_uncommon_words(counter):
    for key, count in dropwhile(lambda key_count: key_count[1] >= 10, counter.most_common()):
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
        pos_word_weights += (counter_pos_reviews.get(word, 0) + 1)
        neg_word_weights += (counter_neg_reviews.get(word, 0) + 1)
    return neg_word_weights, pos_word_weights


pos_word_weights, neg_word_weights = get_word_weight()


def get_loglikelihood():
    pos_likelihood = dict()
    neg_likelihood = dict()
    for word in counter_pos_reviews:
        pos_likelihood[word] = ((counter_pos_reviews.get(word, 0) + 1) /
                pos_word_weights)
    for word in counter_neg_reviews:
        neg_likelihood[word] = ((counter_neg_reviews.get(word, 0) +
            1) / neg_word_weights)
    return pos_likelihood, neg_likelihood


pos_likelihood, neg_likelihood = get_loglikelihood()
print(pos_likelihood.get('amazing'))
print(neg_likelihood.get('amazing'))

def get_prediction(review):
    pos_prediction = 0
    neg_prediction = 0
    for word in review:
        if word in counter_all_reviews:
            pos_prediction += (pos_logprior + pos_likelihood.get(word))
            neg_prediction += (neg_logprior + neg_likelihood.get(word))
    if max(pos_prediction, neg_prediction) is pos_prediction:
        return 1
    else:
        return 0


sample_text = 'such a terrible and aweful movie. Just so bad. Bad I say.'
print(prepare_text(sample_text))
print(get_prediction(prepare_text(sample_text)))
