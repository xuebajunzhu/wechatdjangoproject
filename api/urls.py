# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/8 10:06
from django.conf.urls import url
from api import views
urlpatterns = [
    url(r"^login/$",views.LoginView.as_view()),
    url(r"^mssagecode/$",views.MessageView.as_view()),
    url(r"^credential/$", views.CredentialView.as_view()),
    url(r"^issue/$", views.IssueView.as_view()),
    url(r"^article/$", views.ShowArticlesView.as_view()),
    url(r"^article/(?P<pk>\d+)/$", views.GetArticleDetailView.as_view()),
    url(r"^care/(?P<pk>\d+)/$", views.CareView.as_view()),


    # url(r"^articledetial/(?P<pk>\d+)/$", views.ShowArticleDetailsViews.as_view()),
    url(r"^topic/$", views.TopicView.as_view()),
    url(r"^comment/$", views.CommentView.as_view()),
    url(r"^createarticle/$", views.IssueCreateView.as_view()),

]
