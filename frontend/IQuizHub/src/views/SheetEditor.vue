<template>
    <div class="sheet-editor-header">
        <div class="se-header-container">
            <el-breadcrumb separator="/" class="breadcrumb">
                <el-breadcrumb-item :to="{ path: '/staging' }">staging</el-breadcrumb-item>
                <el-breadcrumb-item>
                    <a href="#">question-bank</a>
                </el-breadcrumb-item>
            </el-breadcrumb>
            <h1>题单编辑</h1>
        </div>
        <div class="content-container">
            <el-upload
                    class="avatar-uploader"
                    :action="apiUrl"
                    :show-file-list="false"
                    method="put"
                    :headers="header"
                    name="avatar"
                    :on-success="handleAvatarSuccess"
            >
                <el-avatar :size="100" :src="form.avatar" class="sheet-avatar"></el-avatar>
            </el-upload>
            <el-form :model="form" label-width="auto" style="max-width: 600px">
                <el-form-item label="题单名">
                    <el-input v-model="form.title"></el-input>
                </el-form-item>
                <el-form-item label="题单描述" style="width: 1000px">
                    <el-tiptap v-model:content="form.content" :extensions="extensions"/>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">Submit</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>

</template>


<script setup lang="ts">
import {computed, onBeforeMount, reactive} from 'vue'
import env from "@/utils/env";
import api from "@/api";

const apiUrl = computed(() => {
    return env.backEnd + `api/question/questiongroup/put/${props.id}/`
})

const header = computed(() => {
    return {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
})

const handleAvatarSuccess = async (res: any) => {
    try {
        const response = await api.getSheetDetail(props.id)
        form.avatar = response.avatar
    } catch (error) {
        console.error("Failed to fetch sheet detail:", error);
    }
}

const props = defineProps<{
    id: string
}>()

onBeforeMount(async () => {
    try {
        const response = await api.getSheetDetail(props.id)
        form.title = response.title
        form.content = response.content
        form.avatar = response.avatar
    } catch (error) {
        console.error("Failed to fetch sheet detail:", error);
    }
})

// do not use same name with ref
const form = reactive({
    title: '',
    content: '',
    avatar: ''
})

const onSubmit = async () => {
    const response = await api.updateSheetDetail({
        title: form.title,
        content: form.content
    }, props.id)
    if (response) {
        ElMessage({
            message: '更新成功',
            type: 'success',
            duration: 3000,
        })
    } else {
        ElMessage.error('更新失败')
    }
}

import {
    // necessary extensions
    Doc,
    Text,
    Paragraph,
    //________________________
    Bold,
    Underline,
    Italic,
    Strike,
    BulletList,
    OrderedList,
    Link,
    Image,
    FontSize,
    FontFamily,
} from 'element-tiptap-vue3-fixed';
import {ElMessage} from "element-plus";

const extensions = [
    Doc,
    Text,
    Paragraph,
    Bold.configure({bubble: true}),
    Underline.configure({bubble: true, menubar: false}),
    Italic,
    Strike,
    BulletList,
    OrderedList,
    Link,
    Image,
    FontSize.configure({bubble: true}),
    FontFamily.configure({bubble: true}),
];

</script>


<style scoped>
.sheet-editor-header {
    background-color: #f5f7fa;
    height: 100px;
    margin: 70px 20px 20px;
    border-radius: 20px;
    box-shadow: #595959 0 0 2px;
}

.se-header-container {
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

.content-container {
    margin: 40px auto 0;
    width: 1200px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.sheet-avatar {
    margin-bottom: 20px;
}
</style>