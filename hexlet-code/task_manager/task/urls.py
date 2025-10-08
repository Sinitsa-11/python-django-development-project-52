from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="tasks_list"),
    path("create/", views.TaskCreateView.as_view(), name="tasks_create"),
    path("<int:id>/show/", views.TaskShowView.as_view(), name="tasks_show"),
    path("<int:id>/update/", views.TaskUpdateView.as_view(), name="tasks_update"),
    path("<int:id>/delete/", views.TaskDeleteView.as_view(), name="tasks_delete"),
]
