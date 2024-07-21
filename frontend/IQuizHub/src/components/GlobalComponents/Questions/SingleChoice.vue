<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import AiAssistant from './AiAssistant.vue'

interface QuestionData {
    pattern: string
    description: string
    id: number
    choices: string[]
    storeId: number
    bigQuestionId: number
}

const props = defineProps<{ question: QuestionData }>()
const selectedChoice = ref<string | null>(null)

const selectChoice = (choice: string) => {
    selectedChoice.value = choice
}

const questionContent = ref<HTMLElement | null>(null);

const message = computed(() => {
    return questionContent.value?.textContent?.trim() || '';
});
</script>

<template>
    <div class="single-question-container">
        <div class="single-question-left" ref="questionContent">
            <h3>单选题</h3>
            <div class="question-header">
                <p>{{ question.id }}.</p>
                <div v-html="question.description"></div>
            </div>
            <ul class="choices">
                <li
                        v-for="(choice, index) in question.choices"
                        :key="index"
                        :class="{ selected: selectedChoice === choice }"
                        @click="selectChoice(choice)"
                >
                    <div class="choice-content">
                        <div class="choice-label">{{ String.fromCharCode(65 + index) }}.</div>
                        <div class="choice-text" v-html="choice"></div>
                    </div>
                </li>
            </ul>
        </div>
        <div class="single-question-right">
            <AiAssistant :message="message"></AiAssistant>
        </div>
    </div>
</template>

<style scoped>
.single-question-container {
    display: flex;
}

.single-question-left {
    width: 70%;
    padding: 20px;
}

.single-question-right {
    width: 30%;
    padding: 20px;
}

h3 {
    margin-bottom: 20px;
}

.question-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.question-header p {
    display: inline;
    margin-right: 10px;
}

ul.choices {
    list-style-type: none;
    padding: 0;
}

ul.choices li {
    margin: 10px 0;
    height: 30px;
    padding: 10px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
}

ul.choices li:hover {
    background-color: #f5f5f5;
}

ul.choices li.selected {
    background-color: #fcebea;
    border-color: #f56c6c;
    color: #f56c6c;
}

ul.choices li.selected .choice-label {
    color: #f56c6c;
}

.choice-content {
    display: flex;
    align-items: center;
    width: 100%;
}

.choice-label {
    margin-right: 10px;
    font-weight: bold;
}

.choice-text {
    flex-grow: 1;
}

ul.choices li.selected .choice-label::after {
    content: '✔';
    color: #f56c6c;
    font-size: 18px;
    margin-left: 5px;
}
</style>
