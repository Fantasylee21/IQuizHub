<template>
    <div class="single-question-container">
        <div class="single-question-left" ref="questionContent">
            <el-tag type="info" style="margin: 15px 5px;">True or False</el-tag>
            <el-tag v-for="tag in question.tags" :key="tag.id">{{ tag.id }}</el-tag>
            <h3>{{ question.title }}</h3>
            <div class="question-header">
                <p>{{ question.id }}.</p>
                <div v-html="question.content"></div>
            </div>

            <div class="question-choices">
                <el-radio-group v-model="selectedChoice"
                                @change="selectChoice(selectedChoice)"
                                :disabled="is_read"
                >
                    <el-radio-button value="0">
                        Wrong!
                    </el-radio-button>
                    <el-radio-button value="1">
                        Right!
                    </el-radio-button>
                </el-radio-group>
                <el-tag v-show="is_read && isCorrect === true" type="success"
                        style="margin-left: 10px; margin-top: 2px">Right!
                </el-tag>
                <el-tag v-show="is_read && isCorrect === false" type="danger"
                        style="margin-left: 10px; margin-top: 2px">Wrong!
                </el-tag>
            </div>
            <el-divider></el-divider>
            <div class="comment-list" v-show="is_read" style="margin-top: 30px">
                <CommentList :id="props.question.id"/>
            </div>
        </div>
        <div class="single-question-right">
            <el-collapse v-if="is_read">
                <el-collapse-item title="Answer">
                    <div v-if="question.ans === '1'">Right</div>
                    <div v-else-if="question.ans === '0'">Wrong</div>
                    <div v-else v-html="question.ans"></div>
                </el-collapse-item>
            </el-collapse>
            <AiAssistant v-show="is_read" :message="message"></AiAssistant>
        </div>
    </div>
</template>

<script setup lang="ts">
import {computed, defineProps, ref} from 'vue'
import AiAssistant from './AiAssistant.vue'
import CommentList from "@/components/GlobalComponents/Questions/CommentList.vue";
import api from "@/api";

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

const is_read = ref(false);
const selectedChoice = ref<any>(null);
const isCorrect = ref<null | boolean>(null);

async function selectChoice(choice: string) {
    try {
        const res = await api.checkQuestion({
            'question_id': props.question.id,
            'ans': choice
        });
        is_read.value = true;

        if (res.message) {
            // 答案正确
            isCorrect.value = true;
        } else {
            // 答案错误
            isCorrect.value = false;
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

.question-choices {
    margin-top: 20px;
    display: flex;
}

</style>