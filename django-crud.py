# https://data-flair.training/blogs/django-crud-example/
# https://www.javatpoint.com/django-crud-application

urls.py
-------
from django.contrib import admin
from django.urls import path
from forms import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index-page"),
    path("update/<int:id>", views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
]


models.py
---------
from django.db import models

# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=100, db_column="Name")
    picture = models.ImageField()
    author = models.CharField(max_length=100, default="anonymous")
    email = models.EmailField(blank=True)
    description = models.CharField(max_length=100, default="This is my 1st CRUD app")

    # object = models.Manager
    object = models.Manager

    class Meta:
        db_table = "CONTACT"

forms.py
--------
from django import forms
from .models import ContactModel

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactModel 
        fields = '__all__'


views.py
--------
from django.shortcuts import render, redirect
from .forms import ContactForm

# from django.http import HttpResponseRedirect
from .models import ContactModel

# Create your views here.


def index(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    records = ContactModel.objects.all()
    return render(
        request, "index.html", {"form": form, "records": records, "mode": "show"}
    )


def update(request, id):
    try:
        book_sel = ContactModel.objects.get(id=id)
    except:
        return redirect("/")
    form = ContactForm(request.POST or None, instance=book_sel)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, "index.html", {"form": form})


def delete(request, id):
    try:
        book_sel = ContactModel.objects.get(id=id)
    except:
        return redirect("/")
    book_sel.delete()
    return redirect("/")


index.html
----------
<!DOCTYPE html>
<html lang="en">
{% load static %}


<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head>

<body>
    <div class='container'>
        {% block content %}
        <center>
            <h1 class="display-3" style="background-color:#000000;color:#FFFF99;">Upload Books</h1>
            <form method='POST' enctype="multipart/form-data">
                {% csrf_token %}
                <table class='w-50 table table-light' style="border-radius:10px;background-color:#FFFF99;">
                    {% for field in form %}
                    <tr>
                        <div>
                            <th>{{field.label}}</th>
                            <td>{{ field }}</td>
                        </div>
                    </tr>
                    {% endfor %}
                </table>
                <button type="submit" class="btn btn-lg btn-warning">Submit</button>
            </form>
        </center>
        {% endblock %}
        {% if mode %}
        <div class='d-block'>
            <table class='table table-responsive'>
                <thead>
                    <th>Name</th>
                    <th>Picture</th>
                    <th>Author</th>
                    <th>Email</th>
                    <th>Description</th>
                    <th colspan="2">Actions</th>
                </thead>
                <tbody>
                    {% for row in records %}
                    <tr>
                        <td>{{row.name}}</td>
                        <td>{{row.picture}}</td>
                        <td>{{row.author}}</td>
                        <td>{{row.email}}</td>
                        <td>{{row.description}}</td>
                        <td><a href='update/{{row.id}}'>Edit</a></td>
                        <td><a href='delete/{{row.id}}'>Delete</a></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
    </div>

</body>

</html>
