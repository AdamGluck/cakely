import urllib2
import re
import facebook
import json
import datetime

def paging(f):
        ''' Decorator for paging through facebook responses '''
        def inner(response):
            data = []
            i=0
            while (True and (i < 10) ):
                data.extend(f(response))
                try:
                    response = json.loads(urllib2.urlopen(response["paging"]["next"]).readlines()[0])
                    i += 1
                except KeyError:
                    break
            return data
        return inner

def get_liked_links(oauth):
    graph = facebook.GraphAPI(oauth)
    friend_count = len(graph.get_connections("me", "friends")['data'])
    links = []
    i = 0
    batch_number = 0
    batch_string = []
    print datetime.datetime.now()

    while (i <= friend_count):
        try: 
            batch_string.append({"relative_url": "method/fql.query?query=" + "SELECT url, image_urls, title, summary, caption FROM link WHERE owner IN (SELECT uid1 FROM friend WHERE uid2 = me() LIMIT 10 OFFSET " + str(i) + ") AND like_info.user_likes=1"})
            batch_number += 1

            if batch_number == 49:
                new_links = graph.request("", post_args={"batch":json.dumps(batch_string)})
                links += new_links
                batch_number = 0
                batch_string = []
            i += 10
            print i
        except Exception:
            i+= 10
            continue

    new_links = graph.request("", post_args={"batch":json.dumps(batch_string)})
    links += new_links
    liked_links = []

    for link in links:
        if link:
            body = json.loads(link[u'body'])
            if len(body) and "error_code" not in body:
                for item in body:
                    liked_links.append(item)
    print "returning liked_links"
    return liked_links

oauth = "CAACEdEose0cBAKKRqtbJBAtjiPLKmdJZBMc7hxoSRUTHqwXWzZA8FHALMbZBgmzk955mYXdJklDPJZB1Nilp8qrZCeEDMpHHuYVoEvzbwxCsYt6uI9JUOX26DaVZC4KwiKOniG50ZARMKwrkUt5IC24TWUIlO6K4FzSkySFKEiJYrQxTqa6PoacUTTLJJtZBlmUZD"
# get_liked_links(oauth)