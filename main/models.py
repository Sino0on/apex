from django.db import models


class University(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='university_logos/')
    image = models.ImageField(upload_to='university_images/', blank=True, null=True)
    description = models.TextField()
    mini_description = models.TextField()
    trending_category = models.ForeignKey('TrendingCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='universities')
    trending_topic = models.ForeignKey('TrendingTopic', on_delete=models.SET_NULL, null=True, blank=True, related_name='universities')
    
    # Detail Page Fields
    banner_image = models.ImageField(upload_to='university_banners/', blank=True, null=True)
    verified_by = models.CharField(max_length=100, default="HKPolyUx", help_text="Entity verifying the course")
    level = models.CharField(max_length=50, default="Intermediate")
    pacing = models.CharField(max_length=50, default="Instructor-paced")
    duration_weeks = models.PositiveIntegerField(default=32, help_text="Duration in weeks")
    certification_type = models.CharField(max_length=100, default="Professional Certificate")
    
    course_count = models.PositiveIntegerField(default=4, help_text="Number of courses in the program")
    months_duration = models.PositiveIntegerField(default=8, help_text="Duration in months")
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    student_count = models.PositiveIntegerField(default=0, help_text="Number of learners enrolled")
    
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Current price")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price before discount")
    
    skills_gained = models.TextField(default="", help_text="Comma-separated list of skills (e.g., Marketing, Tourism)")
    language = models.CharField(max_length=50, default="English")
    transcripts = models.CharField(max_length=100, default="English, 中文", help_text="Available transcripts")
    prerequisites = models.TextField(default="None")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    def get_skills_list(self):
        if self.skills_gained:
            return [skill.strip() for skill in self.skills_gained.split(',')]
        return []

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'
        ordering = ['-updated_at']


class Instructor(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='instructors')
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, help_text="Job title or academic position")
    image = models.ImageField(upload_to='instructors/', blank=True, null=True)
    institution_logo = models.ImageField(upload_to='instructor_logos/', blank=True, null=True, help_text="Logo of the instructor's institution")

    def __str__(self):
        return self.name


class Review(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    user_image = models.ImageField(upload_to='reviewers/', blank=True, null=True)
    user_location = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")

    def __str__(self):
        return f"Review by {self.user_name}"


class HomeSlide(models.Model):
    LAYOUT_CHOICES = (
        ('STANDARD', 'Standard (Quote)'),
        ('ZOOM', 'Zoom (Cards)'),
    )

    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='STANDARD')
    title = models.CharField(max_length=200, help_text="Main title of the slide")
    description = models.TextField(help_text="Description or subtitle", blank=True)
    bg_image = models.ImageField(upload_to='slider_bg/', help_text="Background image for the slide")
    
    # Standard Layout Fields
    button_text = models.CharField(max_length=50, blank=True, null=True, help_text="Button text (Standard layout)")
    button_url = models.CharField(max_length=200, blank=True, null=True, help_text="Button URL (Standard layout)")
    quote_text = models.TextField(blank=True, null=True, help_text="Quote text (Standard layout)")
    
    # Zoom/Card Layout Fields - Card 1
    card_1_title = models.CharField(max_length=200, blank=True, null=True)
    card_1_date = models.CharField(max_length=100, blank=True, help_text="e.g. Feb 23, 2026 08:00 PM Singapore")
    card_1_text = models.TextField(blank=True, help_text="Provider text or description")
    card_1_link = models.URLField(blank=True, null=True, help_text="Zoom link logic applies here")
    card_1_image = models.ImageField(upload_to='slider_cards/', blank=True, null=True)

    # Zoom/Card Layout Fields - Card 2
    card_2_title = models.CharField(max_length=200, blank=True, null=True)
    card_2_date = models.CharField(max_length=100, blank=True)
    card_2_text = models.TextField(blank=True)
    card_2_link = models.URLField(blank=True, null=True)
    card_2_image = models.ImageField(upload_to='slider_cards/', blank=True, null=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_layout_display()})"

    class Meta:
        verbose_name = 'Home Slide'
        verbose_name_plural = 'Home Slides'
        ordering = ['order']


class CategorySubject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Unique identifier for the category tab (e.g., 'business')")
    svg_icon = models.FileField(upload_to='category_icons/', help_text="Upload SVG or Image icon")
    description = models.TextField()
    quote = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Explore Category'
        verbose_name_plural = 'Explore Categories'

    def __str__(self):
        return self.title


class Subject(models.Model):
    category = models.ForeignKey(CategorySubject, on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200, default="Starweaver")
    description = models.TextField()
    badge = models.CharField(max_length=50, default="See more")
    gradient = models.CharField(max_length=200, default="linear-gradient(135deg, #a71d78 0%, #d42e68 100%)", help_text="CSS Gradient string")
    image = models.ImageField(upload_to='subject_images/', blank=True, null=True, help_text="Optional image to override gradient")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Feature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def __str__(self):
        return self.title


class TrendingCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Unique identifier for filtering (e.g., 'mba')")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Trending Category'
        verbose_name_plural = 'Trending Categories'

    def __str__(self):
        return self.name


class PopularTopic(models.Model):
    title = models.CharField(max_length=200)
    icon = models.FileField(upload_to='topic_icons/', help_text="Upload SVG or Image icon")
    link = models.URLField(blank=True, null=True, help_text="Optional link to category page")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Popular Topic'
        verbose_name_plural = 'Popular Topics'

    def __str__(self):
        return self.title


class TrendingTopic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Unique identifier for filtering (e.g., 'data-science')")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Trending Topic'
        verbose_name_plural = 'Trending Topics'

    def __str__(self):
        return self.name