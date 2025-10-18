from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm

from .forms import CustomUserCreationForm, CustomUserChangeForm

# from .models import CustomUser

CustomUser = get_user_model()


class SingUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class CustomUserUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, id=user_id)
            user.set_unusable_password()
            if request.user == user:
                form = CustomUserChangeForm(instance=user)
                return render(
                    request, "users/update.html", {"form": form, "user_id": user_id}
                )
            else:
                messages.info(request, 'У вас нет прав на изменение другого пользователя')
                return redirect("users_list")
        else:
            messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
            return redirect("login")

    def post(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Пользователь успешно изменен')
            return redirect("users_list")
        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
        )


class PasswordUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, id=user_id)
            user.set_unusable_password()
            if request.user == user:
                form = SetPasswordForm(user)
                return render(
                    request, "users/reset_password_form.html", {"form": form, "user_to_reset": user}
                )
            else:
                messages.info(request, 'У вас нет прав на изменение другого пользователя')
                return redirect("users_list")
        else:
            messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
            return redirect("login")

    def post(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Пароль успешно обновлен')
            return redirect("login")
        return render(
            request, "users/reset_password_form.html", {"form": form, "user_to_reset": user}
        )


class CustomUserDeleteView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, id=user_id)
            if request.user == user:
                return render(
                    request, "users/delete.html", {"user_id": user_id}
                )
            else:
                messages.info(request, 'У вас нет прав на удаление другого пользователя')
                return redirect("users_list")
        else:
            messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
            return redirect("login")

    def post(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        if user:
            user.delete()
            messages.success(request, "Пользователь удален")
            return redirect('users_list')
        return render(request, "users/delete.html", {"user_id": user_id, "messages": messages})


def view_logout(request):
    logout(request)
    return redirect('/')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        return render(
            request,
            "users/index.html",
            context={
                'users': users,
            },
        )
