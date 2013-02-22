# Info Agent
# Last Updated 17 February 2013
#
# This program filters news from a set of Twitter accounts and Reddit 
# so you can get the most important news of the day and the week. 
# It's intended to give you a brief look at high-interest news 
# in the least amount of time.
#
# This program reads a series of JSON data from a set of URLs from both
# Twitter and Reddit. It then saves the data to a SQLite3 database, filters
# the results, and puts out a json file to be parsed by Jquery in an HTML page.
# The Twitter portion of this program requires that it is registered as an
# application by the Twitter accounts it follows. The Reddit feeds require
# no authentication.
#
# This program filters information three ways. First, it only follows certain
# feeds of information (your Twitter streams and Reddit feeds) and pulls in
# links from those feeds. Second, it  scores data based on some calculations 
# of retweets or upvotes. Third, it uses a blacklist of key phrases to look 
# for in items you DON'T want to see. The end result is a set of pre-chewed 
# links to information more likely to be of your interest.

import tweepy
import sqlite3
import json
import urllib2
import re
import time
import math

DB_FILE = '/link/to/your/db/directory/info_agent.sqlite'
JSON_FILE = '/link/to/your/web/directory/data.js'
SCORE_THRESHOLD = 50
BLACKLIST = ['badword1', 'badword1','badword3']

reddit_data = [
	(
		'Reddit Games', 
		'http://www.reddit.com/r/Games/top/.json?sort=top&t=week'
	),(
		'Reddit Tech',
		'http://www.reddit.com/r/technology/top/.json?sort=top&t=week'
	)
]

twitter_account_data = [
	{
		'consumer_key': 'yourkeyhere',
		'consumer_secret': 'yourkeyhere',
		'access_token_key': 'yourkeyhere',
		'access_token_secret': 'yourkeyhere',
	}, {
		'consumer_key': 'yourkeyhere',
		'consumer_secret': 'yourkeyhere',
		'access_token_key': 'yourkeyhere',
		'access_token_secret': 'yourkeyhere',
	}
]


def import_reddit(reddit_data):
	try:
		d = urllib2.urlopen(reddit_data[1]).read()
	except urllib2.HTTPError:
		print "Error retrieving "+reddit_data[1]
	j = json.loads(d)
	output = []
	for item in j['data']['children']:
		reddit_score = item['data']['score']
		url = item['data']['url']
		text = item['data']['title']
		reddit_date = str(item['data']['created_utc'])
		date = time.strftime("%Y-%m-%dT%H:%M:%S", 
			time.gmtime(float(reddit_date)))
		score = round(math.log(reddit_score)*10)
		output.append((reddit_data[0], text, url, date, score))
	return output
	
def import_twitter(account_data):
	auth = tweepy.auth.OAuthHandler(account_data['consumer_key'],
			account_data['consumer_secret'])
	auth.set_access_token(account_data['access_token_key'],
			account_data['access_token_secret'])
	api = tweepy.API(auth)

	tweet_data = []
	for tweet in api.home_timeline(count=100, include_rts=1):
		try:
			url = tweet.entities['urls'][0]['expanded_url']
			source = tweet.user.screen_name
			date = str(tweet.created_at).replace(' ','T')
			text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'\
				'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', tweet.text)
			retweets = tweet.retweet_count * 1.0 # Create float
			followers = tweet.user.followers_count * 1.0 # Create float
			if retweets < 2:
				score = 0
			else:
				retweets -= 1 # lower score for low-follower users
				retweet_score = pow(retweets, 1.5) # boost retweets
				raw_score = (retweet_score / followers)*100000 # Build score
				score = round(math.log(raw_score, 1.09)) # Smooth out score
			if (score > 0 and url != '0'):
				tweet_data.append((source, text, url, date, score))
		except:
			url = False
	return tweet_data

def export_to_sqlite(data, db_file):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	try: # Data Model Below
		c.execute('''CREATE TABLE links 
				(source text, 
				text text, 
				url text UNIQUE, 
				date text, 
				score integer);''')
	except:
		error = "table already created..."
	c.executemany('''INSERT OR REPLACE INTO links VALUES (?,?,?,?,?)''', 
					data)
	conn.commit()
	return True

def load_links_from_sqlite(db_file):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	results = []
	tweetquery = conn.cursor()
	tweetquery.execute('''
			select * from links 
			where datetime(date) > date('now','-6 day')
			order by strftime('%Y%m%d', date(date,'-5 hours'))
			desc, score desc;''')
	for result in tweetquery:
		source, text, url, date, score = result
		results.append(result)
	return results

def export_to_json(data, json_file):
	output = []
	for item in data:
		source, text, url, date, score = item
		output.append({'source': source, 'text': text, 'url': url, 
				'date': date, 'score': score})
	with open(json_file, "w") as json_output_handler:
		json_output_handler.write(json.dumps(output))

def filter_from_blacklist(data, blacklist):
	output_data = []
	for item in data:
		source, text, url, date, score = item
		bad_phrase = False
		for phrase in blacklist:
			if phrase.strip() in text:
				bad_phrase = True
		if bad_phrase is not True: output_data.append(item)
	return output_data

def filter_from_score(data, score_threshold):
	output_data = []
	for item in data:
		source, text, url, date, score = item
		if int(score) >= int(score_threshold):
			output_data.append(item)
	return output_data
	
def purge_database(db_file):
	conn = sqlite3.connect(db_file)
	cleandatabase = conn.cursor()
	cleandatabase.execute('''
			delete from links
			where datetime(date) < date('now','-14 day');
			''')
	cleandatabase.execute('vacuum;')
	conn.commit()

def main(reddit_data, twitter_account_data, 
		DB_FILE, JSON_FILE, SCORE_THRESHOLD, BLACKLIST):
	for account in twitter_account_data:
		export_to_sqlite(import_twitter(account), DB_FILE)
	for feed in reddit_data:
		export_to_sqlite(import_reddit(feed), DB_FILE)
	output_data = load_links_from_sqlite(DB_FILE)
	scored_data = filter_from_score(output_data, SCORE_THRESHOLD)
	filtered_data = filter_from_blacklist(scored_data, BLACKLIST)
	export_to_json(filtered_data, JSON_FILE)
	purge_database(DB_FILE)

if __name__ == "__main__":
    main(reddit_data, twitter_account_data,
		DB_FILE, JSON_FILE, SCORE_THRESHOLD, BLACKLIST)