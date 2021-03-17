from logging import PlaceHolder
from re import sub
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2

from . import util

class NewForm(forms.Form):
    query = forms.CharField(label='',
                 widget=forms.TextInput(attrs={"placeholder":"Search in the encyclopedia"}))

class NewPageForm(forms.Form):
    title = forms.CharField(max_length=100, 
            widget= forms.TextInput(attrs={"placeholder": "Insert title here"}))
    description = forms.CharField(widget=forms.Textarea)

class EditTextForm(forms.Form):
    desc = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm()
    })
def titles(request, title):
    content = util.get_entry(title)
    #print(content)
    if content:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/title.html", {
            'title': title,
            'content': content,
            'form': NewForm()
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "message": "The page requested does not exist!",
            "e_num" : '404',
            "form": NewForm()
        })
def search(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"].upper()
            entries = util.list_entries()
            if query in entries:
                print(query)
                return HttpResponseRedirect(reverse('encyclopedia:title', args=(),kwargs={
                    'title': query
                }))
            else:
                list_of_substrings = []
                for entry in entries:
                    if query.casefold() in entry.casefold():
                        list_of_substrings.append(entry)
                        #print(list_of_substrings)

                return render(request, 'encyclopedia/results.html',{
                    "substrings": list_of_substrings,
                    "form":NewForm()
                })
def new_page(request):
    if request.method == 'POST':
        forms = NewPageForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data['title'].title()
            description = forms.cleaned_data['description'].title()
            entries = util.list_entries()
            if title.upper() in entries:
                #print(title.upper(), entries)
                return render(request, "encyclopedia/error.html",{
                    "message": "The page already exist please check and retry"
                })
            else:
                description = "#"+ title +"\n" + description
                util.save_entry(title, description)
            return HttpResponseRedirect(reverse('encyclopedia:title', args=(),kwargs={
                    'title':title
                    }))
    else:
        return render(request, "encyclopedia/new_page.html",{
            "insertions": NewPageForm(),
        })
def edit(request, title):
    if request.method == "POST":
        forms = EditTextForm(request.POST)
        if forms.is_valid():
            description = forms.cleaned_data['desc']
            util.save_entry(title.rstrip("\n"), description.replace("\n",""))
            print(description, title)
        return HttpResponseRedirect(reverse('encyclopedia:title', args=(),kwargs={
                    'title':title
                    })) 
    else:
        content = util.get_entry(title)
        form = EditTextForm()
        form['desc'].initial = content
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":form
        })
def randomPage(request):
    entries = util.list_entries()
    index = random.randint(0, len(entries)-1)
    return HttpResponseRedirect(reverse('encyclopedia:title', args=(),kwargs={
                    'title':entries[index]
                    }))

            
