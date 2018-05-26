from train_model import load_obj, prepare_data, get_prediction, prepare_text
import math


def get_logprior():
    pos_reviews = prepare_data('aclImdb/train/pos')
    neg_reviews = prepare_data('aclImdb/train/neg')
    all_reviews = pos_reviews + neg_reviews


    pos_logprior = math.log(len(pos_reviews) / len(all_reviews))
    neg_logprior = math.log(len(neg_reviews) / len(all_reviews))

    return pos_logprior, neg_logprior


def predict_review(*args):
    review = ''
    if args:
        review = prepare_text(args)
    else:
        print('Write your review here: ')
        review = prepare_text(input())
    pos_prediction = 0
    neg_prediction = 0
    for word in review:
        if word in (pos_loglikelihood or neg_loglikelihood):
            pos_prediction += ((pos_logprior) +
                    (pos_loglikelihood.get(word, 0)))
            neg_prediction += ((neg_logprior) +
                    (neg_loglikelihood.get(word, 0)))
    if max(pos_prediction, neg_prediction) is pos_prediction:
        return 1
    elif max(pos_prediction, neg_prediction) is neg_prediction:
        return 0
    else:
        print('Something went very wrong when predicting class of: ' + review)


def get_prediction(prediction):
    result = 'Your review was calculated to be '
    if prediction == 1:
        result += 'positive'
    else:
        result += 'negative'
    print(result)


if __name__ == '__main__':
    print('Please wait a second...')
    pos_loglikelihood = load_obj('pos_loglikelihood')
    neg_loglikelihood = load_obj('neg_loglikelihood')

    pos_logprior, neg_logprior = get_logprior()

    # print(predict_review(prepare_text("Such a terrible and bad movie.")))

    get_prediction(predict_review())

