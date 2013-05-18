import csv
import itertools
import re
import sys
try:
    import simplejson as json
except ImportError:
    import json


NON_TWITTER_WORD_RE = re.compile(r"[^\w\-'@]")
get_neutral_word = lambda word: NON_TWITTER_WORD_RE.sub('', word.lower().strip())
SENTIMENT_BY_WORD = None


def print_unknown_term_sentiment_estimates(tweet):
    unscored_words = set()
    positive_words = negative_words = 0
    words = tweet.get('text', '').split()
    neutral_words = set(itertools.imap(get_neutral_word, words))
    neutral_words.discard('')
    for word in neutral_words:
        sentiment = SENTIMENT_BY_WORD.get(word)
        if sentiment is not None:
            positive_words += sentiment > 0
            negative_words += sentiment < 0
        else:
            unscored_words.add(word)
    for unscored_word in unscored_words:
        ratio = float(positive_words) / negative_words if negative_words else 0.0
        print '{0} {1}'.format(unscored_word, ratio)

def get_tweets(tweet_file):
    with open(tweet_file, 'r') as f:
        return itertools.imap(json.loads, f)

def get_sentiment_by_word(sentiment_file):
    with open(sentiment_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return dict((get_neutral_word(word), int(sentiment.strip())) 
                    for word, sentiment in reader)

def main():
    sentiment_file, tweet_file = sys.argv[1:3]
    global SENTIMENT_BY_WORD
    SENTIMENT_BY_WORD = get_sentiment_by_word(sentiment_file)
    for tweet in get_tweets(tweet_file):
        print_unknown_term_sentiment_estimates(tweet)

if __name__ == '__main__':
    main()