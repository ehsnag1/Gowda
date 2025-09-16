from django.contrib import admin
from .models import Movie, Review, MovieRequest

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MovieRequestAdmin(admin.ModelAdmin):
    ordering = ['-date']
    search_fields = ['name', 'user__username']
    list_display = ['name', 'user', 'date']
    list_filter = ['date']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MovieRequest, MovieRequestAdmin)