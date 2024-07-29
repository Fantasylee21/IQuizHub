<template>
    <div class="comment-header" style="display: flex; justify-content: space-between; align-items: center">
        <h2 style="margin-bottom: 20px; font-size: 20px; font-weight: bold">评论列表</h2>
        <el-popover placement="right" :width="400" trigger="click">
            <template #reference>
                <el-button style="margin-right: 16px">Leave a comment</el-button>
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
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import api from "@/api";
import {ElMessage} from "element-plus";

const comments = ref([]);
const totalComments = ref(0);
const currentPage = ref(1);
const pageSize = 20;

const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    fetchComments()
};

const userComment = ref('')

const props = defineProps({
    id: Number
})

const fetchComments = async () => {
    try {
        const response = await api.getComments({page: currentPage.value, id: props.id});
        if (response) {
            comments.value = response.results;
            totalComments.value = response.count;
        }
    } catch (error) {
        console.error('Error fetching comments:', error);
    }
};

onMounted(fetchComments);

const submitComment = () => {
    if (userComment.value === '') {
        ElMessage.error('Comment content cannot be empty')
    } else {
        api.postComment({
            question: props.id,
            comment: userComment.value
        }).then(() => {
            ElMessage.success('Comment successfully issued')
            userComment.value = ''
            currentPage.value = 1
            fetchComments()
        })
    }
}
</script>

<style scoped>
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