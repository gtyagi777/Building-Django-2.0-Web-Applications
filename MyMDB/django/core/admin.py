from django.contrib import admin

# Register your models here.

from core.models import Movie, Person, Role, Vote

admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Vote)
