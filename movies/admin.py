from django.contrib import admin
from .models import Movie, Review, MovieRequest, Petition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MovieRequestAdmin(admin.ModelAdmin):
    ordering = ['-date']
    search_fields = ['name', 'user__username']
    list_display = ['name', 'user', 'date']
    list_filter = ['date']

class PetitionAdmin(admin.ModelAdmin):
    ordering = ['-date']
    search_fields = ['title', 'creator__username']
    list_display = ['title', 'creator', 'date', 'get_yes_votes', 'get_no_votes', 'get_total_votes']
    list_filter = ['date']

class PetitionVoteAdmin(admin.ModelAdmin):
    ordering = ['-date']
    search_fields = ['petition__title', 'user__username']
    list_display = ['petition', 'user', 'vote_type', 'date']
    list_filter = ['vote_type', 'date']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MovieRequest, MovieRequestAdmin)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)