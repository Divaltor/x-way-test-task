from django.urls import path
from rest_framework.authtoken import views

from backend_service.views import AlbumListView, AlbumUpdateDeleteView, AlbumRetrieveView, HomePageView, \
    AlbumWithPhotosPageView

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('albums/', AlbumListView.as_view(), name='albums'),
    path('albums/<int:pk>/', AlbumRetrieveView.as_view(), name='album-with-photo-api'),
    path('albums/<int:pk>/', AlbumUpdateDeleteView.as_view()),
    path('', HomePageView.as_view(), name='index'),
    path('albums/<int:pk>/photos/', AlbumWithPhotosPageView.as_view(), name='album-with-photo')
]
