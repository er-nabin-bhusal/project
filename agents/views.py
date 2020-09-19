from django.shortcuts import render
from django.views.generic import ListView
from .models import Agent

# Create your views here.

class AgentListView(ListView):
    template_name = 'agent-list.html'
    model = Agent
