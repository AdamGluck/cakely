from django.shortcuts import render
from django.views.generic import View

class HomePageView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SeeLikeHistoryView(View):
    template_name = 'historical.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# Create your views here.
def login(request):
    return HttpResponse("Hello, world")