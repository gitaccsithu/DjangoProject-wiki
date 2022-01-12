from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.show_entry, name="show_entry"),
    path("create/", views.create_entry, name="create_entry"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random/", views.random_entry, name="random")
]
