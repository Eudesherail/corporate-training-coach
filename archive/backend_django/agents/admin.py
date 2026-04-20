from django.contrib import admin
from .models import Agent, State

class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  

admin.site.register(Agent, AgentAdmin)

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_state', 'user', 'agent')  

admin.site.register(State, StateAdmin)