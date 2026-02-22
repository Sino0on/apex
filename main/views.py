import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import University, HomeSlide, CategorySubject, Feature, TrendingCategory, TrendingTopic, PopularTopic
from django.shortcuts import render

def index(request):
    universities = University.objects.all()
    slides = HomeSlide.objects.filter(is_active=True).order_by('order')
    
    # Serialize Categories
    categories = CategorySubject.objects.prefetch_related('subjects').order_by('order')
    explore_categories = {}
    for cat in categories:
        courses = []
        for subject in cat.subjects.all().order_by('order'):
            courses.append({
                'title': subject.title,
                'provider': subject.provider,
                'desc': subject.description,
                'type': subject.badge,
                'gradient': subject.gradient,
                'image': subject.image.url if subject.image else None
            })
            
        explore_categories[cat.slug] = {
            'title': cat.title,
            'description': cat.description,
            'quote': cat.quote,
            'author': cat.author,
            'courses': courses
        }
    
    categories_json = json.dumps(explore_categories, cls=DjangoJSONEncoder)
    
    features = Feature.objects.all().order_by('order')
    trending_categories = TrendingCategory.objects.all().order_by('order')
    trending_topics = TrendingTopic.objects.all().order_by('order')
    popular_topics = PopularTopic.objects.all().order_by('order')

    return render(request, 'index.html', {
        'universities': universities, 
        'slides': slides,
        'categories': categories,
        'categories_json': categories_json,
        'features': features,
        'trending_categories': trending_categories,
        'trending_topics': trending_topics,
        'popular_topics': popular_topics
    })


def course_detail(request):
    return render(request, 'course_detail.html')


def category_detail(request):
    return render(request, 'category_detail.html')


def univer(request, pk):
    university = University.objects.prefetch_related('instructors', 'reviews').get(pk=pk)
    return render(request, 'univer.html', {'university': university})