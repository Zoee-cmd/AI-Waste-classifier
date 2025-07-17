from django.contrib import admin
from .models import UserScore, ClassificationHistory, LeaderboardEntry

@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'score', 'level', 'created_at', 'updated_at')
    list_filter = ('level', 'created_at')
    search_fields = ('session_id',)
    ordering = ('-score',)

@admin.register(ClassificationHistory)
class ClassificationHistoryAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'predicted_category', 'plastic_confidence', 
                   'paper_confidence', 'organic_confidence', 'user_feedback', 'created_at')
    list_filter = ('predicted_category', 'user_feedback', 'created_at')
    search_fields = ('session_id',)
    ordering = ('-created_at',)

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'level', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('name',)
    ordering = ('-score',) 