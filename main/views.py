import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import University, HomeSlide, CategorySubject, Feature, TrendingCategory, TrendingTopic, PopularTopic, ZoomRegistration, BusinessService, PrivacyPolicy
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
    business_services = BusinessService.objects.prefetch_related('features').all().order_by('order')

    return render(request, 'index.html', {
        'universities': universities, 
        'slides': slides,
        'categories': categories,
        'categories_json': categories_json,
        'features': features,
        'trending_categories': trending_categories,
        'trending_topics': trending_topics,
        # 'popular_topics': popular_topics,
        'business_services': business_services,
    })


def course_detail(request):
    return render(request, 'course_detail.html')


def category_detail(request):
    return render(request, 'category_detail.html')


def univer(request, pk):
    university = University.objects.prefetch_related('instructors', 'reviews').get(pk=pk)
    return render(request, 'univer.html', {'university': university})

def business_service_detail(request, pk):
    service = BusinessService.objects.prefetch_related('features').get(pk=pk)
    return render(request, 'business_service_detail.html', {'service': service})

def privacy_policy(request):
    policy = PrivacyPolicy.objects.first()
    return render(request, 'privacy_policy.html', {'policy': policy})

@csrf_exempt
def zoom_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            phone = data.get('phone')
            country = data.get('country')
            email = data.get('email')
            zoom_link = data.get('zoom_link')
            
            if full_name and email:
                ZoomRegistration.objects.create(
                    full_name=full_name,
                    phone=phone,
                    country=country,
                    email=email,
                    zoom_link=zoom_link
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)