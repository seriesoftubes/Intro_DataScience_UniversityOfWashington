import collections
import itertools
try:
    import simplejson as json
except ImportError:
    import json
import sys


strip_word = lambda word: word.strip()


def get_words(tweets):
    return itertools.chain(*(itertools.imap(strip_word, tweet['text'].split()) 
                             for tweet in tweets if 'text' in tweet))

def get_tweets(tweet_file):
    with open(tweet_file, 'r') as f:
        return itertools.imap(json.loads, f.readlines())

def main():
    tweet_file = sys.argv[1]
    tweets = get_tweets(tweet_file)
    words = (word for word in get_words(tweets) if word)
    count_by_word = collections.Counter(words)
    total_words = float(len(count_by_word))
    for word, count in count_by_word.most_common():
        print '{0} {1}'.format(word.encode('utf-8'), count / total_words)

if __name__ == '__main__':
    main()