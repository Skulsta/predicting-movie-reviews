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
- - Run remove_uncommon_words. This is strict filtering where every word must pass given criterias:
- - - 