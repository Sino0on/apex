import os
import django
import sys

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from main.models import BusinessService, ServiceFeature

def run():
    # Clear existing data just in case
    BusinessService.objects.all().delete()

    services_data = [
        {
            'title': 'IT SOLUTIONS (RECARDME)',
            'description': 'Learn a new skill anywhere, anytime.',
            'icon_class': 'fas fa-book',
            'color_class': 'format-beige',
            'order': 1,
            'features': [
                {'text': '6 months study + 6 months internship', 'icon_class': 'far fa-clock'},
                {'text': 'Earn a verified certificate', 'icon_class': 'fas fa-certificate'},
                {'text': 'Upskill quickly', 'icon_class': 'fas fa-chart-line'},
            ]
        },
        {
            'title': 'MARKETING SOLUTIONS',
            'description': 'Advanced diploma In business management',
            'icon_class': 'fas fa-laptop',
            'color_class': 'format-light',
            'order': 2,
            'features': [
                {'text': '12 months duration', 'icon_class': 'far fa-clock'},
                {'text': 'Earn multiple certificates', 'icon_class': 'fas fa-certificate'},
                {'text': 'Upskill on a deeper level', 'icon_class': 'fas fa-chart-line'},
            ]
        },
        {
            'title': 'INTERNSHIP COLLABARATION OPPORTUNITY',
            'description': 'Postgraduate diploma In business management',
            'icon_class': 'fas fa-globe',
            'color_class': 'format-teal',
            'order': 3,
            'features': [
                {'text': '12 months duration', 'icon_class': 'far fa-clock'},
                {'text': 'Earn credentials', 'icon_class': 'fas fa-chart-line'}, # The original has fas fa-certificate then chart-line
                {'text': 'Grow career critical skills', 'icon_class': 'fas fa-chart-line'},
            ]
        },
        {
            'title': 'OVERSEAS CAREER OPORTUNITIES',
            'description': 'International American University: Bachelor of Business Administration',
            'icon_class': 'fas fa-book',
            'color_class': 'format-beige',
            'order': 4,
            'features': [
                {'text': '1 year duration (online)', 'icon_class': 'far fa-clock'},
                {'text': 'Earn a verified certificate', 'icon_class': 'fas fa-certificate'},
                {'text': 'Upskill quickly', 'icon_class': 'fas fa-chart-line'},
            ]
        },
        {
            'title': 'SALES COMMUNITY',
            'description': 'International American University: Bachelor of Business Administration',
            'icon_class': 'fas fa-laptop',
            'color_class': 'format-light',
            'order': 5,
            'features': [
                {'text': '1-2 years duration in America (offline)', 'icon_class': 'far fa-clock'},
                {'text': 'Earn multiple certificates', 'icon_class': 'fas fa-certificate'},
                {'text': 'Upskill on a deeper level', 'icon_class': 'fas fa-chart-line'},
            ]
        },
        {
            'title': 'FRANCHISE OPPORTUNITIES',
            'description': 'International American University: Bachelor of Business Administration',
            'icon_class': 'fas fa-globe',
            'color_class': 'format-teal',
            'order': 6,
            'features': [
                {'text': '1-2 years duration in America (offline)', 'icon_class': 'far fa-clock'},
                {'text': 'Earn credentials', 'icon_class': 'fas fa-certificate'},
                {'text': 'Grow career critical skills', 'icon_class': 'fas fa-chart-line'},
            ]
        }
    ]

    # Let's quickly fix the icons for the 3rd one which I accidentally made both chart-line
    services_data[2]['features'][1]['icon_class'] = 'fas fa-certificate'

    for index, data in enumerate(services_data):
        features_data = data.pop('features')
        service = BusinessService.objects.create(**data)
        
        for f_index, f_data in enumerate(features_data):
            f_data['service'] = service
            f_data['order'] = f_index + 1
            ServiceFeature.objects.create(**f_data)

    print("Successfully populated business services.")

if __name__ == '__main__':
    run()
