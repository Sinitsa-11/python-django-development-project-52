from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tasks = Task.objects.all()
            return render(
                request,
                "tasks/index.html",
                context={
                    "tasks": tasks,
                },
            )
        return redirect("login")


class TaskShowView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task_id = kwargs.get("id")
            task = Task.objects.get(id=task_id)
            return render(
                request,
                "tasks/show.html",
                context={
                    "task": task,
                },
            )
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")


class TaskCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = TaskForm()
            return render(request, "tasks/create.html", {"form": form})
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            messages.info(request, 'Задача успешно создана')
            return redirect("tasks_list")
        return render(request, "tasks/create.html"), {"form": form}


class TaskUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task_id = kwargs.get("id")
            task = Task.objects.get(id=task_id)
            form = TaskForm(instance=task)
            return render(
                request, "tasks/update.html", {"form": form, "task_id": task_id}
            )
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, 'Задача успешно обновлена')
            return redirect("tasks_list")
        return render(
            request, "tasks/update.html", {"form": form, "task_id": task_id}
        )


class TaskDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            task_id = kwargs.get("id")
            task = Task.objects.get(id=task_id)
            if request.user == task.user:
                return render(
                    request, "tasks/delete.html", {"task_id": task_id}
                )
            else:
                messages.info(request, 'У вас нет прав на удаление задач других пользователей')
                return redirect("tasks_list")
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
            messages.info(request, 'Задача удалена')
            return redirect('tasks_list')
        return render(request, "tasks/delete.html", {"task_id": task_id})
