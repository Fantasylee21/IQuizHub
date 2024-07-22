from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import mixins, status, generics
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
# from rest_framework.mixins.RetrieveModelMixin import retrieve
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from common.permissions import QuestionWritePermission, QuestionGroupPermission, QuestionReadPermission, \
    QuestionGroupDeletePermission, Issuperuser
from questions.models import Question, QuestionGroup, Tag, Choice
from questions.serializers import QuestionSerializer, QuestionGroupSerializer, TagSerializer, ChoiceSerializer
from rest_framework import serializers


# Create your views here.

# class QuestionView(GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAuthenticated, QuestionWritePermission]


class QuestionWriteView(GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, QuestionWritePermission]

    def update_content(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = QuestionSerializer(obj, data=request.data, partial=True)
        # 检查请求中的数据并更新序列化器数据
        data = {}
        if 'title' in request.data:
            data['title'] = request.data.get('title')
        if 'content' in request.data:
            data['content'] = request.data.get('content')
        if 'answer' in request.data:
            data['ans'] = request.data.get('answer')
        if 'type' in request.data:
            data['type'] = request.data.get('type')
        # 如果没有要更新的字段，则返回错误
        if not data:
            return Response({"error": "没有传入要更新的参数"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.update(obj, data)
        return Response({"msg": "成功修改"}, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        author = request.user
        content = request.data.get('content')
        answer = request.data.get('answer')
        type = request.data.get('type')
        choices = request.data.get('choices')
        # print(title, author, content, answer, type)
        if not all([title, author, content, answer, type]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.create(title=title, author=author, content=content, ans=answer, type=type)
        if type == 'multiple_choice' or type == 'single_choice':
            if not choices:
                return Response({"error": "选择题选项不能为空"}, status=status.HTTP_400_BAD_REQUEST)
            for choice in choices:
                if not all([choice.get("content"), choice.get("option")]):
                    return Response({"error": "选项参数不全"}, status=status.HTTP_400_BAD_REQUEST)
                ch = Choice.objects.create(content=choice.get("content"),
                                           option=choice.get("option"))
                question.choices.add(ch)
                question.save()
        result = {
            "id": question.id,
            "title": question.title,
            "author": question.author.username
        }
        return Response(result, status=status.HTTP_201_CREATED)

    def add_tag_to_question(self, request, *args, **kwargs):
        obj = self.get_object()
        tag = request.data.get('tag')
        if not tag:
            return Response({"error": "标签不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        if not Tag.objects.filter(id=tag).exists():
            return Response({"error": "标签不存在"}, status=status.HTTP_400_BAD_REQUEST)
        obj.tags.add(tag)
        return Response({"message": "添加标签成功"}, status=status.HTTP_200_OK)

    def delete_tag_from_question(self, request, *args, **kwargs):
        obj = self.get_object()
        tag = request.data.get('tag')
        if not tag:
            return Response({"error": "标签不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        if not Tag.objects.filter(id=tag).exists():
            return Response({"error": "标签不存在"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj.tags.remove(tag)
        except Exception as e:
            return Response({"error": f"删除标签失败{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": f"删除标签成功{tag}"}, status=status.HTTP_200_OK)


class QuestionGroupView(GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerializer
    permission_classes = [IsAuthenticated, QuestionGroupPermission]

    @action(detail=True, permission_classes=[QuestionGroupDeletePermission])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def upload_questionGroup(self, request, *args, **kwargs):
        questions = request.data.get('questions')
        users = request.data.get('users')
        title = request.data.get('title')
        content = request.data.get('content')
        author = request.user
        if not all([questions, title, author]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        question_group = QuestionGroup.objects.create(title=title, author=author, content=content)
        for question in questions:
            question_group.questions.add(question)
            q = Question.objects.get(id=question)
            if q.is_all:
                q.is_all = False
                q.save()
        for user in users:
            question_group.members.add(user)
        result = {
            "id": question_group.id,
            "title": question_group.title,
            "author": question_group.author.username
        }
        question_group.save()
        return Response(result, status=status.HTTP_201_CREATED)

    def add_question(self, request, *args, **kwargs):
        question_group = self.get_object()
        questions = request.data.get('questions')
        if not questions:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        for question in questions:
            if not Question.objects.filter(id=question).exists():
                return Response({f"error": f"问题{question}不存在"}, status=status.HTTP_400_BAD_REQUEST)
            # if question in [q.id for q in question_group.questions.all()]:
            if question_group.questions.filter(id=question).exists():
                return Response({f"error": f"问题{question}在题组{question_group.id}已存在"},
                                status=status.HTTP_400_BAD_REQUEST)
        for question in questions:
            question_group.questions.add(question)
            q = Question.objects.get(id=question)
            if q.is_all:
                q.is_all = False
                q.save()
        return Response({f"message": f"添加成功{questions}"}, status=status.HTTP_200_OK)

    def delete_question(self, request, *args, **kwargs):
        question_group = self.get_object()
        questions = request.data.get('questions')
        if not questions:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        for question in questions:
            if not Question.objects.filter(id=question).exists():
                return Response({f"error": f"问题{question}不存在"}, status=status.HTTP_400_BAD_REQUEST)
            if not question_group.questions.filter(id=question).exists():
                return Response({f"error": f"问题{question}不在题组{question_group.id}中"},
                                status=status.HTTP_400_BAD_REQUEST)
        for question in questions:
            question_group.questions.remove(question)
            # if question_group.questions.filter(id=question).count() == 0:
            #     q = Question.objects.get(id=question)
            #     q.is_all = True
            #     q.save()
        return Response({f"message": f"删除成功{questions}"}, status=status.HTTP_200_OK)

    def upload_content(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response({"error": "题组不存在"}, status=status.HTTP_400_BAD_REQUEST)
        content = request.data.get('content')
        if not content:
            return Response({"error": "问题组内容不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = self.get_serializer(obj, data={"content": content}, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.errors:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({"content": serializer.data['content']}, status=status.HTTP_200_OK)


class QuestionReadView(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, QuestionReadPermission]
    pagination_class = PageNumberPagination
    # page_size = 10  # 你可以根据需要设置每页的项目数

    # pagination_class = LimitOffsetPagination

    # 通过题目的title模糊查询含有相关词语的题目，返回所有相关的题目,其中tag为一个列表，包含所有要查询的标签,返回的所有题目必须=
    # 要包含所有的提供的tags的id
    def query_question(self, request, *args, **kwargs):
        title = request.data.get('title')
        tags = request.data.get('tags')
        if not title:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if not tags:
            questions = Question.objects.filter(title__contains=title)
            page = self.paginate_queryset(questions)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response({"error": "没有数据"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            questions = Question.objects.filter(title__contains=title)
            for tag in tags:
                questions = questions.filter(tags=tag)
            page = self.paginate_queryset(questions)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response({"error": "没有数据"}, status=status.HTTP_400_BAD_REQUEST)


    def get_all_questions(self, request, *args, **kwargs):
        questions = Question.objects.all()
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response({"error": "没有数据"}, status=status.HTTP_400_BAD_REQUEST)


class TagView(GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, Issuperuser]
    pagination_class = PageNumberPagination

    def upload_tag(self, request, *args, **kwargs):
        name = request.data.get('name')
        if not name:
            return Response({"error": "标签名不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        if Tag.objects.filter(name=name).exists():
            return Response({"error": "标签名已存在"}, status=status.HTTP_400_BAD_REQUEST)
        tag = Tag.objects.create(name=name)
        result = {
            "id": tag.id,
            "name": tag.name,
        }
        return Response(result, status=status.HTTP_201_CREATED)
