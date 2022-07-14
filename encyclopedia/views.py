from django.http import HttpResponse
from django.shortcuts import render
import markdown2
from django import forms

from . import util


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title:")
    text_form = forms.CharField(label="Content:", widget=forms.Textarea)


def index(request):
    if request.method == "POST":
        word = request.POST['q']
        filenames = util.list_entries()
        scope = list(filename for filename in filenames if word.lower().strip() in filename.lower())
        if scope == []:
            return render(request, "encyclopedia/index.html", {'title': 'File not found'})
        else:
            return render(request, "encyclopedia/index.html", {"entries": scope, 'title': 'Search results'})

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'title': 'Encyclopedia'})


def entries(request, name):
    return render(request, "encyclopedia/entrys.html",
                  {"entries": markdown2.markdown(util.get_entry(name)), 'title': name})


def createnewpage(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text_form = "# " + title + "\n"*2 + form.cleaned_data["text_form"]
            util.save_entry(title, text_form)
            return render(request, "encyclopedia/entrys.html",
                          {"entries": markdown2.markdown(util.get_entry(title)), 'title': title})

    return render(request, "encyclopedia/createnewpage.html", {'title': 'Greate new page', 'form': NewTaskForm})

    # return HttpResponse('wdwadawdawdadwadwad')
# def searh(request):
#     if request.POST['q']:
#         word = request.POST['q']
#         filenames = util.list_entries()
#         scope = list(filename for filename in filenames if word.lower().strip() in filename.lower())
#         return render(request, "encyclopedia/index.html", {"entries": scope, 'title': 'Search results'})
#
#     return HttpResponse(request.POST['q'])
