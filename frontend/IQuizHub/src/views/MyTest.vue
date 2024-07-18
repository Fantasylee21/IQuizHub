<template>
    <div style="width: 1200px; margin: 0 auto; padding-top: 25px;">
        <h2>单选题展示</h2>
        <SingleChoiceQuestion :question="question"/>
        <SingleChoiceQuestion :question="question"/>
        <SingleChoiceQuestion :question="question"/>

    </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import SingleChoiceQuestion from '@/components/GlobalComponents/Questions/SingleChoice.vue';

const question = ref({
    pattern: "single_choice",
    description: "<p>I <span style='text-decoration: underline;'>shall answer</span> your question after class. 划线部分的句子成分为:</p>",
    id: 1,
    choices: [
        "<p>主语</p>",
        "<p>宾语</p>",
        "<p>谓语</p>",
        "<p>定语</p>"
    ],
    storeId: 568252,
    bigQuestionId: 568252
});
</script>

<style scoped>
h2 {
    margin-bottom: 20px;
}
</style>
