from re import sub
from django.shortcuts import redirect, render
from django import forms
import markdown2

from . import util

class NewForm(forms.Form):
    query = forms.CharField(label='',
                 widget=forms.TextInput(attrs={"placeholder":"Search in the encyclopedia"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm()
    })
def title(request, title):
    content = util.get_entry(title)
    print(content)
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
                return title(request,query)
            else:
                list_of_substrings = []
                for entry in entries:
                    if query.casefold() in entry.casefold():
                        list_of_substrings.append(entry)
                        print(list_of_substrings)

                return render(request, 'encyclopedia/results.html',{
                    "substrings": list_of_substrings,
                    "form":NewForm()
                })
    else: 
        return render(request, 'encyclopedia/index.html')

            

