from django.db import models

from users.models import User

# Create your models here.
class Question(models.Model):
    """问题模型类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    title = models.CharField(max_length=100, verbose_name='问题标题')
    content = models.TextField(verbose_name='问题内容')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='作者', default=None)
    CONTENT_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_in_the_blank', 'Fill in the Blank'),
        ('single_choice', 'Single Choice'),
    ]
    type = models.CharField(max_length=20, choices=CONTENT_CHOICES, default='single_choice', verbose_name='问题类型')
    ans = models.TextField(verbose_name='问题答案', default=None)
    is_all = models.BooleanField(default=True, verbose_name='是否为全部题目')
    tags = models.ManyToManyField('Tag', related_name='questionsTags', verbose_name='标签')
    choices = models.ManyToManyField('Choice', related_name='questionsChoices', verbose_name='选项')

    class Meta:
        db_table = 'questions'
        verbose_name = '问题表'
        verbose_name_plural = verbose_name
        # ordering = ['-create_time']

    def __str__(self):
        return self.title


class QuestionGroup(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    title = models.CharField(max_length=100, verbose_name='问题组标题')
    questions = models.ManyToManyField(
        'Question',
        related_name='question_groups',
        verbose_name='问题'
    )
    members = models.ManyToManyField(
        'users.User',
        related_name='member_question_groups',
        verbose_name='组员'
    )
    author = models.ForeignKey(
        'users.User',
        verbose_name='作者',
        on_delete=models.CASCADE,
        default=None
    )
    content = models.TextField(verbose_name='问题组内容', default="作者很懒，什么都没有留下")

    class Meta:
        db_table = 'question_groups'
        verbose_name = '问题组表'
        verbose_name_plural = verbose_name
        # ordering = ['-create_time']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """标签模型类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    name = models.CharField(max_length=20, verbose_name='标签名称', unique=True)

    # questions = models.ManyToManyField('Question', related_name='tagsQuestions', verbose_name='问题')

    class Meta:
        db_table = 'tags'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name
        # ordering = ['-create_time']

    def __str__(self):
        return self.name


class Choice(models.Model):
    """选项模型类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    content = models.TextField(verbose_name='选项内容')

    class Meta:
        db_table = 'choices'
        verbose_name = '选项表'
        verbose_name_plural = verbose_name
        # ordering = ['-create_time']

    def __str__(self):
        return self.content

class UserGroup(models.Model):
    """用户组模型类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    title = models.CharField(max_length=100, verbose_name='用户组标题')
    members = models.ManyToManyField(
        'users.User',
        related_name='user_groups',
        verbose_name='组员'
    )
    author = models.ForeignKey(
        'users.User',
        verbose_name='作者',
        on_delete=models.CASCADE,
        default=None
    )
    content = models.TextField(verbose_name='用户组内容', default="作者很懒，什么都没有留下")
    CONTENT_CHOICES = [
        ('academic', '学术版'),
        ('enterprise', '企业版'),
        ('person', '个人版'),
        ('other', '其他'),
    ]
    type = models.CharField(max_length=20, choices=CONTENT_CHOICES, default='person', verbose_name='群组类型')


    class Meta:
        db_table = 'user_groups'
        verbose_name = '用户组表'
        verbose_name_plural = verbose_name
        # ordering = ['-create_time']

    def __str__(self):
        return self.title


if __name__ == '__main__':
    questionGroup = QuestionGroup.objects.create(title='test', author=User.objects.get(pk=6))
