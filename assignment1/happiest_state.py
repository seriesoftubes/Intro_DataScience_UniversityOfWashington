import collections
import csv
try:
    import simplejson as json
except ImportError:
    import json
import itertools
import re
import sys


NON_TWITTER_WORD_RE = re.compile(r"[^\w\-'@]")
get_neutral_word = lambda word: NON_TWITTER_WORD_RE.sub('', word.lower().strip())
SENTIMENT_BY_WORD = None


def get_us_state(tweet):
    if not tweet.get('delete'):
        user = tweet.get('user', {})
        if user.get('lang') == 'en' and user.get('geo_enabled'):
            place = tweet.get('place') or {}
            location_name = place.get('full_name')
            if location_name and place.get('country_code') == 'US':
                #sometimes it's State, City
                state = [word for word in location_name.split(',') 
                         if len(word.strip()) == 2 and word.strip() != 'US']
                return state[0].strip().upper() if state else None

def get_average(numbers):
    return sum(numbers) / float(len(numbers))

def get_average_sentiment(state_and_sentiments, min_sentiments=1):
    sentiments = state_and_sentiments[1]
    if len(sentiments) >= min_sentiments:
        return get_average(sentiments)

def get_total_sentiment(tweet_text):
    return sum(SENTIMENT_BY_WORD.get(get_neutral_word(word), 0) 
               for word in tweet_text.split())

def get_tweets(tweet_file):
    with open(tweet_file, 'r') as f:
        return itertools.imap(json.loads, f.readlines())

def get_happiest_state(tweet_file):
    sentiments_by_state = collections.defaultdict(list)
    tweets = get_tweets(tweet_file)
    for tweet in tweets:
        state = get_us_state(tweet)
        if state and 'text' in tweet:
            sentiment = get_total_sentiment(tweet['text'])
            sentiments_by_state[state].append(sentiment)
    return sorted(sentiments_by_state.iteritems(), 
                  key=get_average_sentiment, reverse=True)[0][0]

def get_sentiment_by_word(sentiment_file):
    with open(sentiment_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return dict((get_neutral_word(word), int(sentiment.strip())) 
                    for word, sentiment in reader)

def init(sentiment_file):
    global SENTIMENT_BY_WORD
    SENTIMENT_BY_WORD = get_sentiment_by_word(sentiment_file)

def main():
    sentiment_file, tweet_file = sys.argv[1:3]
    init(sentiment_file)
    print get_happiest_state(tweet_file)

if __name__ == '__main__':
    main()