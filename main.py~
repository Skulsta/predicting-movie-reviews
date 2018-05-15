from pathlib import Path
from collections import Counter
from itertools import dropwhile
import re

# stop_words = Path('aclImdb/stopwords.txt').read_text()


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


def remove_uncommon_words(counter):
    for key, count in dropwhile(lambda key_count: key_count[1] >= 20,
            counter.most_common()):
        del counter[key]


def make_counter(words):
    counter = Counter()
    for word in words:
        counter.update(word)
    remove_uncommon_words(counter)
    return counter


# Data sets split into Counters
test_neg = make_counter(prepare_data('aclImdb/test/neg'))
test_pos = make_counter(prepare_data('aclImdb/test/pos'))
train_neg = make_counter(prepare_data('aclImdb/train/neg'))
train_pos = make_counter(prepare_data('aclImdb/train/pos'))
all_train_data = train_neg + train_pos
# print(all_data.most_common(5))

total_numb_of_words = sum(all_train_data.values())
neg_num_of_words = sum(train_neg.values())
pos_num_of_words = sum(train_pos.values())
# words_and_weights = dict()

def list_to_counter(review):
    if isinstance(review, list):
        text = ' '.join(review)
        words = re.split('\s+', text)
    return Counter(words)


pos_word_weights = dict()
neg_word_weights = dict()

def make_word_weights():
    gamma = 1
    for word in all_train_data.keys():
        if word in train_pos.keys():
            pos_word_weights[word] = (train_pos.get(word) / pos_num_of_words) * gamma
        if word in train_neg.keys():
            neg_word_weights[word] = (train_neg.get(word) / neg_num_of_words) * gamma


make_word_weights()

def get_prediction(review):
    input_counter = list_to_counter(review)
    probability_of_positive_reviews = 0.5
    probability_of_negative_reviews = 0.5
    product_of_pos = 1
    product_of_neg = 1
    for word in input_counter.keys():
        product_of_pos *= (pos_word_weights.get(word, 0) + 1 **
                input_counter.get(word))
        product_of_neg *= (neg_word_weights.get(word, 0) + 1 **
                input_counter.get(word))
    prediction = ((product_of_pos * probability_of_positive_reviews) /
            ((product_of_pos * probability_of_positive_reviews) +
                (product_of_neg * probability_of_negative_reviews)))
    return prediction


print(get_prediction(prepare_data('aclImdb/test/neg')[23]))
print(get_prediction(prepare_data('aclImdb/test/pos')[23]))

# print("Negative reviews: ")
# run_test_set('aclImdb/test/neg')

# print("\nPositive reviews: ")
# run_test_set('aclImdb/test/pos')

def calculate_error():
    neg_test_reviews = 'aclImdb/test/neg'
    pos_test_reviews = 'aclImdb/test/pos'
    correct_neg_prediction = 0
    correct_pos_prediction = 0

    for review in prepare_data(neg_test_reviews):
        if (get_prediction(review) < 0.5):
            correct_neg_prediction += 1

    for review in prepare_data(pos_test_reviews):
        if (get_prediction(review) > 0.5):
             correct_pos_prediction += 1

    print("------------")
    print("Predicted correctly on: " + str(correct_neg_prediction) + " of " +
            str(len(prepare_data(neg_test_reviews))) + " negative reviews")
    print("Error rate for negative reviews: " + str(correct_neg_prediction /
        len(prepare_data(neg_test_reviews))))
    print("Predicted correctly on: " + str(correct_pos_prediction) + " of " +
            str(len(prepare_data(pos_test_reviews))) + " positive reviews")
    print("Error rate for positive reviews: " + str(correct_pos_prediction /
        len(prepare_data(pos_test_reviews))))
    return (correct_neg_prediction + correct_pos_prediction) / (len(prepare_data(neg_test_reviews)) +
            len(prepare_data(pos_test_reviews)))


print("Calculating test reviews ...")
print(calculate_error())

