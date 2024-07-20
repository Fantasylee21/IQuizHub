from rest_framework import serializers
from .models import Question, QuestionGroup, Tag


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'create_time', 'update_time', 'title', 'content', 'author', 'type']

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


class QuestionGroupSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = QuestionGroup
        fields = "__all__"


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