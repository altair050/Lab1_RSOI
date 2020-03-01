from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serialized = MovieSerializer(movies, many=True)

        return Response(serialized.data)

    def post(self, request):
        serialized = MovieSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status.HTTP_201_CREATED)

        return Response(serialized.errors, status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        serialized = MovieSerializer(movie)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)

        serializer = MovieSerializer(instance=movie, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        movie.delete()

        return Response({"message": "Movie with id '{}' successfully removed.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)
