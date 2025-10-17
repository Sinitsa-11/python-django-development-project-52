from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Label
from .forms import LabelForm
from .. import task


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            labels = Label.objects.all()
            return render(
                request,
                "labels/index.html",
                context={
                    'labels': labels,
                },
            )
        return redirect("login")


class LabelCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = LabelForm()
            return render(request, "labels/create.html", {"form": form})
        return redirect("login")

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            return redirect("labels_list")
        return render(request, "labels/create.html", {"form": form})


class LabelUpdateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            label_id = kwargs.get("id")
            status = Label.objects.get(id=label_id)
            form = LabelForm(instance=status)
            return render(
                request, "labels/update.html", {"form": form, "label_id": label_id}
            )
        return redirect("login")

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get("id")
        label = Label.objects.get(id=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect("labels_list")
        return render(
            request, "labels/update.html", {"form": form, "label_id": label_id}
        )


class LabelDeleteView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            label_id = kwargs.get("id")
            label = Label.objects.get(id=label_id)
            if task.models.Task.objects.filter(label=label).exists():
                return redirect("labels_list")
            return render(
                request, "labels/delete.html", {"label_id": label_id}
            )
        return redirect("login")

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get("id")
        label = Label.objects.get(id=label_id)
        if label:
            label.delete()
            messages.success(request, "meow")
            return redirect('labels_list')
        return render(
            request, "labels/delete.html", {"label_id": label_id}
        )
