from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import apps.helpers as helpers
from apps.models import Link, User, UserLink
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
            ul = UserLink(user=user, link=l, seen=link[u'created_time'])
            ul.save() 
        except Exception:
            continue

    user.loaded = True;

    return True   


# Create your views here.
def login(request):
    return HttpResponse("Hello, world")