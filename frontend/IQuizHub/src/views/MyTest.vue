<template>
    <el-tiptap v-model:content="content" :extensions="extensions"/>
</template>

<script setup>
import {ref} from 'vue';
import {
    // necessary extensions
    Doc,
    Text,
    Paragraph,
    //________________________
    Heading,
    Bold,
    Underline,
    Italic,
    Strike,
    BulletList,
    OrderedList,
} from 'element-tiptap-vue3-fixed';

// editor extensions
// they will be added to menubar and bubble menu by the order you declare.
const extensions = [
    Doc,
    Text,
    Paragraph,
    Heading.configure({level: 5}),
    Bold.configure({bubble: true}), // render command-button in bubble menu.
    Underline.configure({bubble: true, menubar: false}), // render command-button in bubble menu but not in menubar.
    Italic,
    Strike,
    BulletList,
    OrderedList,
];

// editor's content
const content = ref(`
  <h1>Heading</h1>
  <p>This Editor is awesome!</p>
`);
</script>