<template>
    <QuestionDetail :is_read="true" :question="question"/>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import QuestionDetail from "@/views/QuestionDetail.vue";

const question = ref({
    type: "single_choice",
    content: "<p>I <span style='text-decoration: underline;'>shall answer</span> your question after class. 划线部分的句子成分为:</p>",
    id: 6,
    choices: [
        "<p>主语</p>",
        "<p>宾语</p>",
        "<p>谓语</p>",
        "<p>定语</p>"
    ],
    tags: ['标签', '又一个标签'],
    title: '这是标题',
});
</script>

<style scoped>

</style>