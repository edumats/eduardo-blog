from django.urls import path

from .views import ProfileDetailView

urlpatterns = [
    path('<id>/', ProfileDetailView.as_view(), name='profile-detail'),
]
