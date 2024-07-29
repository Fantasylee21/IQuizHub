<template>
    <div class="ai-assistant" v-loading="loading">
        <el-button
                type="primary"
                @click="fetchAiAnswer"
                :loading="loading"
                class="load-button"
                :disabled="isClicked"
        >
            {{ loading ? 'Loading...' : 'Ask Ai Assistant' }}
        </el-button>
        <el-card class="creator_card" v-if="loading"></el-card>
        <el-card class="creator_card custom-scrollbar" v-else-if="data">
            <div class="text">
                <p v-html="renderedData"></p>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import {ref} from 'vue'
import api from '@/api'

const props = defineProps({
    message: {
        type: String,
        required: true
    }
})

const loading = ref(false)
const data = ref('')
const renderedData = ref('')
let interval = null
const isClicked = ref(false)

const fetchAiAnswer = async (content) => {
    isClicked.value = true;
    loading.value = true;
    data.value = '';
    renderedData.value = '';

    try {
        data.value = await api.ask({content: props.message}); // 使用传递的content
        renderData();
    } catch (error) {
        console.error('Error fetching AI answer:', error);
    } finally {
        loading.value = false;
    }
};

const renderData = () => {
    let index = 0
    interval = setInterval(() => {
        if (index < data.value.length) {
            renderedData.value += data.value[index]
            index++
        } else {
            clearInterval(interval)
        }
    }, 20) // 调整时间间隔以控制渲染速度
}
</script>

<style scoped>
.ai-assistant {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
}

.load-button {
    margin-bottom: 20px;
}

.creator_card {
    width: 100%;
    max-width: 600px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    text-align: left;
    max-height: 400px;
    overflow-y: auto;
    transition: all 0.3s ease;
    padding: 20px;
}

.scrollbar-wrapper {
    max-height: 100%;
}

.text {
    white-space: pre-wrap; /* 保持换行符 */
    font-size: 16px;
    color: #333;
    line-height: 1.5;
    word-break: break-word; /* 确保单词在容器边界换行 */
}

p {
    text-align: justify;
    margin: 0;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 8px; /* 设置滚动条的宽度 */
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #c1c1c1; /* 滚动条的滑块颜色 */
    border-radius: 10px; /* 滑块的圆角 */
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #a8a8a8; /* 滑块在鼠标悬停时的颜色 */
}

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: #f1f1f1; /* 滚动条的轨道颜色 */
    border-radius: 10px; /* 轨道的圆角 */
}
</style>
