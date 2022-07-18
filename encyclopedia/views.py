from random import random, randint

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import markdown2
from django import forms
from django.urls import reverse

from . import util


class EditForms(forms.Form):
    EditForm = forms.CharField(label='', widget=forms.HiddenInput())


def index(request):
    if request.method == "POST":
        word = request.POST['q']
        filenames = util.list_entries()
        scope = list(filename for filename in filenames if word.lower().strip() in filename.lower())
        if not scope:
            return render(request, "encyclopedia/index.html", {'title': 'File not found'})
        else:
            return render(request, "encyclopedia/index.html", {"entries": scope, 'title': 'Search results'})

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'title': 'Encyclopedia'})


def entries(request, name):
    markText = util.get_entry(name).split("\n", 2)[2]
    if request.method == "POST":
        return createnewpage(request, name, markText)

    return render(request, "encyclopedia/entrys.html",
                  {"entries": markdown2.markdown(util.get_entry(name)), 'title': name, })


def createnewpage(request, initTitle='', initText=''):
    print(request.POST)

    class NewTaskForm(forms.Form):
        title = forms.CharField(label="Title:", initial=initTitle)
        text_form = forms.CharField(label="Content:", widget=forms.Textarea, initial=initText)

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text_form = "# " + title + "\n" * 2 + form.cleaned_data["text_form"]
            filenames = util.list_entries()
            if title in filenames and not 'EditForm' in (request.POST):
                return render(request, "encyclopedia/index.html",
                              {'title': 'File already exists'})
            else:
                util.save_entry(title, text_form)
                return redirect(reverse("index") + title)
    if initTitle:
        return render(request, "encyclopedia/createnewpage.html",
                      {'title': 'Edit page', 'form': NewTaskForm, 'flag': EditForms})
    return render(request, "encyclopedia/createnewpage.html", {'title': 'Greate new page', 'form': NewTaskForm})


def randompage(request):
    name_file = util.list_entries()
    rand_int = randint(0, len(name_file) - 1)
    return entries(request, name_file[rand_int])
