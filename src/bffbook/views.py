from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    #return HttpResponse('Hello World')
    context = {
        'user' : request.user,
        'hello' : 'hello world'
    }
    return render(request,'main/home.html', context)