from django.db import models
from django.contrib.auth.models import User as auth_user


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Articles(models.Model):
    # "on_delete=models.CASCADE" 代表當關連的 User 刪除時，這筆 Article 也刪除。
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    # "blank=False" 代表不允許空值
    title = models.CharField(max_length=50, blank=False, null=False)
    content = models.CharField(max_length=500, blank=False, null=False)
    last_update = models.DateField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='articles_related_tags'
    )


def _create_articles(request):
    Articles.objects.create(user=request.user, title=request.POST.get(
        "title"), content=request.POST.get("content"))
    return


def _edit_articles_by_id(request, id):
    Articles.objects.filter(id=id).update(
        title=request.POST['title'], content=request.POST['content'])  # No need to update user
    return


def _delete_articles_by_id(request, id):
    Articles.objects.filter(id=id).delete()
    return


# def _get_article_auther(article_id):
#     article = Articles.objects.get(id=article_id)
#     user = article.user

#     print(user.last_login)
#     return user


def _get_articles():
    return Articles.objects.all().order_by('-last_update')


def _get_article_by_id(id):
    return Articles.objects.filter(id=id).first()
