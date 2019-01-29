from django.shortcuts import render

def index(request):

    response = render(request, 'noobnews/index.html', {})
    
    return response
