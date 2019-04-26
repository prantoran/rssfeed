import feedparser

from flask import Flask
from flask import render_template
from flask import request
import json
import urllib
import urllib.request
import urllib.parse

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()


RSS_FEEDS = {
    'Funny': 'https://9gag-rss.com/api/rss/get?code=9GAGFunny&format=2',
    'Fresh': 'https://9gag-rss.com/api/rss/get?code=9GAGFresh&format=2',
    'Hot': 'https://9gag-rss.com/api/rss/get?code=9GAGHot&format=2',
    'Trending': 'https://9gag-rss.com/api/rss/get?code=9GAG&format=2'
}
app = Flask(__name__)



# openweathermap.org key 6e5115bf81e4d8257d80a79bb67db7a5
@app.route("/")
@app.route("/<tag>")
def get_feed():
    try:

        query = "Funny"
        if "tag" in request.args:
            query = urllib.parse.unquote_plus(request.args.get("tag"))
        
        print("init query:", query)
        
        if not query or query not in RSS_FEEDS:
            query = "Funny"
        print("query:", query)
        
        if cache.has(query) == False:
            feed = feedparser.parse(RSS_FEEDS[query])
            
            template =  render_template("home.html", articles=feed['entries'], header=query, rssFeeds= RSS_FEEDS)
            print("templtate ok")
            cache.set(query, template, timeout=60)

        print("about to return cache")

        return cache.get(query)
    
    except:
        return "no news is good news"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
