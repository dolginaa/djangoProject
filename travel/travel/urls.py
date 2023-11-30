
from django.urls import path, re_path
from pages import views

urlpatterns = [
    path('', views.index, name='home'),
    re_path(r"index.html", views.index),
    re_path(r"^about/(?P<name>\D+)/", views.about, name='info'),
    re_path(r"^about", views.about),
    re_path(r"about.html", views.about),
    re_path(r"^weather/(?P<name>\D+)/", views.weather, name='climat'),
    re_path(r"^weather", views.weather),
    re_path(r"weather.html", views.weather),
    re_path(r"^sights/(?P<name>\D+)/", views.sights, name='seeing'),
    re_path(r"^sights", views.sights),
    re_path(r"sights.html", views.sights),
    path('hangman_game/', views.hangman_game, name='hangman_game'),
    path('wikipedia/', views.get_wikipedia_page, name='wikipedia'),
]
