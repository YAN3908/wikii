from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import markdown2
from django import forms
from django.urls import reverse

from . import util


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title:", initial="")
    text_form = forms.CharField(label="Content:", widget=forms.Textarea, initial="")



# class EditForms(forms.Form):
# EditForm = forms.CharField(label="Title:")


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
    class EditForms(forms.Form):
        EditForm = forms.CharField(label='', widget=forms.HiddenInput(), initial=name)

    return render(request, "encyclopedia/entrys.html",
                  {"entries": markdown2.markdown(util.get_entry(name)), 'title': name, 'form': EditForms})


def createnewpage(request):
    if request.method == "POST":
        if 'EditForm' in request.POST:
            return HttpResponse('worced')
        form = NewTaskForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text_form = "# " + title + "\n" * 2 + form.cleaned_data["text_form"]
            filenames = util.list_entries()
            if title in filenames:
                return render(request, "encyclopedia/index.html",
                              {'title': 'File already exists'})
            else:
                util.save_entry(title, text_form)
                # return HttpResponseRedirect("/wiki/" + title)
                return redirect(reverse("index") + title)
                # return render(request, "encyclopedia/entrys.html",
                #               {"entries": markdown2.markdown(util.get_entry(title)), 'title': title, })

    return render(request, "encyclopedia/createnewpage.html", {'title': 'Greate new page', 'form': NewTaskForm})

    # return HttpResponse('worced')
# def searh(request):
#     if request.POST['q']:
#         word = request.POST['q']
#         filenames = util.list_entries()
#         scope = list(filename for filename in filenames if word.lower().strip() in filename.lower())
#         return render(request, "encyclopedia/index.html", {"entries": scope, 'title': 'Search results'})
#
#     return HttpResponse(request.POST['q'])
