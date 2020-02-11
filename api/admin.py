from django.contrib import admin
from api import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Message)
admin.site.register(models.Topic)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Comment)
admin.site.register(models.Image)
