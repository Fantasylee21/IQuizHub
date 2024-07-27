from rest_framework import serializers

from users.models import Comment
from questions.models import Question, QuestionGroup, Tag, Choice, UserGroup, Favorite
from users.serializers import UserSimpleSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'create_time', 'update_time', 'name']

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    # tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # choices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # tags = serializers.StringRelatedField(many=True)
    choices = serializers.SlugRelatedField(many=True, read_only=True, slug_field='content')
    tags = TagSerializer(many=True, read_only=True)

    # choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ['is_all']

    def create(self, validated_data):
        """保存问题时，确保作者是请求的用户"""
        author = self.context['request'].user
        validated_data['author'] = author
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新问题时，确保作者是请求的用户"""
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

    # def to_representation(self, instance):
    #     """序列化时添加标签和选项数据"""
    #     representation = super().to_representation(instance)
    #     tags = instance.tags.all()
    #     representation['tags'] = TagSerializer(tags, many=True).data
    #     if instance.type in ['single_choice', 'multiple_choice']:
    #         choices = instance.choices.all()
    #         representation['choices'] = ChoiceSerializer(choices, many=True).data
    #     return representation


class QuestionGroupSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    questionCnt = serializers.SerializerMethodField()  # 添加这个方法字段
    favoriteCnt = serializers.SerializerMethodField()  # 添加这个方法字段
    passedCnt = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = QuestionGroup
        fields = "__all__"

    def get_questionCnt(self, obj):
        # 计算与问题组关联的题目数量
        return Question.objects.filter(question_groups=obj).count()

    def get_favoriteCnt(self, obj):
        return Favorite.objects.filter(questiongroup=obj).count()

    def get_passedCnt(self, obj):

        request = self.context.get('request', None)
        question_group = obj
        user = request.user
        historys = user.historys.filter(question__in=question_group.questions.all(), correct=True).values_list(
            'question_id', flat=True).distinct()
        cnt = len(historys)
        return cnt

    def get_is_favorite(self, obj):
        request = self.context.get('request', None)
        user = request.user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(questiongroup=obj, author=user).exists()


class UserGroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # author = UserSimpleSerializer()

    class Meta:
        model = UserGroup
        fields = "__all__"


class UserGroupSimpleSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    cnt = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        exclude = ['members']

    def get_cnt(self, obj):
        return Comment.objects.filter(usergroup=obj).count()


class QuestionGroupSimpleSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = QuestionGroup
        fields = ['id', 'title', 'avatar', 'content']


class FavoriteSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'create_time', 'author', 'question', 'questiongroup']


class FavoriteGroupSimpleSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    questiongroup = QuestionGroupSimpleSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'create_time', 'author', 'question', 'questiongroup']
