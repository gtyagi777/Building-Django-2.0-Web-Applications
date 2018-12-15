from django.shortcuts import render

from django.views.generic import (
    ListView, DetailView,
)
from core.models import Movie, Person


class MovieList(ListView):
    model = Movie
    paginate_by = 5

class MovieDetail(DetailView):
    queryset = ( Movie.objects.all_with_prefetch_persons() )

class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()