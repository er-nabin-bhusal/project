from django.urls import path
from agents.views import AgentListView


app_name = "agents"

urlpatterns=[
  path("list/", AgentListView.as_view(), name='list'),
]
