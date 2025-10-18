from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Status
from .forms import StatusForm
from .. import task


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            statuses = Status.objects.all()
            return render(
                request,
                "statuses/index.html",
                context={
                    'statuses': statuses,
                },
            )
        return redirect("login")


class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = StatusForm()
            return render(request, "statuses/create.html", {"form": form})
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            messages.info(request, 'Статус успешно создан')
            return redirect("statuses_list")
        return render(request, "statuses/create.html", {"form": form})


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status_id = kwargs.get("id")
            status = Status.objects.get(id=status_id)
            form = StatusForm(instance=status)
            return render(
                request, "statuses/update.html", {"form": form, "status_id": status_id}
            )
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.info(request, 'Статус успешно обновлен')
            return redirect("statuses_list")
        return render(
            request, "statuses/update.html", {"form": form, "status_id": status_id}
        )


class StatusDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status_id = kwargs.get("id")
            status = Status.objects.get(id=status_id)
            if task.models.Task.objects.filter(status=status).exists():
                messages.info(request, 'Нельзя удалить статус, который используется в данный момент')
                return redirect("statuses_list")
            return render(
                request, "statuses/delete.html", {"status_id": status_id}
            )
        messages.info(request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = Status.objects.get(id=status_id)
        if status:
            status.delete()
            messages.info(request, 'Статус успешно удален')
            return redirect('statuses_list')
        return render(request, "statuses/delete.html", {"status_id": status_id})
