import re
import random
import uuid

from sts.sts import Sts
from django_redis import get_redis_connection

from api import models
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView,DestroyAPIView
from rest_framework.exceptions import ValidationError
from api.seriralizer.account import LoginSerializers, MessageSerializers
from api.seriralizer.ArticleSerializer import ArticleSerializer, ArticleDetailSerializer, IssueSerializer, \
    CommentSerializer
from api.seriralizer.TopicSerializer import TopicSerializer
from api.auth import CoerceAuth, Auth
from api.seriralizer.CareSerializer import CareSerializer

# Create your views here.

class LoginView(APIView):
    """
    程序启动调用
    """

    def get(self, request, *args, **kwargs):
        # print(request.data)
        userinfo = request.query_params.dict()
        userobj = models.UserInfo.objects.filter(token=userinfo.get("token"))
        if userobj:
            userinfo.update(nickName=userinfo.get("nickName"), avatarUrl=userinfo.get("avatarUrl"))

            return Response({"status": True, "code": "ok", "msg": "数据库已更新"})
        return Response({"status": False, "code": "warning", "msg": "用户未登录"})


class MessageView(APIView):
    """
    get获取短信验证码
    post登陆或者认证
    """

    def get(self, request, *args, **kwargs):
        ser = MessageSerializers(data=request.query_params)
        if not ser.is_valid():
            return Response({"status": False, "code": "error", "msg": "手机号格式错误"})
        phone = ser.validated_data.get("phone")
        code = random.randint(1000, 9999)
        print(code)
        # ret = sendsms(phone, code)  #发送验证码
        # if not ret:
        #     return Response({"status": False, "code": "fail", "msg": "验证码发送失败!"})

        # conn = get_redis_connection("default")
        # conn.set(phone, code, ex=60)
        return Response({"status": True, "code": "ok", "msg": "验证码发送成功!"})

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        code = request.data.get("code")
        nickName = request.data.get("nickName")
        avatarUrl = request.data.get("avatarUrl")
        print(nickName, avatarUrl)
        ser = LoginSerializers(data=request.data)
        print(phone, code)
        if not ser.is_valid():
            return Response({"status": False, "code": "error", "msg": "验证码错误"})

        # usergg  = models.UserInfo.objects.filter(phone=ser.initial_data.get("phone")).first()
        # if not user:
        #     models.UserInfo.objects.create(phone=ser.initial_data.get("phone"),token=str(uuid.uuid4()))
        # else:
        #     user.token = str(uuid.uuid4())
        #     user.save()

        phone = ser.initial_data.get("phone")
        message_obj = models.Message.objects.create()
        userobj, flag = models.UserInfo.objects.get_or_create(phone=phone)  # flag=True 是创建
        if flag:
            userobj.message = message_obj
        userobj.token = str(uuid.uuid4())
        userobj.avatarUrl = avatarUrl
        userobj.nickName = nickName
        userobj.save()

        return Response({"status": True, "code": "ok", "msg": "登陆成功", "data": {"token": userobj.token, "phone": phone}})


class CredentialView(APIView):
    def get(self, request, *args, **kwargs):
        config = {
            # 临时密钥有效时长，单位是秒
            'duration_seconds': 1800,
            # 固定密钥 id
            'secret_id': settings.TENCENT_SECRET_ID,
            # 固定密钥 key
            'secret_key': settings.TENCENT_SECRET_KEY,
            # 设置网络代理
            # 'proxy': {
            #     'http': 'xx',
            #     'https': 'xx'
            # },
            # 换成你的 bucket
            'bucket': 'examplebucket-1300594020',
            # 换成 bucket 所在地区
            'region': 'ap-beijing',
            # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
            # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
            'allow_prefix': '*',
            # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
            'allow_actions': [
                'name/cos:PostObject',
                'name/cos:DeleteObject',
            ],

        }

        sts = Sts(config)
        response = sts.get_credential()
        return Response(response)


class IssueView(APIView):
    """
    发布文章
    """

    def post(self, request, *args, **kwargs):
        print(request.data)
        userinfo = request.data.get("userinfo")  # 获取到用户对象
        user_obj = models.UserInfo.objects.filter(phone=userinfo.get("phone")).first()
        if not user_obj:
            return Response({"status": False, "code": "error", "msg": "用户未登录"})
        image = request.data.get("image")  # 拿到体图片url

        content = request.data.get("content")  # 内容

        article_obj = models.Article.objects.create(author=user_obj, cover_url=image[0], summary=content[:10])

        location = request.data.get("location")
        content = request.data.get("content")
        topic = models.Topic.objects.filter(id=request.data.get("topic")).first()
        articledetail_obj = models.ArticleDetail.objects.create(article=article_obj, location=location, content=content,
                                                                topic=topic)
        image_obj_list = []
        for url in image:
            image_obj_list.append(models.Image(url=url, articledetial=articledetail_obj))
        models.Image.objects.bulk_create(image_obj_list)  # 返回model对象
        return Response({"status": True, "code": "ok", "msg": "发布成功"})


class IssueCreateView(CreateAPIView):
    authentication_classes = [CoerceAuth, ]
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        new_obj = serializer.save(author_id=1)
        return new_obj


class ShowArticleView(APIView):

    def get(self, request, *args, **kwargs):
        query_set = models.Article.objects.all().order_by("-id")
        page_obj = PageNumberPagination()
        result = page_obj.paginate_queryset(query_set, request, self)  # 参数必须是 QuerySet对象  request  和当前类的对象
        article_objs = ArticleSerializer(instance=result, many=True)  # 序列化
        return Response(article_objs.data)


class ShowArticlesView(ListAPIView):
    queryset = models.Article.objects.all().order_by("-id")[:10]
    serializer_class = ArticleSerializer

    def get_queryset(self):
        print(self.request.query_params)
        min_id = self.request.query_params.get("min_id")
        print(min_id)
        max_id = self.request.query_params.get("max_id")
        if min_id:
            return models.Article.objects.all().filter(id__lt=min_id).order_by("-id")[:10]
        elif max_id:
            return models.Article.objects.all().filter(id__gt=max_id).order_by("id")[:10].reverse()
        else:
            return models.Article.objects.all().order_by("-id")[:10]


class GetArticleDetailView(RetrieveAPIView):
    queryset = models.ArticleDetail
    serializer_class = ArticleDetailSerializer



class CommentView(CreateAPIView, ListAPIView):
    authentication_classes = [CoerceAuth, ]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(commentator_id=1)

    def get_authenticators(self):
        if self.request.method == "GET":
            return [Auth(), ]
        else:
            return [CoerceAuth(),]

    def get_queryset(self):
        root = self.kwargs.get("root")
        queryset = models.Comment.objects.filter(root_id=root)
        return queryset


class ShowArticleDetailView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        articledetial_obj = models.ArticleDetail.objects.filter(article_id=pk).first()
        articledetial_serializer_obj = ArticleDetailSerializer(instance=articledetial_obj, many=False)
        print(articledetial_serializer_obj.data)
        return Response(articledetial_serializer_obj.data)


class ShowArticleDetailsViews(RetrieveAPIView):
    serializer_class = ArticleDetailSerializer

    def get_queryset(self):
        print(self.kwargs)
        return models.ArticleDetail.objects.filter(article_id=self.kwargs.get("pk"))


class TopicView(ListCreateAPIView,):
    queryset = models.Topic.objects.all()
    serializer_class = TopicSerializer




class CareView(CreateAPIView,DestroyAPIView):
    authentication_classes = [CoerceAuth,]
    serializer_class = CareSerializer
    def perform_create(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass
