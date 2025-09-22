from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="labels_list"),
    path("create/", views.LabelCreateView.as_view(), name='labels_create'),
    path("<int:id>/update/", views.LabelUpdateView.as_view(), name="labels_update"),
    path("<int:id>/delete/", views.LabelDeleteView.as_view(), name="labels_delete"),
]
