import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer


class MovieTests(TestCase):
    def setUp(self):
        Movie.objects.create(name='Полицейская академия', director='Х. Х. Уилсон', release_date=1984)
		
    def test_movie_create(self):
        movie_police_academia = Movie.objects.get(name='Полицейская академия')
        self.assertEqual(movie_police_academia.name, 'Полицейская академия')


class MovieViewTest(APITestCase):
    client = APIClient()
    url = reverse('get_post_movie')

    def setUp(self):
        Movie.objects.create(name='Полицейская академия', director='Х. Х. Уилсон', release_date=1984)
        Movie.objects.create(name='Полицейская академия 3: Переподготовка', director='Х. Х. Уилсон', release_date=1986)
        Movie.objects.create(name='Полицейская академия 7: Миссия в Москве', director='Х. Х. Уилсон', release_date=1994)

    def test_get_all_movies(self):
        '''
        Запрос на получение всех кинокартин
        '''
        movies = Movie.objects.all()
        serialized = MovieSerializer(movies, many=True)

        response = self.client.get(self.url)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_add_new_movie(self):
        '''
        Запрос на добавление нового фильма
        '''
        movie = {
            'name': 'Полицейская академия 2: Их первое задание',
            'director': 'Х. Х. Уилсон',
            'release_date': 1985
        }

        response = self.client.post(self.url,
                                    data=json.dumps(movie),
                                    content_type='application/json')

        self.assertEqual(response.data, movie)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_movie_negative_publish_year(self):
        '''
        Запрос на добавление нового фильма c некорректным годом выпуска
        '''
        movie = {
            'name': 'Полицейская академия 4: Граждане в дозоре',
            'director': 'Х. Х. Уилсон',
            'release_date': 1337
        }

        response = self.client.post(self.url,
                                    data=json.dumps(movie),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
