from django.urls import path
from .views import MovieListView, MovieDetailView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='get_post_movie'),
    path('movies/<int:pk>', MovieDetailView.as_view(), name='get_put_delete_movie'),
]
