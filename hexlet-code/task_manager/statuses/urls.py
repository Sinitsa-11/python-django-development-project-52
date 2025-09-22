from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="statuses_list"),
    path("create/", views.StatusCreateView.as_view(), name="statuses_create"),
    path("<int:id>/update/", views.StatusUpdateView.as_view(), name="statuses_update"),
    path("<int:id>/delete/", views.StatusDeleteView.as_view(), name="statuses_delete"),
]
