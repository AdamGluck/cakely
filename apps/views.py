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
        data = request.DATA

        try:
            fb_id = data['fb_id']
            oauth = data['oauth']
            email = data['email']
        except KeyError:
            error = {'error': "Invalid request"}
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            u = User(fb_id=fb_id, email=email)
            u.save()
        except Exception:
            content = {'content': 'account already exists'}
            return Response(content, status=status.HTTP_200_OK)

        django_rq.enqueue(run_queue, fb_id, oauth, email)
        return Response(status=status.HTTP_201_CREATED)

def run_queue(fb_id, oauth, email):
    links = helpers.get_liked_links(oauth)

    for link in links:
        image_url = ""
        if len(link[u'image_urls']):
            image_url = link[u'image_urls'][0]

        try:
            l = Link(url=link[u'url'], title=link[u'title'], summary=link[u'summary'], image_url=image_url)
            l.save()
        except Exception:
            l = Link.objects.filter(url=link[u'url'])

        try:
            ul = UserLink(user=u, link=l)
            ul.save() 
        except Exception:
            continue

    return True   


# Create your views here.
def login(request):
    return HttpResponse("Hello, world")