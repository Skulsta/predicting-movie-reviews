from pathlib import Path
from collections import Counter
import re

data = []

def prepare_data(directory):
    dirpath = Path(directory)
    assert(dirpath.is_dir())
    for x in dirpath.iterdir():
        if x.is_file() and re.search('^\d+?_([1-9]|10)\.txt$', x.name):
            data.append(re.split('\s+', re.sub(r'[^\w\s]','',Path(x).read_text(errors='ignore')).lower()))
        elif x.is_dir():
            data.extend(prepare_data(x))
    return data

# Prints every file like this: PosixPath('aclImdb/train/pos/4290_9.txt')
# pprint(prepare_data('aclImdb'))

test_neg = prepare_data('aclImdb/test/neg')
test_pos = prepare_data('aclImdb/test/pos')
train_neg = prepare_data('aclImdb/train/neg')
train_pos = prepare_data('aclImdb/train/pos')

# print(test_neg[1])
# print(test_pos[1])
# print(train_neg[1])
# print(train_pos[1])

# If we need a Counter
def make_counter(words):
    counter = Counter()
    for word in words:
        counter.update(word)
    print(counter.most_common(3)) #Remember to remove this.
    return counter


# make_counter(test_neg)


