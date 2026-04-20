from django.contrib import admin
from .models import User, Goal

class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goal', 'startDate', 'endDate')

admin.site.register(User)
admin.site.register(Goal, GoalAdmin)