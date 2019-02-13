from django.shortcuts import render

def home(request):

    response = render(request, 'noobnews/index.html', {})
    
    return response
