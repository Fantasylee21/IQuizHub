<script setup lang="ts">
import {computed, ref} from 'vue'
import AiAssistant from './AiAssistant.vue'
import api from "@/api";
import CommentList from "@/components/GlobalComponents/Questions/CommentList.vue";

interface QuestionData {
    type: string
    content: string
    id: number
    choices: string[]
    tags: any[]
    title: string
    ans: string
}

const props = defineProps<{
    question: QuestionData,
}>()

const selectedChoice = ref<string | null>(null);
const choiceResults = ref<Record<string, 'correct' | 'incorrect'>>({});
const is_read = ref(false);

async function selectChoice(choice: string) {
    if (is_read.value) return;

    try {
        const res = await api.checkQuestion({
            'question_id': props.question.id,
            'ans': choice
        });
        is_read.value = true;

        selectedChoice.value = choice;
        if (res.message) {
            // 答案正确, 渲染成绿色并出现对钩
            choiceResults.value[choice] = 'correct';
        } else {
            // 答案错误, 渲染成红色并出现叉
            choiceResults.value[choice] = 'incorrect';
        }
    } catch (error) {
        console.error(error);
    }
}

const questionContent = ref<HTMLElement | null>(null);

const message = computed(() => {
    return questionContent.value?.textContent?.trim() || '';
});
</script>

<template>
    <div class="single-question-container">
        <div class="single-question-left" ref="questionContent">
            <el-tag type="info" style="margin: 15px 5px;">Single Choice Question</el-tag>
            <el-tag v-for="tag in question.tags" :key="tag.id">{{ tag.name }}</el-tag>
            <h3>{{ question.title }}</h3>
            <div class="question-header">
                <p>{{ question.id }}.</p>
                <div v-html="question.content"></div>
            </div>
            <ul class="choices">
                <li
                        v-for="(choice, index) in question.choices"
                        :key="index"
                        :class="{
                        selected: selectedChoice === String.fromCharCode(65 + index),
                        correct: choiceResults[String.fromCharCode(65 + index)] === 'correct',
                        incorrect: choiceResults[String.fromCharCode(65 + index)] === 'incorrect'
                    }"
                        @click="!is_read && selectChoice(String.fromCharCode(65 + index))"
                >
                    <div class="choice-content">
                        <div class="choice-label">{{ String.fromCharCode(65 + index) }}.</div>
                        <div class="choice-text" v-html="choice"></div>
                    </div>
                </li>
            </ul>
            <el-divider></el-divider>
            <div class="comment-list" v-show="is_read" style="margin-top: 30px">
                <CommentList :id="props.question.id"/>
            </div>
        </div>
        <div class="single-question-right">
            <el-collapse v-if="is_read">
                <el-collapse-item title="Answer">
                    <div v-html="question.ans"></div>
                </el-collapse-item>
            </el-collapse>
            <AiAssistant v-show="is_read" :message="message"></AiAssistant>
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

ul.choices li.selected.correct {
    background-color: #e1f3d8;
    border-color: #67c23a;
    color: #67c23a;
}

ul.choices li.selected.correct .choice-label::after {
    content: '✔';
    color: #67c23a;
    font-size: 18px;
    margin-left: 5px;
}

ul.choices li.selected.incorrect {
    background-color: #fde2e2;
    border-color: #f56c6c;
    color: #f56c6c;
}

ul.choices li.selected.incorrect .choice-label::after {
    content: '✘';
    color: #f56c6c;
    font-size: 18px;
    margin-left: 5px;
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
</style>
