# -*- coding:utf-8 -*-
# Author:cqk
# Data:2020/1/10 18:09

from rest_framework import serializers
from django.db.models import F,Max
from api import models

from django.forms import model_to_dict


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickName")
    author_avatarUrl = serializers.CharField(source="author.avatarUrl")

    class Meta:
        model = models.Article
        fields = "__all__"


# class ArticleCreateSerializer(serializers.ModelSerializer):
#     image = ImageSerializer(many=True)
class CommentSerializer(serializers.ModelSerializer):
    commentator = serializers.SerializerMethodField(read_only=True)
    comment_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = models.Comment
        fields = "__all__"

    def get_commentator(self, obj):
        return model_to_dict(obj.commentator, fields=["id", "nickName", "avatarUrl"])


class ArticleDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="article.author.nickName")
    author_id = serializers.CharField(source="article.author.id")
    author_avatarUrl = serializers.CharField(source="article.author.avatarUrl")
    topic_title = serializers.SerializerMethodField()
    like_count = serializers.CharField(source="article.like_count")
    imageList = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d")
    commentinfo = serializers.SerializerMethodField()
    browse_user = serializers.SerializerMethodField()

    class Meta:
        model = models.ArticleDetail
        fields = "__all__"

    def get_imageList(self, obj):
        image_objList = obj.image_set.all()
        return [model_to_dict(i, fields=["url"]) for i in image_objList]

    def get_topic_title(self, obj):
        if obj.topic:
            return model_to_dict(obj.topic, fields=["id", "title"])

    def get_browse_user(self, obj):
        return [model_to_dict(user, fields=["id", "nickName", "avatarUrl"]) for user in obj.browse_user.all().order_by("-id")[:10]]

    def get_commentinfo(self, obj):
        firstcomments = models.Comment.objects.filter(article=obj.article,depth=1)
        second_comment_id = models.Comment.objects.filter(article=obj.article,depth=2).values("reply_id").annotate(max_id=Max("id"))
        second_comment_idList = [i["max_id"] for i in second_comment_id]
        secondcomments=models.Comment.objects.filter(id__in=second_comment_idList)
        firstcomments_dict = CommentSerializer(instance=firstcomments, many=True).data
        secondcomments_dict = CommentSerializer(instance=secondcomments, many=True).data
        comments_dict = {k["id"]:k for k in firstcomments_dict}
        for key in secondcomments_dict:
            comments_dict[key["reply"]]["reply_comment"] =[ key,]
        return comments_dict.values()

    # def get_commentinfo(self, obj):
    #     comment_objList = obj.article.comment_set.all().order_by("id")
    #     commentinfo = {}
    #     for comment in comment_objList:
    #         commentDict = {
    #             "comment_id": comment.id,
    #             "commentator_nickName": comment.commentator.nickName,
    #             "commentator_id": comment.commentator_id,
    #             "commentator_avatarUrl": comment.commentator.avatarUrl,
    #             "comment_date": comment.comment_date.strftime("%Y-%m-%d %H %M"),
    #             # "comment_date":comment.comment_date,
    #             "content": comment.content,
    #             "like_count": comment.like_count,
    #             "depth": comment.depth,
    #         }
    #         if comment.depth == 2:
    #             commentinfo.get(comment.reply_id).setdefault("reply", []).append(commentDict)
    #             continue
    #         if comment.depth == 3:
    #             commentDict.setdefault("mention_user", {"mention_user_nickName": comment.mention_user.nickName,
    #                                                     "mention_user_id": comment.mention_user.id})
    #             commentinfo.get(comment.reply_id).setdefault("reply", []).append(commentDict)
    #             continue
    #         commentinfo[comment.id] = commentDict
    #     return commentinfo


class ImageSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=256)


class NewArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleDetail
        fields = ["content", "location", "topic"]
        # exclude = ["mention_user", "create_time", "browse_user", "browse_count", "share_count", "enshrine_count",
        #            "comment_count", "article"]


class IssueSerializer(serializers.ModelSerializer):
    imageList = ImageSerializer(many=True)
    articledetial = NewArticleDetailSerializer()

    class Meta:
        model = models.Article
        fields = ["cover_url", "summary", "imageList", "articledetial"]

    def create(self, validated_data):
        print(validated_data)
        imageList = validated_data.pop("imageList")
        articledetial = validated_data.pop("articledetial")
        article_obj = models.Article.objects.create(**validated_data)
        articledetial_obj = models.ArticleDetail.objects.create(**articledetial, article=article_obj)
        models.Image.objects.bulk_create(
            [models.Image(**i, articledetial=articledetial_obj) for i in imageList]
        )
        if article_obj.articledetail.topic:
            article_obj.articledetail.topic.article_count += 1
        article_obj.articledetial = articledetial_obj
        article_obj.imageList = imageList
        return article_obj
