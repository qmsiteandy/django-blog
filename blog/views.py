from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import _get_articles, _create_articles, _get_article_by_id, _edit_articles_by_id, _delete_articles_by_id
from .form import create_articles_form, edit_articles_form
from django.contrib.auth import authenticate, login as auth_login, logout as user_logout
from django.contrib.auth.decorators import login_required


@require_http_methods(['GET'])
def index(request):
    articles = _get_articles()
    context = {"articles": articles}
    return render(request, "index.html", context)


###
# articles part
###

@login_required
def create_articles(request):
    if request.method == "GET":
        context = {'form': create_articles_form(), }
        return render(request, "create_articles.html", context)
    else:
        a = _create_articles(request)
        return redirect("index")


@login_required
def edit_articles(request, article_id):
    if request.method == "GET":
        context = {'form': edit_articles_form(article_id), 'id': article_id}
        return render(request, "edit_articles.html", context)
    else:
        _edit_articles_by_id(request, article_id)
        return redirect("index")


@login_required
def delete_articles(request, article_id):
    _delete_articles_by_id(request, article_id)
    return redirect("index")


def view_article_by_id(request, article_id):
    a = _get_article_by_id(article_id)
    context = {"article": a}
    return render(request, "view_article.html", context)


###
# auth part
###

def login(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        return redirect("index")
    else:
        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        print(user)
        if user != None:
            auth_login(request, user)
            return redirect("index")
        else:
            return redirect("/blog/login")


def logout(request):
    if request.user.is_authenticated:
        user_logout(request)
    return redirect("index")
