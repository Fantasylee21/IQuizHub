<template>
    <div class="group-detail-header">
        <div class="gd-header-container">
            <el-breadcrumb separator="/" class="breadcrumb">
                <el-breadcrumb-item :to="{ path: '/staging' }">staging</el-breadcrumb-item>
                <el-breadcrumb-item :to="{ path: '/groupPage' }">group-page</el-breadcrumb-item>
                <el-breadcrumb-item>
                    <a href="#">sheet-detail</a>
                </el-breadcrumb-item>
            </el-breadcrumb>
          <h1>Group Detail</h1>
        </div>
    </div>

<div class="sheet-detail-container">
        <div class="sheet-detail-nav">
            <el-tabs class="demo-tabs">
                    <div class="sheet-description">
                        <div class="description-left">
                            <el-card>
                                <h2>Group Description</h2>
                                <div v-html="sheetData?.content"></div>
                            </el-card>
                            <el-card style="margin-top: 50px">
                                    <div class="comment-header" style="display: flex; justify-content: space-between; align-items: center">
                                      <h2 style="margin-bottom: 20px; font-size: 20px; font-weight: bold">Comment List</h2>
                                      <el-popover placement="right" :width="400" trigger="click">
                                          <template #reference>
                                              <el-button style="margin-right: 16px">Comment</el-button>
                                          </template>
                                          <div class="comment-input">
                                              <el-button type="primary" style="margin-bottom: 10px" @click="submitComment">Issue</el-button>
                                              <el-input
                                                      v-model="userComment"
                                                      :rows="2"
                                                      type="textarea"
                                                      placeholder="Please input"
                                              />
                                          </div>
                                      </el-popover>
                                  </div>
                                  <div class="content-list">
                                      <div v-for="(comment, index) in comments" :key="index" class="comment">
                                          <img :src="comment.author.avatar" class="avatar"/>
                                          <div class="comment-details">
                                              <p class="commenter-name">{{ comment.author.username }}</p>
                                              <p class="comment-content">{{ comment.comment }}</p>
                                          </div>
                                      </div>

                                      <el-pagination
                                              @current-change="handleCurrentChange"
                                              :current-page="currentPage"
                                              :page-size="pageSize"
                                              :total="totalComments">
                                      </el-pagination>
                                  </div>
                            </el-card>
                        </div>
                        <div class="description-right">
                            <el-card class="detail-card">
                                <div class="sheet-id">
                                    <p>Group Id</p>
                                    <p style="padding-right: 15px">{{ sheetData?.id }}</p>
                                </div>
                                <div class="sheet-creator">
                                    <p>Creator</p>
                                    <el-popover
                                            placement="top-start"
                                            width="300"
                                            :title="sheetData?.author.username"
                                            trigger="hover"
                                    >
                                        <template #reference>
                                            <el-button>{{ sheetData?.author.username }}</el-button>
                                        </template>
                                        <div class="creator_profile">
                                            <div class="creator_avatar_description">
                                                <el-avatar size="50"
                                                           :src="env.backEnd + sheetData?.author.avatar.slice(1)"
                                                           style="float: left"/>
                                                <p>{{ sheetData?.author.introduction }}</p>
                                            </div>
                                            <div class="creator_details">
                                                <p style="margin-bottom: 10px">
                                                    followers <span>0</span> fans <span>32k</span> rank <span>19k</span>
                                                </p>
                                                <el-button type="primary" size="small">follow</el-button>
                                                <el-button size="small">message</el-button>
                                            </div>
                                        </div>
                                    </el-popover>
                                </div>
                                <div class="sheet-type">
                                    <p>last replied time</p>
                                    <p style="padding-right: 15px">{{ sheetData?.update_time }}</p>
                                </div>
                            </el-card>
                        </div>
                    </div>
            </el-tabs>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from "@/api";
import env from "@/utils/env";
import { ElMessage } from 'element-plus'


