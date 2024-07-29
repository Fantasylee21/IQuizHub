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
            <el-tabs v-model="activeName" class="demo-tabs" style="margin-bottom: 20px; width: 100%">
                <el-tab-pane label="Basic Info" name="first">
                    <el-form :model="form" label-width="auto">
                        <el-form-item label="Name" style="max-width: 600px">
                            <el-input v-model="form.title"></el-input>
                        </el-form-item>
                        <el-form-item label="Description" style="width: 1000px">
                            <el-tiptap v-model:content="form.content" :extensions="extensions"/>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="onSubmit">Submit</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
                <el-tab-pane label="List" name="second" style="width: 100%">
                    <div class="upload" style="display: flex;">
                        <el-input v-model="questionId" style="width: 200px; margin-right: 20px"
                                  placeholder="id"></el-input>
                        <el-button type="primary" @click="handleUploadQuestion">Add</el-button>
                    </div>
                    <SEList :table-data="tableData"></SEList>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>

</template>


<script setup lang="ts">
import {computed, onBeforeMount, reactive, ref} from 'vue'
import env from "@/utils/env";
import api from "@/api";

const activeName = ref('first')
const tableData = ref([])
const questionId = ref('')
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
        ElMessage.success('upload successfully')
    } catch (error) {
        console.error("Failed to fetch sheet detail:", error);
    }
}

const props = defineProps<{
    id: string
}>()


const handleUploadQuestion = async () => {
    try {
        await api.addQuestionToGroup(questionId.value, props.id)
        const response = await api.getSheetDetail(props.id)
        tableData.value = response.questions
        ElMessage.success('Successfully added')
    } catch (e) {
        ElMessage.error('Failed to add')
    }

}

onBeforeMount(async () => {
    try {
        const response = await api.getSheetDetail(props.id)
        form.title = response.title
        form.content = response.content
        form.avatar = response.avatar
        tableData.value = response.questions
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
            message: 'Successfully updated',
            type: 'success',
            duration: 3000,
        })
    } else {
        ElMessage.error('Failed to update')
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
import SEList from "@/components/SheetEditor/SEList.vue";

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

.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}
</style>