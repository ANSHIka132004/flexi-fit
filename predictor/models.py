from django.db import models
from django.utils import timezone

# Create your models here.

class DailyHealthData(models.Model):
    """Model to store daily health tracking data"""
    date = models.DateField(default=timezone.now)
    food_calories = models.IntegerField(default=0)
    exercise_calories = models.IntegerField(default=0)
    steps = models.IntegerField(default=0)
    exercise_time = models.IntegerField(default=0)  # in minutes
    base_goal = models.IntegerField(default=2050)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['date']
        ordering = ['-date']

    def __str__(self):
        return f"Health Data for {self.date}"

    @property
    def remaining_calories(self):
        return self.base_goal - self.food_calories + self.exercise_calories

    @property
    def steps_progress(self):
        return min((self.steps / 10000) * 100, 100)

    @property
    def exercise_progress(self):
        return min((self.exercise_calories / 300) * 100, 100)

class Meal(models.Model):
    """Model to store meal data"""
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    date = models.DateField(default=timezone.now)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    name = models.CharField(max_length=200)
    calories = models.IntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carbs = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'meal_type']

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.name} ({self.date})"

class WeeklyStats(models.Model):
    """Model to store weekly aggregated statistics"""
    week_start = models.DateField()
    total_calories = models.IntegerField(default=0)
    total_steps = models.IntegerField(default=0)
    total_exercise_calories = models.IntegerField(default=0)
    active_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['week_start']
        ordering = ['-week_start']

    def __str__(self):
        return f"Weekly Stats for {self.week_start}"
