<template>
    <div class="question-detail-container">
        <SingleChoice v-if="question.type === 'single_choice'"
                      :question="question"
                      :is_read="is_read"
        />
    </div>

</template>

<script setup lang="ts">

import SingleChoice from "@/components/GlobalComponents/Questions/SingleChoice.vue";


interface QuestionData {
    type: string
    content: string
    id: number
    choices: string[]
    tags: string[]
    title: string
    answer: string
}

const props = defineProps<{
    question: QuestionData,
    is_read: boolean
}>()
</script>

<style scoped>
.question-detail-container {
    width: 1200px;
    margin: 50px auto 0;
}
</style>