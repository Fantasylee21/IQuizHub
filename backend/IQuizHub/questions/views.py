from collections import Counter

from rest_framework import mixins, status, generics
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from common.permissions import QuestionWritePermission, QuestionGroupPermission, QuestionReadPermission, \
    QuestionGroupDeletePermission, Issuperuser
from users.models import History, User, Comment
from questions.models import Question, QuestionGroup, Tag, Choice, UserGroup, Favorite
from questions.serializers import QuestionSerializer, QuestionGroupSerializer, TagSerializer, ChoiceSerializer, \
    UserGroupSerializer, UserGroupSimpleSerializer, QuestionGroupSimpleSerializer, FavoriteSerializer, \
    FavoriteGroupSimpleSerializer
from rest_framework import serializers

from users.serializers import UserSerializer, HistorySerializer
from utils.yichat import ask


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
        if not all([title, author, content, answer, type]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        res = ask(
            "我的以下信息中是否包含敏感词，如果有敏感词你应该说”是的“，如果没有敏感词你应该说”不是“\n" + content + " " + title + " " + answer + " " + type)
        if "是的" in res['result']:
            return Response({"error": "题目中包含敏感词"}, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.create(title=title, author=author, content=content, ans=answer, type=type)
        if type == 'multiple_choice' or type == 'single_choice':
            if not choices:
                return Response({"error": "选择题选项不能为空"}, status=status.HTTP_400_BAD_REQUEST)
            for choice in choices:
                ch = Choice.objects.create(content=choice)
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

    def get_all_question_groups(self, request, *args, **kwargs):
        question_groups = QuestionGroup.objects.all()
        page = self.paginate_queryset(question_groups)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def query_questiongroup(self, request, *args, **kwargs):
        title = request.GET.get('title')
        type = request.GET.get('type')

        if not title:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        question_groups = QuestionGroup.objects.filter(title__contains=title)
        if type == "0":
            pass
        elif type == "1":  #
            question_groups = question_groups.filter(author__is_superuser=True)
        elif type == "2":
            question_groups = question_groups.filter(author__is_superuser=False)
        else:
            return Response({"error": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)
        page = self.paginate_queryset(question_groups)

        if page is not None:
            # 序列化数据，包括 question_count 字段
            serializer = QuestionGroupSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=True, permission_classes=[QuestionGroupDeletePermission])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def upload_questionGroup(self, request, *args, **kwargs):
        questions = request.data.get('questions')
        users = request.data.get('users')
        title = request.data.get('title')
        content = request.data.get('content')
        author = request.user
        is_all = request.data.get('is_all')
        if not all([title, author, content]) or is_all is None:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        question_group = QuestionGroup.objects.create(title=title, author=author, content=content, is_all=is_all)
        if questions:
            for question in questions:
                question_group.questions.add(question)
                q = Question.objects.get(id=question)
                if q.is_all:
                    q.is_all = False
                    q.save()
        if not is_all:
            for user in users:
                question_group.members.add(user)
        result = {
            "id": question_group.id,
            "title": question_group.title,
            "author": question_group.author.username
        }
        question_group.save()
        return Response(result, status=status.HTTP_201_CREATED)

    def add_person(self, request, *args, **kwargs):
        question_group = self.get_object()
        users = request.data.get('users')
        if question_group.is_all:
            return Response({"msg": "本题组对所有人可见"}, status=status.HTTP_400_BAD_REQUEST)
        for user in users:  # 如果题组中本来就有这个人了那么报错
            if not User.objects.filter(id=user).exists():
                return Response({f"error": f"用户{user}不存在"}, status=status.HTTP_400_BAD_REQUEST)
            if question_group.members.filter(id=user).exists():
                return Response({f"error": f"用户{user}在题组{question_group.id}已存在"},
                                status=status.HTTP_400_BAD_REQUEST)
        for user in users:
            question_group.members.add(user)
        question_group.save()
        return Response({"msg": "添加成功"}, status=status.HTTP_200_OK)

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

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        data = serializer.data
        userSerializer = UserSerializer(User.objects.filter(id=data['author']).first())
        data['author'] = {key: userSerializer.data[key] for key in ['id', 'username', 'avatar', 'introduction']}
        return Response(data, status=status.HTTP_200_OK)

    # 统计题组中我的通过的题目的数量，其中不能统计重复做过的题目,不能统计题目id相同的数量
    def get_my_success_cnt(self, request, *args, **kwargs):
        user = request.user
        question_group = self.get_object()
        historys = user.historys.filter(question__in=question_group.questions.all(), correct=True).values_list(
            'question_id', flat=True).distinct()
        cnt = len(historys)
        return Response({"correct_cnt": cnt, "all_cnt": len(question_group.questions.all())}, status=status.HTTP_200_OK)


class QuestionReadView(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, QuestionReadPermission]
    pagination_class = PageNumberPagination

    def check_question(self, request, *args, **kwargs):
        question_id = request.data.get("question_id")
        ans = request.data.get("ans")
        user = request.user
        if not all([question_id, ans]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if not Question.objects.filter(id=question_id).exists():
            return Response({"error": "问题不存在"}, status=status.HTTP_400_BAD_REQUEST)
        question = Question.objects.get(id=question_id)
        if question.ans == ans:
            his = History.objects.create(question=question, correct=True)
            his.save()
            user.historys.add(his)
            return Response({"message": True}, status=status.HTTP_200_OK)
        else:
            his = History.objects.create(question=question, correct=False)
            his.save()
            user.historys.add(his)
            return Response({"message": False}, status=status.HTTP_200_OK)

    # 通过题目的title模糊查询含有相关词语的题目，返回所有相关的题目,其中tag为一个列表，包含所有要查询的标签,返回的所有题目必须=
    # 要包含所有的提供的tags的id
    def query_question(self, request, *args, **kwargs):
        title = request.GET.get('title')
        tags = request.GET.getlist('tags')
        type = request.GET.get('type')
        if not title and not tags:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        questions = Question.objects.all()
        if title:
            print("title")
            questions = questions.filter(title__contains=title)
        if tags:
            # print(tags)
            for tag in tags:
                if tag:
                    questions = questions.filter(tags__name=tag)

        if type:
            questions = questions.filter(type=type)
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def get_all_questions(self, request, *args, **kwargs):
        questions = Question.objects.all()
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def get_recommend_questions(self, request, *args, **kwargs):
        user = request.user
        # 收集用户历史中所有问题的所有标签
        tags = set()
        for history in user.historys.all():
            for tag in history.question.tags.all():
                tags.add(tag.name)  # 确保添加的是标签的名称

        # 如果没有标签，返回所有问题的响应
        if not tags:
            return self.get_all_questions(request, *args, **kwargs)  # 注意这里self应该传给get_all_questions方法

        # 统计标签频率
        tag_counts = Counter(tags)

        # 选择出现频率最高的标签，这里选择前5个最高频的标签
        top_tags = tag_counts.most_common(5)  # 这里假设选择前5个标签

        # 根据标签推荐问题
        recommended_questions = Question.objects.filter(
            tags__name__in=[tag_name for tag_name, count in top_tags]  # 使用标签名称进行过滤
        ).distinct()

        # 分页处理
        page = self.paginate_queryset(recommended_questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


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


class UserGroupView(GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer

    def upload_userGroup(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        author = request.user
        type = request.data.get('type')
        if not all([title, content, author, type]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        usergroup = UserGroup.objects.create(title=title, content=content, author=author, type=type)
        result = {
            "id": usergroup.id,
            "title": usergroup.title,
            "author": usergroup.author.username,
            "content": usergroup.content
        }
        return Response(result, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, Issuperuser])
    def upload_comment(self, request, *args, **kwargs):
        comment = request.data.get('comment')
        usergroup = request.data.get('usergroup')
        author = request.user
        if not all([comment, usergroup, author]):
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if not UserGroup.objects.filter(id=usergroup).exists():
            return Response({"error": "用户组不存在"}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(comment=comment, usergroup=UserGroup.objects.filter(id=usergroup).first(),
                                         author=author)
        comment.save()
        result = {
            "id": comment.id,
            "comment": comment.comment,
            "author": comment.author.username
        }
        return Response(result, status=status.HTTP_201_CREATED)

    def upload_content(self, request, *args, **kwargs):
        content = request.data.get('content')
        obj = self.get_object()
        if not content:
            return Response({"error": "内容不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(obj, data={"content": content}, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.errors:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"content": serializer.data['content']}, status=status.HTTP_200_OK)

    def get_all_usergroups(self, request, *args, **kwargs):
        usergroups = UserGroup.objects.all()
        page = self.paginate_queryset(usergroups)
        if page is not None:
            serializer = UserGroupSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def query_usergroup(self, request, *args, **kwargs):
        title = request.GET.get('title')
        type = request.GET.get('type')
        usergroups = UserGroup.objects.all()
        if type == '0':
            pass
        elif type == '1':
            usergroups = usergroups.filter(type__in=['academic'])
        elif type == '2':
            usergroups = usergroups.filter(type__in=['enterprise'])
        elif type == '3':
            usergroups = usergroups.filter(type__in=['person'])
        elif type == '4':
            usergroups = usergroups.filter(type__in=['other'])
        else:
            return Response({"error": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)
        if title:
            usergroups = usergroups.filter(title__contains=title)
        page = self.paginate_queryset(usergroups)
        if page is not None:
            serializer = UserGroupSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def get_usergroup(self, request, *args, **kwargs):
        usergroup = self.get_object()
        serializer = self.get_serializer(usergroup)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def add_member(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if not user:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if obj.members.filter(id=user.id).exists():
            return Response({"error": "用户已在该用户组中"}, status=status.HTTP_400_BAD_REQUEST)
        obj.members.add(user)
        return Response({"message": "添加成功"}, status=status.HTTP_200_OK)

    def delete_users(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if not user:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if not obj.members.filter(id=user.id).exists():
            return Response({"error": "用户不在该用户组中"}, status=status.HTTP_400_BAD_REQUEST)
        obj.members.remove(user)
        return Response({"message": "删除成功"}, status=status.HTTP_200_OK)

    @action(detail=True, permission_classes=[QuestionGroupDeletePermission])
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class FavoriteView(GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def favorite(self, request, *args, **kwargs):
        user = request.user
        question = request.data.get('question')
        questiongroup = request.data.get('questiongroup')
        if not question and not questiongroup:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if question:
            if Favorite.objects.filter(author=user, question=question).exists():
                favorite = Favorite.objects.get(author=user, question=question)
                favorite.delete()
                return Response({"message": "删除成功"}, status=status.HTTP_200_OK)
            else:
                favorite = Favorite.objects.create(author=user, question=Question.objects.get(id=question))
                favorite.save()
                return Response({"message": "收藏成功"}, status=status.HTTP_200_OK)
        if questiongroup:
            if Favorite.objects.filter(author=user, questiongroup=questiongroup).exists():
                favorite = Favorite.objects.get(author=user, questiongroup=questiongroup)
                favorite.delete()
                return Response({"message": "删除成功"}, status=status.HTTP_200_OK)
            else:
                favorite = Favorite.objects.create(author=user, questiongroup=QuestionGroup.objects.get(id=questiongroup))
                favorite.save()
                return Response({"message": "收藏成功"}, status=status.HTTP_200_OK)
        return Response({"error": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)

    def get_favorite(self, request, *args, **kwargs):
        user = request.GET.get('user')
        type = request.GET.get('type')
        if not user:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=user).exists():
            return Response({"error": "用户不存在"}, status=status.HTTP_400_BAD_REQUEST)
        if type == '0':
            favorites = Favorite.objects.filter(author=user)
            serializer = FavoriteGroupSimpleSerializer(favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif type == '1':
            favorites = Favorite.objects.filter(author=user, question__isnull=False)
            page = self.paginate_queryset(favorites)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        elif type == '2':
            favorites = Favorite.objects.filter(author=user, questiongroup__isnull=False)
            page = self.paginate_queryset(favorites)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        else:
            return Response({"error": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        question = request.data.get('question')
        questiongroup = request.data.get('questiongroup')
        if not question and not questiongroup:
            return Response({"error": "参数不全"}, status=status.HTTP_400_BAD_REQUEST)
        if question:
            if not Favorite.objects.filter(author=user, question=question).exists():
                return Response({"err": "未收藏过"}, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.get(author=user, question=question)
            favorite.delete()
            return Response({"message": "删除成功"}, status=status.HTTP_200_OK)
        if questiongroup:
            if not Favorite.objects.filter(author=user, questiongroup=questiongroup).exists():
                return Response({"err": "未收藏过"}, status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorite.objects.get(author=user, questiongroup=questiongroup)
            favorite.delete()
            return Response({"message": "删除成功"}, status=status.HTTP_200_OK)
        return Response({"error": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)
