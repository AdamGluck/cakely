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
    print datetime.datetime.now()

    while (i <= friend_count):
        try: 
            query = ''' SELECT link_id FROM link
                    WHERE owner IN (SELECT uid1 FROM friend WHERE uid2 = me() LIMIT 10 OFFSET ''' + str(i) + ''')
                    AND like_info.user_likes=1'''
            new_links = graph.fql(query)
            print new_links
            links += new_links
            i += 10
            print i
        except Exception:
            i+= 10
            continue

    print datetime.datetime.now()
    print len(links)
    return links

oauth = "CAACEdEose0cBANevZB1NGY2NdSXXbHwSR7dnpT4ZBCPQPZChOksTxZBZCMddYF5nQf9rm4mSoZCAU0ZCzcDXNeEqhmTZAq7yCXZCUZC8eZBtbUHvdjwxqSI0clUtRFVFuuryQcA3AYjNeUqUlQ9ZAkSLNQvO3ypj1XIijkMqoOWRBiDzwg6pHZCkVmwnqX74zyDpVXRMZD"
# get_liked_links(oauth)