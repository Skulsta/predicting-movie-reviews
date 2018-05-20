from pathlib import Path
from collections import Counter
from itertools import dropwhile
import re
import pickle
import math

stop_words = Path('aclImdb/stopwords.txt').read_text()

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


def make_counter(reviews):
    result = []
    for review in reviews:
        for word in review:
            if word not in stop_words:
                result.append(word)
    return Counter(result)


def prepare_input(review):
    result = []
    for word in review:
        result.append(word)
    return result


def remove_least_common(counter):
    for key, count in dropwhile(lambda key_count: key_count[1] >= 10, counter.most_common()):
        del counter[key]
    return counter


all_train_data = remove_least_common(make_counter(prepare_data('aclImdb/train')))
total_docs = len(prepare_data('aclImdb/train'))
num_of_neg_docs = len(prepare_data('aclImdb/train/neg'))
num_of_pos_docs = len(prepare_data('aclImdb/train/pos'))
pos_logprior = math.log(num_of_pos_docs/total_docs)
neg_logprior = math.log(num_of_neg_docs/total_docs)
total_num_of_words = sum(all_train_data.values())
laplace = 20

def change_word_weights():
    train_neg = remove_least_common(make_counter(prepare_data('aclImdb/train/neg')))
    train_pos = remove_least_common(make_counter(prepare_data('aclImdb/train/pos')))
    pos_word_weights = dict()
    neg_word_weights = dict()
    neg_num_of_words = sum(train_neg.values())
    pos_num_of_words = sum(train_pos.values())
    pos_loglikelihood = dict()
    neg_loglikelihood = dict()


def make_word_weights():
    for word in all_train_data.keys():
        pos_word_weights[word] = train_pos.get(word, 0) + total_num_of_words
        neg_word_weights[word] = train_neg.get(word, 0) + total_num_of_words


def get_loglikelihood():
    for word in all_train_data:
        pos_loglikelihood[word] = math.log((train_pos.get(word, 0) + laplace) /
                sum(pos_word_weights.values()))
        neg_loglikelihood[word] = math.log((train_neg.get(word, 0) + laplace) /
                sum(neg_word_weights.values()))


# make_word_weights()
# get_loglikelihood()

def save_obj(obj, name):
    with open('word_weights/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('word_weights/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# save_obj(pos_loglikelihood, 'pos_loglikelihood')
# save_obj(neg_loglikelihood, 'neg_loglikelihood')

pos_loglikelihood = load_obj('pos_loglikelihood')
neg_loglikelihood = load_obj('neg_loglikelihood')



def get_prediction(review):
    input_counter = prepare_input(review)
    pos_prediction = 1
    neg_prediction = 1
    for word in input_counter:
        if word in all_train_data:
            pos_prediction += (pos_logprior + pos_loglikelihood.get(word))
            neg_prediction += (neg_logprior + neg_loglikelihood.get(word))
    prediction = max(pos_prediction, neg_prediction)
    if prediction is pos_prediction:
        return 1
    else:
        return 0


def calculate_error():
    neg_test_reviews = prepare_data('aclImdb/test/neg')
    pos_test_reviews = prepare_data('aclImdb/test/pos')
    correct_neg_prediction = 0
    correct_pos_prediction = 0

    for review in neg_test_reviews:
        if (get_prediction(review) == 0):
            correct_neg_prediction += 1

    for review in pos_test_reviews:
        if (get_prediction(review) ==  1):
             correct_pos_prediction += 1

    print("------------")
    print("Predicted correctly on: " + str(correct_neg_prediction) + " of " +
            str(len(neg_test_reviews)) + " negative reviews")
    print("Error rate for negative reviews: " + str(correct_neg_prediction /
        len(neg_test_reviews)))
    print("Predicted correctly on: " + str(correct_pos_prediction) + " of " +
            str(len(pos_test_reviews)) + " positive reviews")
    print("Error rate for positive reviews: " + str(correct_pos_prediction /
        len(pos_test_reviews)))
    return ((correct_neg_prediction + correct_pos_prediction) /
            (len(neg_test_reviews) +
            len(pos_test_reviews)))


print("Calculating test reviews ...")
print(calculate_error())
