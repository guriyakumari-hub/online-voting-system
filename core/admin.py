from django.contrib import admin
from .models import Candidate, Election, Vote


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_ongoing')
    search_fields = ('title', 'description')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'election', 'user')
    search_fields = ('full_name',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'election', 'created_at')
    list_filter = ('election',)
