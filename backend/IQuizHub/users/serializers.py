from rest_framework import serializers

from users.models import User, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = '__all__'
