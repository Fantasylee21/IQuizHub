<template>
    <div class="editor-container">
        <div class="editor-left">
            <el-tiptap v-model:content="content" :extensions="extensions" ref="editorRef"/>
        </div>
        <div class="editor-right">
            <el-button type="primary" @click="insertText(' (  ) ')">插入选择框</el-button>
            <el-button type="primary" @click="insertText(' ____ ')">插入填空线</el-button>
            <el-button type="primary" @click="addOption">添加选项</el-button>
            <div class="option-input">
                <div class="option-list">
                    <el-input v-for="(option, index) in options" :key="index" v-model="option.text"
                              placeholder="请输入选项内容" class="option-item">
                        <template #append>
                            <el-button type="danger" @click="removeOption(index)">删除</el-button>
                        </template>
                    </el-input>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
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

const content = ref(`
  <h1>Heading</h1>
  <p>This Editor is awesome!</p>
`);

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

const addOption = () => {
    options.value.push({text: ''});
};

const removeOption = (index: number) => {
    options.value.splice(index, 1);
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
</style>