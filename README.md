How to run the code:
---
1. Navigate to the project folder in a terminal.
2. Run the python file "predict_review.py"
    - You will be asked to write a review. Hit enter when done, and the program
      will return a string saying whether the review was predicted to be
      positive or negative.
2.1 Already have a ".txt" file with a review?
    - Add the txt file to the "review" folder and type the name of the file
      in the terminal after "predict_review.py". Example if running the code
      using Python 3 and  MacOS will be:

      python3 predict_review.py movie_test_review.txt

      This will run the classification algorithm on the provided test file in the
      review folder.


Training the model
---
The code that were used for training the Multinomial Naive Bayes Classifier is
in the file "train_model.py". This is where important values such as logprior
and loglikelihoods are calculated. The values are saved to files and stored
in the "model_values" folder.

Running the training file will calculate and save these values again,
overriding the existing values in the files. If no changes are made, the exact
same values will override the old values. The call to the "save_model_values" function can be commented out to prevent the code from calculating and override the model values. Running this file also
gives insight into how well the model is doing by printing scores for
precision, recall and accuracy to the terminal.
