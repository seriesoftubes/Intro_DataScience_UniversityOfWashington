import collections
import itertools
import operator
import sys
try:
    import simplejson as json
except ImportError:
    import json


def get_hashtags(tweet):
    hashtag_objects = tweet.get('entities', {}).get('hashtags', [])
    return itertools.imap(operator.itemgetter('text'), hashtag_objects)

def get_count_by_hashtag(tweets):
    hashtags = itertools.chain(*itertools.imap(get_hashtags, tweets)) 
    return collections.Counter(hashtags)

def get_tweets(tweet_file):
    with open(tweet_file, 'r') as f:
        return itertools.imap(json.loads, f)

def main():
    tweet_file = sys.argv[1]
    tweets = get_tweets(tweet_file)
    count_by_hashtag = get_count_by_hashtag(tweets)
    for hashtag, count in count_by_hashtag.most_common(10):
        print '{0} {1}'.format(hashtag, float(count))

if __name__ == '__main__':
    main()