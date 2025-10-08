from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Task
from .forms import TaskForm


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(
            request,
            "tasks/index.html",
            context={
                "tasks": tasks,
            },
        )


class TaskShowView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        return render(
            request,
            "tasks/show.html",
            context={
                "task": task,
            },
        )


class TaskCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "tasks/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            return redirect("tasks_list")
        return render(request, "tasks/create.html"), {"form": form}


class TaskUpdateView(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        return render(
            request, "tasks/update.html", {"form": form, "task_id": task_id}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks_list")
        return render(
            request, "tasks/update.html", {"form": form, "task_id": task_id}
        )


class TaskDeleteView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        return render(
            request, "tasks/delete.html", {"task_id": task_id}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        if task:
            task.delete()
            messages.success(request, "meow")
            return redirect('tasks_list')
        return render(request, "tasks/delete.html", {"task_id": task_id})
