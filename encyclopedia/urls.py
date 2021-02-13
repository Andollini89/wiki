from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.titles, name="title"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random_wiki/", views.randomPage, name='random')
]
