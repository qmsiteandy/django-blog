from django.urls import path
from . import views

# route '' 時呼叫 views.index (注意函式不用括號)
# name 是用來辨識的 (Optional)
urlpatterns = [
    path('', views.index, name='index'),

    path('articles/<int:article_id>',
         views.view_article_by_id, name='view_article'),
    path('articles/create', views.create_articles, name='create_articles'),
    path('articles/edit/<int:article_id>',
         views.edit_articles, name='edit_articles'),
    path('articles/delete/<int:article_id>',
         views.delete_articles, name='delete_articles'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]
