from django.contrib import admin
from .models import Topic, Question, CurrentStatus

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Topic, TopicAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'chapter', 'question')
admin.site.register(Question, QuestionAdmin)

class CurrentStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'question')
admin.site.register(CurrentStatus, CurrentStatusAdmin)
