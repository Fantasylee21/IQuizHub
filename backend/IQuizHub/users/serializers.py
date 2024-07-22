from rest_framework import serializers

from questions.serializers import QuestionSerializer
from users.models import User, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    # 返回发布者的id与名称与问题的id与名称
    author = serializers.CharField(max_length=100)
    author_id = serializers.IntegerField()
    question = serializers.CharField(max_length=100)
    question_id = serializers.IntegerField()
    comment = serializers.CharField(max_length=1000)
    id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = '__all__'
