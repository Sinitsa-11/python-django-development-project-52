from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.contrib.auth import get_user_model, logout
from django.contrib import messages

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
            if request.user == user:
                form = CustomUserChangeForm(instance=user)
                return render(
                    request, "users/update.html", {"form": form, "user_id": user_id}
                )
            else:
                return HttpResponse("you damn wrong")
        else:
            return HttpResponse("you idiot")

    def post(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users_list")
        return render(
            request, "users/update.html", {"form": form, "user_id": user_id}
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
                return HttpResponse("you damn wrong")
        else:
            return HttpResponse("you idiot")

    def post(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        if user:
            user.delete()
            messages.success(request, "meow")
            return redirect('users_list')
        return render(request, "users/delete.html", {"user_id": user_id})


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
