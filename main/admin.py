from django.contrib import admin
from .models import University, HomeSlide, CategorySubject, Subject, Feature, TrendingCategory, TrendingTopic, PopularTopic, Instructor, Review, ZoomRegistration

class InstructorInline(admin.TabularInline):
    model = Instructor
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    inlines = [InstructorInline, ReviewInline]
    list_display = ('title', 'trending_category', 'trending_topic', 'updated_at')
    search_fields = ('title', 'description')

@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'layout', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('layout', 'is_active')
    search_fields = ('title', 'description', 'quote_text')


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(CategorySubject)
class CategorySubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order')
    list_editable = ('order',)
    inlines = [SubjectInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'provider', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'provider')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(TrendingCategory)
class TrendingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TrendingTopic)
class TrendingTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PopularTopic)
class PopularTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(ZoomRegistration)
class ZoomRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'country', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'country')
    readonly_fields = ('created_at',)
    list_filter = ('created_at', 'country')
