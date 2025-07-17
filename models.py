from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserScore(models.Model):
    """Model to store user scores and levels"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"Score: {self.score}, Level: {self.level}"


class ClassificationHistory(models.Model):
    """Model to store classification history"""
    WASTE_CATEGORIES = [
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('organic', 'Organic'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='classifications/', null=True, blank=True)
    plastic_confidence = models.FloatField(default=0)
    paper_confidence = models.FloatField(default=0)
    organic_confidence = models.FloatField(default=0)
    predicted_category = models.CharField(max_length=10, choices=WASTE_CATEGORIES)
    user_feedback = models.BooleanField(null=True, blank=True)  # True for correct, False for wrong
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.predicted_category} - {self.created_at}"


class LeaderboardEntry(models.Model):
    """Model for leaderboard entries"""
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.name} - {self.score} points" 