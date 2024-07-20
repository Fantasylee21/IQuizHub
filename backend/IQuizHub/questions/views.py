from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from common.permissions import QuestionWritePermission, QuestionGroupPermission, QuestionReadPermission, \
    QuestionGroupDeletePermission, Issuperuser
from questions.models import Question, QuestionGroup, Tag
from questions.serializers import QuestionSerializer, QuestionGroupSerializer, TagSerializer


# Create your views here.

# class QuestionView(GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAuthenticated, QuestionWritePermission]


class QuestionWriteView(GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, QuestionWritePermission]

    def post(self, request):
        title = request.data.get('title')
        author = request.user
        content = request.data.get('content')
        answer = request.data.get('answer')
        type = request.data.get('type')
        print(title, author, content, answer, type)
        if not all([title, author, content, answer, type]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.create(title=title, author=author, content=content, ans=answer, type=type)
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
        return Response({"message": "删除标签成功"}, status=status.HTTP_200_OK)


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
        author = request.user
        if not all([questions, title, author]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        question_group = QuestionGroup.objects.create(title=title, author=author)
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


class TagView(GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, Issuperuser]

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
