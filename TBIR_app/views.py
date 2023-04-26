from django.shortcuts import render


def welcome(request):
    return render(request, 'index.html')


def result(request):
    index = request.GET['index']
    return render(request, 'result.html')
