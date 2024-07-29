import os
import random
import re

from django.core.mail import send_mail
from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

from questions.serializers import QuestionGroupSimpleSerializer
from users.serializers import UserSerializer, CommentSerializer, HistorySerializer, UserSimpleSerializer
from IQuizHub.settings import MEDIA_ROOT
from users.models import User, Captcha, Comment, History
from common.permissions import UserPermission, CommentDeletePermission
from common.aliyunapi import AliyunSMS
from questions.models import Question, QuestionGroup


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

        result = serializer.validated_data
        result['username'] = serializer.user.username
        result['id'] = serializer.user.id
        result['moblie'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['token'] = result.pop('access')
        return Response(result, status=status.HTTP_200_OK)


class RigisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        passwordConfirm = request.data.get('passwordconfirm')
        codeID = request.data.get('codeID')
        captcha = request.data.get('captcha')
        mobile = request.data.get('mobile')
        # 从captcha的数据库中查询ID为codeID的capatcha
        if not Captcha.objects.filter(id=codeID).exists():
            return Response({"error": "验证码ID错误"}, status=status.HTTP_400_BAD_REQUEST)
        tmp = Captcha.objects.get(id=codeID)
        if tmp.captcha != captcha:
            return Response({"error": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        if tmp.mobile != mobile:
            return Response({"error": "手机号与验证码不匹配错误"}, status=status.HTTP_400_BAD_REQUEST)
        # print(username, email, password, passwordConfirm)
        if not all([username, email, password, passwordConfirm, codeID, captcha]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "用户名已注册"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "用户邮箱已注册"}, status=status.HTTP_400_BAD_REQUEST)

        if password != passwordConfirm:
            return Response({"error": "两次密码不一致"}, status=status.HTTP_400_BAD_REQUEST)

        # 校验密码强度
        if not 6 < len(password) < 18:
            return Response({"error": "密码长度不在要求范围内"}, status=status.HTTP_400_BAD_REQUEST)
        # 匹配邮箱
        if re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email) is None:
            return Response({"error": "邮箱格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        tmp.delete()

        user = User.objects.create_user(username=username, email=email, password=password, mobile=mobile)
        result = {
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }
        return Response(result, status=status.HTTP_201_CREATED)


class UserView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]

    def avatar_upload(self, request, *args, **kwargs):
        obj = self.get_object()
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({"error": "头像不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not avatar.name.endswith('.jpg') and not avatar.name.endswith('.png'):
            return Response({"error": "头像格式错误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if avatar.size > 1024 * 300:
            return Response({"error": "头像过大"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = self.get_serializer(obj, data={"avatar": avatar}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"url": serializer.data['avatar']}, status=status.HTTP_200_OK)

    def upload_introduction(self, request, *args, **kwargs):
        obj = self.get_object()
        introduction = request.data.get('introduction')
        if not introduction:
            return Response({"error": "个人简介不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = self.get_serializer(obj, data={"introduction": introduction}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"introduction": serializer.data['introduction']}, status=status.HTTP_200_OK)

    def get_questiongroup(self, request, *args, **kwargs):
        user = request.user
        questiongroup = QuestionGroup.objects.filter(author=user)
        serializer = QuestionGroupSimpleSerializer(questiongroup, many=True)


        return Response(serializer.data, status=status.HTTP_200_OK)
class UserReadView(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_history(self, request, *args, **kwargs):
        user = self.get_object()
        historys = user.historys.all().order_by('-create_time')
        serializer = HistorySerializer(historys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_all_user(self, request, *args, **kwargs):
        users = User.objects.all()  # 这里需要添加圆括号
        serializer = UserSimpleSerializer(users,many=True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)



class FileView(APIView):
    """获取文件的视图"""
    def get(self, request, name):
        path = os.path.join(MEDIA_ROOT, name)
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error':"没有找到该文件"}, status=status.HTTP_404_NOT_FOUND)


class CaptchaView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({"error": "手机号不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile=mobile).exists():
            return Response({"error": "手机号已注册"}, status=status.HTTP_400_BAD_REQUEST)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return Response({"error": "手机号格式错误"}, status=status.HTTP_400_BAD_REQUEST)
        code = str(random.randint(1000, 9999))
        sms = AliyunSMS()
        res = sms.send_sms(mobile, code)

        if res['code'] == 'error':
            return Response({"error": res['msg']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            captcha = Captcha.objects.create(mobile=mobile, captcha=code)
            res['codeID'] = captcha.id
            return Response(res, status=status.HTTP_200_OK)


class CommentView(GenericViewSet, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer = CommentSerializer

    def upload_comment(self, request, *args, **kwargs):
        comment = request.data.get('comment')
        question = request.data.get('question')
        if not all([comment, question]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=request.user.id).exists():
            return Response({"error": "用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
        if not Question.objects.filter(id=question).exists():
            return Response({"error": "问题不存在"}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(comment=comment, question_id=question, author_id=request.user.id)
        serializers = self.serializer(comment)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    # 获取评论按照时间顺序进行排序

    def get_comment(self, request, *args, **kwargs):
        question = request.GET.get('question')
        user = request.GET.get('user')
        usergroup = request.GET.get('usergroup')

        if usergroup:
            if not User.objects.filter(id=usergroup).exists():
                return Response({"error": "用户组不存在"}, status=status.HTTP_400_BAD_REQUEST)
            comments = Comment.objects.filter(usergroup_id=usergroup).order_by('-create_time')
            page = self.paginate_queryset(comments)
            if page is not None:
                serializer = self.serializer(page, many=True)
                return self.get_paginated_response(serializer.data)


        if question and user:
            # print(question, user)
            if not Question.objects.filter(id=question).exists():
                return Response({"error": "问题不存在"}, status=status.HTTP_400_BAD_REQUEST)
            if not User.objects.filter(id=user).exists():
                return Response({"error": "用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
            comments = Comment.objects.filter(question_id=question, author_id=user).order_by('-create_time')
            page = self.paginate_queryset(comments)
            if page is not None:
                serializer = self.serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        if question:
            if not Question.objects.filter(id=question).exists():
                return Response({"error": "问题不存在"}, status=status.HTTP_400_BAD_REQUEST)
            comments = Comment.objects.filter(question_id=question).order_by('-create_time')
            page = self.paginate_queryset(comments)
            if page is not None:
                serializer = self.serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        if user:
            if not User.objects.filter(id=user).exists():
                return Response({"error": "用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
            comments = Comment.objects.filter(author_id=user).order_by('-create_time')
            page = self.paginate_queryset(comments)
            if page is not None:
                serializer = self.serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[CommentDeletePermission], methods=['delete'])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
