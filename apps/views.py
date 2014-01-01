from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Link, User, UserLink

import time
import calendar
import datetime
import django.utils.timezone as tz

import apps.helpers as helpers
import django_rq

class HomePageView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SeeLikeHistoryView(View):
    template_name = 'historical.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RunView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.QUERY_PARAMS
        fb_id = data['fb_id']
        print(fb_id);
        try:
            user_queryset = User.objects.filter(fb_id=fb_id)
            user_list = list(user_queryset)
            if len(user_list) == 1:
                user = user_list[0]
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.loaded:
            completion_status = {"loaded": "true"}
            return Response(completion_status, status=status.HTTP_200_OK)
        else:
            completion_status = {"loaded": "false"}
            return Response(completion_status, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        print "post received"
        data = request.DATA
        print "data received"

        try:
            print "trying to get data"
            fb_id = data['fb_id']
            oauth = data['oauth']
            email = data['email']
        except KeyError:
            error = {'error': "Invalid request"}
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)

        print "trying to get User"
        try:
            user = User(fb_id=fb_id, email=email)
            user.save()
        except Exception:
            content = {'content': 'account already exists'}
            return Response(content, status=status.HTTP_200_OK)
        print("starting redis queue")
        django_rq.enqueue(run_queue, fb_id, oauth, email, user)
        print("redis queue started")
        return Response(status=status.HTTP_201_CREATED)

def run_queue(fb_id, oauth, email, user):
    print("in run queue")
    links = helpers.get_liked_links(oauth)

    for link in links:
        if not link:
            continue

        image_url = ""
        if link[u'image_urls']:
            image_url = link[u'image_urls'][0]

        try:
            l = Link(url=link[u'url'], title=link[u'title'], 
                     summary=link[u'summary'], image_url=image_url)
            l.save()
        except Exception:
            l = Link.objects.filter(url=link[u'url'])

        try:
            proper_date = datetime.datetime.utcfromtimestamp(link[u'created_time'])
            utc_date = tz.make_aware(proper_date, tz.utc)
            date_string = utc_date.isoformat()
            ul = UserLink(user=user, link=l, seen=date_string)
            ul.save() 
        except Exception:
            continue

    user.loaded = True;
    user.save()
    return True   


# Create your views here.
def login(request):
    return HttpResponse("Hello, world")