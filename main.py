from pathlib import Path
from collections import Counter
import re

data = []

def prepare_data(directory):
    dirpath = Path(directory)
    assert(dirpath.is_dir())
    for x in dirpath.iterdir():
        if x.is_file() and re.search('^\d+?_[1-9]\.txt$', x.name):
            data.append(re.split('\s+', re.sub(r'[^\w\s]','',Path(x).read_text(errors='ignore')).lower()))
        elif x.is_dir():
            data.extend(prepare_data(x))
    return data

# Prints every file like this: PosixPath('aclImdb/train/pos/4290_9.txt')
# pprint(prepare_data('aclImdb'))

prepare_data('aclImdb')

counter = Counter()
# If we need a Counter
def make_counter():
    for word in data:
        counter.update(word)
    print(counter.most_common(3)) #Remember to remove this.


# make_counter()

