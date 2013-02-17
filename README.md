# Info Agent: Breaking the Urgency of News

Updated 17 February 2013

## 30 Second Summary

News, blogs, and social networks demand more and more of our time to process an ever-growing torrent of noise from the small amount of information we really care about. This Python script helps you filter noise from your Twitter and Reddit streams so you can read only the items worthy of your attention and refocus your attention on *doing things* instead of *processing* and *consuming*. This experimental Python script helps us move our attention from urgent distractions to important action.

This script and it's HTML files are all [hosted at Github](https://github.com/mshea/Info-Agent).

## Moving from Urgent to Important

In the most popular self-help book, [7 Habits of Highly Effective People](http://www.amazon.com/dp/0743269519/ref=as_li_ss_til?tag=mikesheanet-20&camp=0&creative=0&linkCode=as4&creativeASIN=0743269519&adid=0AR6MH60DEX0FA59GEMS), Stephen Covey describes how we might move our time, effort, and attention to activities of long-term importance instead of the urgent distractions we face throughout much of our day. Urgency isn't importance, regardless of how most of us act. Covey puts this together in a four-section grid:

<img src="http://mikeshea.net/images/urgent-important.jpg" alt="Stephen Covey's Urgent vs. Important grid">

Ever since 9/11, mainstream news has moved from importance to urgency. We've grown used to the idea that we have to know what's going on **right now**. This attitude has filtered down and propagated to every blog on every topic in which we might be interested. Regardless of the topic, everyone seems out to be the first to break a story, even if the results of that story might not affect us for a year, or ever!

Now it's filtered down to Twitter, a social network built on urgency. We can learn anything that happens the minute it happens by the very people it happened to. Do we really need to know it? Must we spend four hours a day watching Twitter? Must we have a constantly open chat log with the whole planet invited in? Is this *really important* or is it simply an *urgent distraction*?

<img src="http://mikeshea.net/images/urgent_twitter.jpg" alt="Twitter & Reddit, urgent distractions">

I say we have better things to do and better places to put out attention. This script is the coded manifestation of the philosophy that **urgency isn't importance**.

## Outsourcing Our Attention

Thousands to millions of people might monitor the very same feeds of information you do. They follow the same people on Twitter. They read the same news on Reddit. When they like something, they retweet it to share it with those who follow them. Their own brain power processes incoming information and determines what is important.

Instead of working in parallel with all of that brain power, why not work in series? Why not let these other brains work for *you*? Imagine if you could run your own [MapReduce](http://en.wikipedia.org/wiki/MapReduce) cluster across human brains instead of the CPUs of commodity computer systems. This is essentially what Google has done by following hyperlinks across the web to [determine web page relevancy](http://en.wikipedia.org/wiki/PageRank).

Though far from perfect, we have little bits of data we can use to monitor what is important to people and what is not. Twitter retweets and Reddit upvotes are imperfect but systematic ways to determine when someone thought some bit of news was valuable. If we use those people as a net that sits between us and the continuing flow of information, we might let them filter out the little fish so we can catch the big ones.

## Yesterday's News Today

One of the HTML pages included in this script gives us a different way of looking at the news. You can see an example on my own [personal news page](http://mikeshea.net/news/). Rather than showing you all of the news up to the hour, it only shows you news from yesterday, ranked by score, and then all of the news of the previous six days before yesterday, also ranked by score. It won't show you anything from today. You'll see today's news tomorrow.

This seems counterintuitive, I know. Since it only shows you news from yesterday, *you're only going to check it once a day*. There's no reason to check it more than that. Now you can catch up on all the news you care about, pre-filtered by other people, once a day in just a couple of minutes. This moves the urgent distractions of up-to-the-minute Twitter and Reddit surfing to focusing on pre-filtered news of importance read only once a day. Let's look at this on the Covey chart:

<img src="http://mikeshea.net/images/urgent_twitter_important_infoagent.jpg" alt="Twitter & Reddit, urgent distractions">

Letting go of the need to read today's news today is hard to do. We've come to expect that we'll learn about today's news as soon as it happens. Is it important that we do so? Or are news corporations, blogs, and other content creators simply building in a *"sense of urgency"* to keep our eyeballs on their sites and feeds as much as they can? Do we really need this level of information or is it simply a way for advertisers to keep our eyeballs on their ads as often as they can?

## How Does This Script Work?

This program accesses one or more Twitter accounts and Reddit feeds through their respective APIs, pulls down data in JSON, filters the results, stores them in a SQLite database, and then outputs a new JSON file of text and links filtered by source, score, and the lack of any phrases held in the script's blacklist.

The score is determined by running an algorithm on retweets / followers for Twitter and on the number of up-votes for Reddit into a shallow and normalized scoring system. You can change the threshold of the visible score in the parameters.

This program is intended to run every hour as a scheduled event or cron job.

## Dependencies

This program requires the [Tweepy](https://github.com/tweepy/tweepy) Python module to authenticate with [Twitter's 1.1 API](https://dev.twitter.com/docs/api/1.1). This program must be [registered as an application](https://dev.twitter.com/apps) on the Twitter accounts you plan to monitor.

The HTML files use [JQuery](http://jquery.com) and [Moment.js](http://momentjs.com) to process and display the program's JSON output.

## A Breakdown Of the Script's Actions

This script starts by bringing in Twitter data from one or more accounts authenticated through OAuth. It loads 100 tweets from that user's time, finds URLs in those tweets (URLs are required as this program focuses on links), and scores the tweet based on an algorithm. Any tweet with fewer than two retweets isn't included. Two is the minimum number of tweets for this program to pay attention to.

With the score complete, the text, link, date, score, and source are stored in the SQLite links database.

Next, the program hits Reddit, pulling down JSON files from included Reddit URLs. These are likewise scored and stored in the database.

The program then loads links from the database and runs them through two filters. First, any links with a score below the identified threshold are omitted. Second, any items with text containing one or more phrases from the blacklist are omitted. The results are stored in a static JSON file in a web-accessible directory.

The user (you) hits an HTML page that uses [JQuery](http://jquery.com) to load these JSON items and displays them in a web page. This page can be customized any way you see fit. I've included two HTML templates, one for daily news and one for yesterday + last week's news. These pages also use the [Moment.js](http://momentjs.com) Javascript library to parse and display dates.

## Saving You Time and Attention for More Important Things

The whole intent of this script is to save you time and help you redirect your attention to *doing* things instead of just surfing news all the time. As the stream of information grows ever wider, it's important that we have some way to sift through, find the stuff we care about, and ignore the rest. This script helps you use the experience of other people, through retweets and upvotes, to bring the right things to your attention.

## Released Under a Creative Commons License

This script is released under a [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license](http://creativecommons.org/licenses/by-nc-sa/3.0/) so you can distribute it, modify it, and share it as long as you release it under a similar license and attribute the original program to me. 
