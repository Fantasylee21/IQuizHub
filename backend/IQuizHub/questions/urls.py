from django.urls import path

from questions.views import QuestionWriteView, QuestionGroupView, QuestionReadView, TagView, UserGroupView,FavoriteView

urlpatterns = [
    path('upload/', QuestionWriteView.as_view({'post': 'post'}), name='上传题目'),
    path('detail/<int:pk>/', QuestionReadView.as_view({'get': 'retrieve'}), name='题目详情'),
    path('update/<int:pk>/', QuestionWriteView.as_view({'put': 'update_content'}), name='题目修改'),
    path('questiongroup/content/update/<int:pk>/', QuestionGroupView.as_view({'post': 'upload_content'}),
         name='上传题目组信息'),
    path('delete/<int:pk>/', QuestionWriteView.as_view({'delete': 'destroy'}), name='题目删除'),
    path('questiongroup/upload/', QuestionGroupView.as_view({'post': 'upload_questionGroup'}),
         name='新建题目列表'),
    path('questiongroup/delete/<int:pk>/', QuestionGroupView.as_view({'delete': 'destroy'}), name='删除题目组'),
    path('questiongroup/detail/<int:pk>/', QuestionGroupView.as_view({'get': 'retrieve'}), name='返回题目列表'),
    path('questiongroup/addquestion/<int:pk>/', QuestionGroupView.as_view({'post': 'add_question'}),
         name='向题组添加题目'),
    path('questiongroup/addperson/<int:pk>/', QuestionGroupView.as_view({'post': 'add_person'}),
         name='向题组添加人物'),
    path('questiongroup/deletequestion/<int:pk>/', QuestionGroupView.as_view({'delete': 'delete_question'}),
         name='删除题目组'),
    path('questiongroup/update/<int:pk>/', QuestionGroupView.as_view({'put': 'update'})),
    path('questiongroup/all/', QuestionGroupView.as_view({'get': 'get_all_question_groups'}), name='获取所有题目组'),
    path('questiongroup/querypass/<int:pk>/', QuestionGroupView.as_view({'get': 'get_my_success_cnt'})),
    path('questiongroup/put/<int:pk>/', QuestionGroupView.as_view({'put': 'update_avatar'}), name='更新题目组'),
    path('tag/upload/', TagView.as_view({'put': 'upload_tag'}), name='上传标签'),
    path('tag/delete/<int:pk>/', TagView.as_view({'delete': 'destroy'}), name='删除标签'),
    path('modifytag/<int:pk>/',
         QuestionWriteView.as_view({'put': 'add_tag_to_question', 'delete': 'delete_tag_from_question'}),
         name='给题目添加标签'),
    path('query/question/', QuestionReadView.as_view({'get': 'query_question'}), name='查询题目'),
    path('get/questions/', QuestionReadView.as_view({'get': 'get_all_questions'}), name='获取题目'),
    path('check/question/', QuestionReadView.as_view({'post': 'check_question'}), name='检查题目'),
    path('get/selfquestions/', QuestionReadView.as_view({'get': 'get_recommend_questions'}), name='获取自己推荐的题目'),
    path('guestiongroup/query/', QuestionGroupView.as_view({'get': 'query_questiongroup'}), name='查询题目组'),
    path('usergroup/upload/', UserGroupView.as_view({'post':'upload_userGroup'}), name='上传用户组'),
    path('usergroup/delete/<int:pk>/', UserGroupView.as_view({'delete': 'delete'}), name='删除用户组'),
    path('usergroup/detail/', UserGroupView.as_view({'get': 'get_all_usergroups'}), name='返回用户组'),
    path('usergroup/query/', UserGroupView.as_view({'get': 'query_usergroup'}), name='查询用户组'),
    path('usergroup/addmember/<int:pk>/', UserGroupView.as_view({'post': 'add_member'}), name='添加成员'),
    path('usergroup/deletemember/<int:pk>/', UserGroupView.as_view({'delete': 'delete_users'}), name='删除成员'),
    path('usergroup/uploadcontent/<int:pk>/', UserGroupView.as_view({'put': 'upload_content'}), name='上传用户组内容'),
    path('usergroup/uploadcomment/', UserGroupView.as_view({'put': 'upload_comment'}), name='上传用户组评论'),
    path('usergroup/detail/<int:pk>/', UserGroupView.as_view({'get': 'get_usergroup'}), name='返回用户组详情'),
    path('favorite/', FavoriteView.as_view({'post': 'favorite'}), name='收藏题目'),
    path('favorite/delete/', FavoriteView.as_view({'delete': 'delete'}), name='取消收藏'),
    path('favorite/query/', FavoriteView.as_view({'get': 'get_favorite'}), name='查询收藏'),
]
