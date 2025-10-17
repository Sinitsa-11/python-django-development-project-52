from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='users_list'),
    path('signup/', views.SingUpView.as_view(), name='signup'),
    path('<int:user_id>/update/', views.CustomUserUpdateView.as_view(), name='users_update'),
    path('<int:user_id>/delete/', views.CustomUserDeleteView.as_view(), name="users_delete"),
    path('<int:user_id>/password/', views.PasswordUpdateView.as_view(), name="change_password"),
    path('logout/', views.view_logout, name="logout"),
]
