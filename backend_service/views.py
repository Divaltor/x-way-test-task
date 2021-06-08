from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from loguru import logger
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from backend_service.models import Album
from backend_service.serializers import AlbumSerializer, AlbumWithPhotoSerializer


class AlbumListView(ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumRetrieveView(RetrieveAPIView):
    serializer_class = AlbumWithPhotoSerializer
    queryset = Album.objects.all()


class AlbumUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class AlbumWithPhotosPageView(LoginRequiredMixin, TemplateView):
    template_name = 'album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['album'] = Album.objects.get(pk=kwargs.get('pk'))

        return context