function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    //把时间格式定为2位不够补0

    return `${year}-${month}-${day} ${hour}:${minute}`;
}

const props = defineProps<{
    id: string
}>()

const sheetData = ref<{
  title: string;
  content: string;
  id: number;
  create_time: string;
  update_time: string;
  author: {
    id: number;
    username: string;
    avatar: string;
    introduction: string;
  };
  type: string;
  count: number;
  members: {
    id: number;
    username: string;
    avatar: string;
    introduction: string;
  }[];
  memberCnt: number;

}>({
  title: '',
  content: '',
  id: 0,
  create_time: '',
  update_time: '',
  author: {
    id: 0,
    username: '',
    avatar: '',
    introduction: ''
  },
  type: '',
  count: 0,
  members: [],
  memberCnt: 0
});

// const comments = ref< {
//   id: number,
//   comment: string,
//   author: {
//     id: number,
//     username: string,
//     avatar: string,
//     introduction: string,
//   },
// }>({
//   id: 0,
//   comment: '',
//   author: {
//     id: 0,
//     username: '',
//     avatar: '',
//     introduction: '',
//   }
// });
const comments = ref([]);

const fetchComments = async () => {
    try {
        const res = await api.getGroupDetail({page: currentPage.value.toString() ,usergroup_id: props.id});
        sheetData.value = res.results.data;
        comments.value = res.results.comments;
        console.log('---comments:', comments.value);
        console.log('-sheetData:', sheetData.value);
        totalComments.value = res.results.data.count;
        sheetData.value.create_time = formatDate(sheetData.value.create_time);
        sheetData.value.update_time = formatDate(sheetData.value.update_time);
    } catch (error) {
        console.error("Failed to fetch sheet detail:", error);
    }

}

onMounted(fetchComments);


const totalComments = ref(0);
const currentPage = ref(1);
const pageSize = 20;

const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    fetchComments()
};

const userComment = ref('')

const submitComment = () => {
    if (userComment.value === '') {
        ElMessage.error('评论内容不能为空')
    } else {
        api.uploadCommentsInGroup({
            usergroup: props.id,
            comment: userComment.value
        }).then(() => {
            ElMessage.success('评论成功')
            userComment.value = ''
            currentPage.value = 1
            fetchComments()
        })
    }
}
</script>

<style scoped>
.group-detail-header {
    background-color: #f5f7fa;
    height: 100px;
    margin: 70px 20px 20px;
    border-radius: 20px;
    box-shadow: #595959 0 0 2px;
}

.gd-header-container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
}

.breadcrumb {
    margin-top: 20px;
    margin-bottom: 15px;
}

h1 {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin-bottom: .5em;
    font-family: inherit;
    font-weight: bold;
    line-height: 1.2;
    color: inherit;
    font-size: 1.75em;
}


.sheet-detail-container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
}

.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

.sheet-description {
    display: flex;
    width: 100%;
    height: 100%;
}

.description-left {
    width: 70%;
    padding: 10px;
    margin-top: -10px;
}

.description-right {
    width: 30%;
}

h2 {
    font-size: 20px;
    margin-bottom: 2em;
    font-weight: bold;
    line-height: 1.2;
}

.detail-card {
    padding: 10px 10px 0;
    display: flex;
    flex-direction: column;
}

.sheet-id, .sheet-creator, .sheet-type {
    margin: 10px 0 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.creator_avatar_description {
    display: flex;
    flex-wrap: wrap;
}

.creator_avatar_description p {
    margin-left: 10px;
    flex: 1;
}

.creator_details {
    clear: both;
    margin-top: 10px;
}


.comment {
    display: flex;
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ebeef5;
    border-radius: 5px;
}

.avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
}

.comment-details {
    display: flex;
    flex-direction: column;
}

.commenter-name {
    font-weight: bold;
}

.comment-content {
    margin-top: 5px;
}

.el-pagination {
    margin-top: 20px;
}
</style>


