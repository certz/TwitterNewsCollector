#!/usr/bin/python
# -*- coding: utf-8 -*-
from pytz import timezone
import operator
import tweepy
import datetime
import requests

config = {}
execfile("config.py", config)
now = datetime.datetime.now()

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_key"], config["access_secret"])

api = tweepy.API(auth)

statuses = []
todays_statuses = []
top_tweet_htmls = []
tweet_htmls = []

for source in ["WSJJapan","nhk_shutoken","nikkei","kyodo_official", "mainichi"]:
    query = "from:" + source #+ " since:2017-03-11_00:47:00"
    statuses.extend(api.search(q=query,count=100))


for status in statuses:
    if status.created_at> datetime.datetime.utcnow() - datetime.timedelta(1,0,0):
        todays_statuses.append(status)

rt_num_sorted_statuses = sorted(todays_statuses,key=lambda todays_statuses:todays_statuses.retweet_count,reverse=True)

 
for status in rt_num_sorted_statuses[:10]:
   tweet_url = "https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id)
   oembed_endpoint = "https://publish.twitter.com/oembed?align=center&maxwidth=550&url=" + tweet_url
   r = requests.get(oembed_endpoint)
   oembed = r.json()
   top_tweet_htmls.append(oembed["html"])

time_sorted_statuses = sorted(todays_statuses,key=lambda todays_statuses:todays_statuses.created_at,reverse=True)

for status in time_sorted_statuses:
   tweet_url = "https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id)
   tweet_html = status.user.name + ' <a href="' + tweet_url + '">' + status.text + '</a>'
   tweet_htmls.append(tweet_html)

print "Content-Type: text/html;charset=utf-8\n\n\n";
print '<h2 style="text-align:center;">Top News Tweets</h2>'
print '<div style="width:80%;margin: 0 auto;display:block;position:relative;float:none;">'
print  u"".join(top_tweet_htmls).encode("utf-8")
print '</div>'
print '<div style="width:80%;;margin: 0 auto;display:block;position:relative;float:none;"">'
print '<h2>News Tweets</h2>'
print  u"<br>".join(tweet_htmls).encode("utf-8")
print '</div>'
