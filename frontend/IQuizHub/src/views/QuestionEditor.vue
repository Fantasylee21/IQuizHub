<template>
    <div class="editor-container">
        <div class="editor-left">
            <el-tiptap v-model:content="content" :extensions="extensions" ref="editorRef"/>
        </div>
        <div class="editor-right">
            <div class="type">
            </div>
            <el-button type="primary" @click="insertText(' (  ) ')"
                       :disabled="type !== 'single_choice' && type !== 'multiple_choice'"
            >
                Add selection box
            </el-button>
            <el-button type="primary" @click="insertText(' ____ ')" :disabled="type !== 'short_answer'">
                Add blank line
            </el-button>
            <el-button
                    type="primary"
                    @click="addOption"
                    :disabled="optionNum >= 4 || type !== 'multiple_choice' && type !== 'single_choice'"
                    style="margin-top: 20px"
            >
                Add options
            </el-button>
            <div class="option-input">
                <div class="option-list">
                    <div class="options"
                         v-for="(option, index) in options"
                         :key="index" style="display: flex; align-items: center">
                        <p style="margin-right: 10px !important">{{ String.fromCharCode(65 + index) }}</p>
                        <el-input
                                v-model="option.text"
                                placeholder="Please input option"
                                class="option-item"
                        >
                            <template #append>
                                <el-button type="danger" @click="removeOption(index)">Delete</el-button>
                            </template>
                        </el-input>
                    </div>
                </div>
            </div>
            <div class="type">
                <strong style="margin-top: 15px; align-items: center">type</strong>
                <el-select v-model="type" placeholder="Please select type" style="margin-top: 10px; margin-left: 20px">
                    <el-option label="single_choice" value="single_choice"/>
                    <el-option label="True/False" value="True/False"/>
                </el-select>
            </div>
            <div class="title" style="display: flex">
                <strong style="margin-top:10px; align-items: center">title</strong>
                <el-input
                        v-model="inputTitle"
                        style="width: 240px; ; margin-left: 35px"
                        placeholder="Please input title"
                />
            </div>
            <div class="answer" style="display: flex">
                <strong style="margin-top: 15px; align-items: center">answer</strong>
                <el-input
                        v-model="inputAnswer"
                        style="width: 240px; margin-top: 10px; margin-left: 10px"
                        placeholder="Please input answer"
                />
            </div>
            <el-button type="primary" style="margin-top: 10px" @click="upload">Upload</el-button>
            <div class="ocr">
                <EditorOCR/>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import EditorOCR from '@/components/Editor/EditorOCR.vue';
import {ref, onMounted, computed, defineProps} from 'vue';
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
import {ElMessage} from 'element-plus';
import api from '@/api';

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

const content = ref('');

const editorRef = ref<InstanceType<typeof import('element-tiptap-vue3-fixed').ElTiptap> | null>(null);

onMounted(() => {
    if (editorRef.value) {
        const editor = editorRef.value.editor;
    }
});

const insertText = (text: string) => {
    if (editorRef.value) {
        const editor = editorRef.value.editor;
        editor.chain().focus().insertContent(text).run();
    }
};

const options = ref<{ text: string }[]>([]);
const optionNum = computed(() => options.value.length);
const removeOption = (index: number) => {
    options.value.splice(index, 1);
};
const addOption = () => {
    options.value.push({text: ''});
};

const inputAnswer = ref('');
const inputTitle = ref('');

const props = defineProps<{ type: string }>();

const type = ref('');

const upload = async () => {
    // todo 校验逻辑
    console.log(options.value[0].text)
    const res = await api.uploadQuestion({
        type: type.value,
        content: content.value,
        answer: inputAnswer.value,
        title: inputTitle.value,
        choices: options.value.map(option => option.text)
    });
    if (res) {
        ElMessage({
            message: '上传成功',
            type: 'success',
            duration: 3000,
        });
    } else {
        ElMessage({
            message: '上传失败',
            type: 'error',
            duration: 3000,
        });
    }
};
</script>

<style scoped>
.editor-container {
    margin: 70px auto 0;
    width: 1200px;
    display: flex;
}

.editor-left {
    width: 70%;
}

.editor-right {
    width: 30%;
    margin-left: 20px;
}

.type {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.type strong {
    margin-right: 10px;
}

.option-input {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}

.add-option {
    text-align: right;
}

.option-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.option-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.option-item .el-input {
    flex: 1;
}

.ocr {
    margin-top: 50px;

}
</style>