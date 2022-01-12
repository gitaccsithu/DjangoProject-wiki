from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random
import markdown2

from . import util
from django import forms

class NewEntryForm(forms.Form):
    req_entry = forms.CharField()

def index(request):
    if request.method == "POST":
        entry = request.POST.get("q")
        print(entry)
        if util.get_entry(entry):
            return render(request, "encyclopedia/entry.html", {
                "entry_name": entry,
                "entry": markdown2.markdown(util.get_entry(entry))
            })
        else:
            return render(request, "encyclopedia/result.html", {
                "results": list(i for i in util.list_entries() if i.find(entry) > -1)
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry,
            "entry": markdown2.markdown(util.get_entry(entry))
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_name": 404,
            "error": "Page not found"
        })

def create_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        print(title)
        contents = request.POST.get("contents")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "error_name": "Can't create",
                "error": "Entry already exit"
            })
        else:
            util.save_entry(title, contents)
            return HttpResponseRedirect(reverse("show_entry", args=[title]))
    return render(request, "encyclopedia/create.html")

def edit(request, entry):
    if request.method == "POST":
        edited_contents = request.POST.get("edited_entry")
        util.save_entry(entry, edited_contents)
        return HttpResponseRedirect(reverse("show_entry", args=[entry]))
    return render(request, "encyclopedia/edit.html", {
        "entry_name": entry,
        "entry": util.get_entry(entry)
    })

def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    print(entry)
    return render(request, "encyclopedia/entry.html", {
            "entry_name": entry,
            "entry": markdown2.markdown(util.get_entry(entry))
        })