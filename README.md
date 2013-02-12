# Info Agent

## Why?

This script is designed to help you sort through the constant flow of news, filter it down to what you want, and help you read it in as short amount of time as possible so you can quit worrying about what is changing in the world and go change it yourself. We already spend too much time mindlessly surfing the web, yet we fear that we'll miss the "big news" if we stop looking. This program helps identify links of interest to you, based on your filters, from Twitter and Reddit and displays them in a simple web or mobile interface.

## How?

This program accesses Twitter accounts and Reddit feeds through their respective APIs, pulls down data in JSON, filters the results, stores them in a SQLite database, and then outputs a new JSON file of links filtered by source, score, and the lack of any phrases held in the script's blacklist.

The score is determined by running an algorithm on retweets / followers for Twitter and on the number of up-votes for Reddit into a shallow and normalized scoring system. You can change the threshold of the visible score in the parameters.

This program is intended to run every hour as a scheduled event or cron job.

## Dependencies

This program requires the [Tweepy](https://github.com/tweepy/tweepy) Python module to authenticate with [Twitter's 1.1 API](https://dev.twitter.com/docs/api/1.1). This program must be [registered as an application](https://dev.twitter.com/apps) on the Twitter accounts you plan to monitor.

## A Breakdown Of the Script's Actions

This script starts by bringing in Twitter data from one or more accounts authenticated through OAuth. It loads 100 tweets from that user's time, finds URLs in those tweets (URLs are required as this program focuses on links), and scores the tweet based on an algorithm. Any tweet with fewer than two retweets isn't included. Two is the minimum number of tweets for this program to pay attention to.

With the score complete, the text, link, date, score, and source are stored in the SQLite link database.

Next, the program hits Reddit, pulling down JSON files from included Reddit URLs. These are likewise scored and stored in the database.

The program then imports links from the database and runs them through two filters. First, any links with a score below the identified threshold are omitted. Second, any item text containing one or more phrases from the blacklist are omitted. The results are stored in a static JSON file in a web-accessible directory.

The user (you) hits an HTML page that uses [JQuery](http://jquery.com) to load these JSON items and displays them in a web page. This page can be customized any way you see fit.

## Saving You Time for More Important Things

The whole intent of this script is to save you time. Instead of reading news every moment of every day, you can stick to just once a day or maybe once a week. This script helps you avoid surfing through noise and uses the experience of other people, through retweets and upvotes, to bring the right things to your attention.

## Released Under a Creative Commons License

This script is released under a [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license](http://creativecommons.org/licenses/by-nc-sa/3.0/) so you can distribute it, modify it, and share it as long as you release it under a similar license and attribute the original program to me. 
