from django.urls import path
from . import views

app_name = 'calls'

urlpatterns = [
    path('', views.CallLogListView.as_view(), name='list'),
    path('<int:pk>/', views.CallLogDetailView.as_view(), name='detail'),
    path('create/', views.CallLogCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.CallLogUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CallLogDeleteView.as_view(), name='delete'),
]
