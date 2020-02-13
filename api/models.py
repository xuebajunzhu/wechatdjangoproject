from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """
    token
    电话
    用户名
    用户头像url
    """
    phone = models.CharField(verbose_name="手机号", max_length=11, unique=True)
    token = models.CharField(verbose_name="用户的token", max_length=64, null=True, blank=True)
    nickName = models.CharField(verbose_name="用户名", max_length=32, null=True, blank=True)
    avatarUrl = models.CharField(verbose_name="用户头像url", max_length=256, null=True, blank=True)
    message = models.OneToOneField(verbose_name="用户详细信息", to="Message", on_delete=models.CASCADE)
    open_id =models.CharField(verbose_name="openid",null=True,blank=True,max_length=128)
    balance = models.PositiveIntegerField(verbose_name='账户余额', default=1000)
    session_key = models.CharField(verbose_name='微信会话秘钥', max_length=32)
    def __str__(self):
        return self.nickName

class Adress(models.Model):
    user=models.ForeignKey(verbose_name="用户",to="UserInfo")
    linkman = models.CharField(verbose_name="联系人姓名",max_length=48)
    linkphone = models.CharField(verbose_name="联系人电话",max_length=16)
    address = models.TextField(verbose_name="送货地址")
class Message(models.Model):
    """
        收到点赞数
        点赞 关联到文章(多对多)
        收藏的文章(多对多 文章)
        关注(自关联多对多)
        被提醒
    """
    recv_like_count = models.IntegerField(verbose_name="收到的点赞数量", null=True, blank=True, default=0)
    like = models.ManyToManyField(verbose_name="赞过的文章", to="Article", related_name="article_like")
    enshrine = models.ManyToManyField(verbose_name="收藏的文章", to="Article", related_name="article_enshrine")
    attention = models.ManyToManyField(verbose_name="关注", to="UserInfo", related_name="userinfo_attention")
    mention = models.ManyToManyField(verbose_name="被提及", to="UserInfo", related_name="userinfo_mention")


class Article(models.Model):
    """
    作者(外键关联UserInfo)
    封面   第一张图片
    简介  内容的前10个字符
    点赞数



    文章内容
    定位位置
    参与话题(外键关联话题)
    提醒 多对多
    创建时间
    浏览人数
    浏览人(外键关联Userinfo)  多对多
    点赞数
    收藏(数)
    分享数
    评论数量

    评论(另一张表)
    """
    author = models.ForeignKey(verbose_name="作者", to="UserInfo", related_name="author", on_delete=models.CASCADE)
    cover_url = models.CharField(verbose_name="封面图片", max_length=256)
    summary = models.TextField(verbose_name="简介", blank=True, null=True)
    like_count = models.IntegerField(verbose_name="点赞数量", null=True, blank=True, default=0)

    def __str__(self):
        return self.summary


class ArticleDetail(models.Model):
    article = models.OneToOneField(verbose_name="文章", to="Article", on_delete=models.CASCADE)

    content = models.TextField(verbose_name="发布内容")
    location = models.CharField(verbose_name="位置定位", max_length=64, null=True, blank=True)
    topic = models.ForeignKey(verbose_name="参与话题", to="Topic", null=True, blank=True, on_delete=models.CASCADE)

    mention_user = models.ManyToManyField(verbose_name="提及", to="UserInfo", related_name="mention_user")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    browse_user = models.ManyToManyField(verbose_name="浏览者", to="UserInfo", related_name="browse_user")
    browse_count = models.IntegerField(verbose_name="浏览数量", null=True, blank=True, default=0)
    share_count = models.IntegerField(verbose_name="分享数量", null=True, blank=True, default=0)
    enshrine_count = models.IntegerField(verbose_name="收藏数量", null=True, blank=True, default=0)
    comment_count = models.IntegerField(verbose_name="评论数量", null=True, blank=True, default=0)


class Image(models.Model):
    """
    文章图片
    """
    url = models.CharField(verbose_name="图片路径", max_length=256)
    articledetial = models.ForeignKey(verbose_name="文章", to="ArticleDetail")

    def __str__(self):
        return self.articledetial


class Comment(models.Model):
    """
    内容
    评论人
    评论时间
    评论文章
    回复(自关联)
     @人回复
    点赞数
    评论深度  3级以上加@
    """
    content = models.TextField(verbose_name="评论内容")
    article = models.ForeignKey(verbose_name="评论文章", to="Article", on_delete=models.CASCADE)

    commentator = models.ForeignKey(verbose_name="评论人", to="UserInfo", on_delete=models.CASCADE)

    comment_date = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)

    reply = models.ForeignKey(verbose_name="回复", to="self", null=True, blank=True, on_delete=models.CASCADE)

    mention_user = models.ForeignKey(verbose_name="提及用户回复", to="UserInfo", related_name="comment_mention_user",
                                     null=True, blank=True, on_delete=models.CASCADE)
    root = models.ForeignKey(verbose_name="根评论", to="self", null=True, blank=True, related_name="root_comment",
                             on_delete=models.CASCADE)
    like_count = models.IntegerField(verbose_name="点赞数量", null=True, blank=True, default=0)
    depth = models.IntegerField(verbose_name="评论层级", null=True, blank=True, default=1)

    def __str__(self):
        return self.content + self.commentator.nickName


# 话题
class Topic(models.Model):
    """
    话题标题
    话题首页
    文章数
    浏览次数
    热议人数
    """
    title = models.CharField(verbose_name="话题标题", max_length=32)
    image_url = models.CharField(verbose_name="话题封面", max_length=256)
    article_count = models.IntegerField(verbose_name="文章数", null=True, blank=True, default=0)
    browse_count = models.IntegerField(verbose_name="浏览数量", null=True, blank=True, default=0)
    discussion_count = models.IntegerField(verbose_name="热议人数", null=True, blank=True, default=0)

    def __str__(self):
        return self.title
