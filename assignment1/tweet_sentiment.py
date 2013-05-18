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


def get_total_sentiment(tweet_text):
    return sum(SENTIMENT_BY_WORD.get(get_neutral_word(word), 0) 
               for word in tweet_text.split())

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
        print float(get_total_sentiment(tweet['text']) 
                    if 'text' in tweet else 0)

if __name__ == '__main__':
    main()