<template>
    <div class="question-detail-container">
        <SingleChoice v-if="question?.type === 'single_choice'" :question="question"/>
        <TrueFalse v-else-if="question?.type === 'True/False'" :question="question"/>
    </div>
</template>

<script setup lang="ts">
import SingleChoice from "@/components/GlobalComponents/Questions/SingleChoice.vue";
import TrueFalse from "@/components/GlobalComponents/Questions/TrueFalse.vue";
import {onBeforeMount, ref} from "vue";
import api from "@/api";

interface QuestionData {
    type: string;
    content: string;
    id: number;
    choices: string[];
    tags: string[];
    title: string;
    answer: string;
}

const props = defineProps<{
    id: string;
}>();

const question = ref<QuestionData>();
const isLoading = ref(true);

onBeforeMount(async () => {
    try {
        question.value = await api.getQuestionDetail(props.id);
    } catch (error) {
        console.error("Failed to fetch question detail:", error);
    }
});
</script>

<style scoped>
.question-detail-container {
    width: 1200px;
    margin: 50px auto 0;
}

.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 18px;
    color: #888;
}
</style>