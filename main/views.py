from django.shortcuts import render
from .models import University

def index(request):
    universities = University.objects.all()
    return render(request, 'index.html', {'universities': universities})


def course_detail(request):
    return render(request, 'course_detail.html')


def category_detail(request):
    return render(request, 'category_detail.html')


def univer(request, pk):
    university = University.objects.get(pk=pk)
    return render(request, 'univer.html', {'university': university})