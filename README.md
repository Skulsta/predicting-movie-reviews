# predicting-movie-reviews

Name of main file: Training.py:

We now have access to:
- Total number of words in:
    - A given review
    - All positive or negative reviews
- The number of unique words in any review
- Possibility to filter reviews with our own stopwords file

The main method is "get_prediction"
-----------------------------------
- It only accepts clean text as input, so before a review can be used, either:
    - Run remove_uncommon_words. This is strict filtering where every word must pass given criterias:
        - The word must exist somewhere whithin at least on positive and one negative review. These have already filtered out stopwords.
        - The word must occurre at least 50 times (not fine tuned this variable) accross either all positive or negative reviews.
    - Run remove_stopwords. Less strict filtering. Removing stopwords from the review and removes words that does not exist in imdb.vocab
    - Run get_text returns clean text without any filtering.
- Goes through every word in the review (that is left if filtered) and uses Multinomial Naive Bayes to return a prediction.
    - More than 0.5 means it's predicted to be a positive review. Less than 0.5 means the opposite.

Missing:
- Needs a lot of optimalization if it is to complete 25 000 test sets during the next decade.
- Implement a method for calculating error rate
    - Tweaking the algorithm to make accurate predictions. Underfitting/Overfitting
- Words ending with a punctuation is not included. Might miss important words because of this. E.g "The movie was amazing."
- There's a microscopic chance that a review will not contain any words after filtering. This will result in an error. More likely
the smaller "most.common" number is in the "filter_words" method.