
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.half_plus_three, name = 'half_plus_three'),
    path('list', views.RequestListView.as_view(), name='request-list'),
]