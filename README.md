# predicting-movie-reviews

How to:
- Name of main file: Training.py.
- Tests are at the bottom of the file. Uncomment to run.
- Main methods are at the very bottom.
- A screenshot of required folder structure is added in the root folder.


The main method is "calculate_error"
---
- The method need the parameter values "folder" and "folder_path"
    - These are defined at the very top of Training.py.
        - Using positive_test_reviews and positive_test_reviews_folder
         for testing positive test sets.
        - Replace positive with negative to run negative test sets.
- It only accepts clean text as input, so before a review can be used:
    - Run filter_words. This is strict filtering where every word must pass given criterias:
      The word must exist somewhere whithin a given number of most common words in positive or
      negative reviews, which have already filtered out stopwords and vocabulary.
        - stopwords is a .txt file that contains words such as "the" and "a", which we don't want.
        - vocabulary is a .vocab file containing 90 000 words. We only accept words if it appears in this file.
            - This is done to remove words such as "</b" and the like.

    - These two were previously used, might be able to remove them after a little refactoring:

        - Run remove_stopwords. Less strict filtering. Removing stopwords from the review and removes words that does not exist in imdb.vocab
        - Run get_text returns clean text without any filtering.

Other important methods
---
- get_prediction iterates through every word in a review and calculates the product of
every word weight. It then completes the prediction by using Multinomial Naive Bayes.
- word_weights, this method us the most time consuming. Used twice, one time for positive words
and one time for negative words
    - Iterates through every word that survived the previous filtering by stopwords, vocabulary and remove_uncommon_words.
    - Looking up how often the word appears in positive/negative reviews and devides it by the total amount
    of words in positive/negative reviews.

Missing
---
- Tweaking the algorithm to make accurate predictions. Underfitting/Overfitting
- Words ending with a punctuation is not included. Might miss important words because of this. E.g "The movie was amazing."


Best results
------------
- Best time/accuracy combo:
    - Calculating 100 most common words in negative reviews, and positive reviews.
    - Runtime: 6 minutes
    - Accuracy: 0.70 for positive reviews, 0.75 for negative reviews.
- Best accuracy:
    - Calculating 400 most common
    - Runtime: 20 minutes
    - Accuracy: 0.74 for positive reviews, 0.79 for negative reviews.