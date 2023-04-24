from django.shortcuts import render


def welcome(request):
    return render(request, 'index.html')


def result(request):
    index = request.GET['index']
    print("Fix here for retrieve the photo")
    return render(request, 'result.html')
