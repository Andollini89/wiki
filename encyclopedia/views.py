from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def title(request, title):
    content = util.get_entry(title)
    print(content)
    if content:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/title.html", {
            'title': title,
            'content': content
        })
    else:
        return render(request, "encyclopedia/index.html",)

