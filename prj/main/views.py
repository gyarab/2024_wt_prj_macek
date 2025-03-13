from django.shortcuts import render

def homepage(request):
    return render(request, 'main/homepage.html')

def one(request):
    return render(request, 'main/one.html')

def two(request):
    return render(request, 'main/two.html')
