<template>
    <div class="ai-assistant" v-loading="loading">
        <el-button
                type="primary"
                @click="fetchAiAnswer"
                :loading="loading"
                class="load-button"
                :disabled="isClicked"
        >
            {{ loading ? '正在加载...' : '向AI提问' }}
        </el-button>
        <el-card class="box-card" v-if="loading">
        </el-card>
        <el-card class="box-card custom-scrollbar" v-else-if="data">
            <div class="text">
                <p v-html="renderedData"></p>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import {ref} from 'vue';

const loading = ref(false);
const data = ref('');
const renderedData = ref('');
let interval = null;
const isClicked = ref(false);

const fetchAiAnswer = () => {
    isClicked.value = true;
    loading.value = true;
    data.value = '';
    renderedData.value = '';

    // 模拟请求
    setTimeout(() => {
        // 假设从后端返回的数据
        data.value = '这是从AI返回的数据，逐字渲染。\n\n\n划线部分的句子成分为：D. 定语。\n' +
                '\n' +
                '在这个句子“I shall answer your question after class”中，“after class”是介词短语作状语，用于修饰动词“shall answer”，但考虑到问题的选项设置，我们需要从更宽泛的“句子成分”角度来分析。若从“your question”这个名词短语内部来看，“after class”实际上是对“question”的进一步描述，即“课后的问题”，因此它在这里起到了定语的作用，尽管它并不直接紧挨着“question”。但在这个选择题的语境下，我们可以将其理解为对“question”的修饰，即定语成分。所以正确答案是D。注意，这种分析方式可能略显灵活，因为“after class”通常被视为状语，但从“your question”这个名词短语的角度来看，它确实起到了定语的作用。不过，根据选项的严格性和问题的设定，D选项“定语”是最接近的。';
        renderData();
        loading.value = false;
    }, 5000);
};

const renderData = () => {
    let index = 0;
    interval = setInterval(() => {
        if (index < data.value.length) {
            renderedData.value += data.value[index];
            index++;
        } else {
            clearInterval(interval);
        }
    }, 20); // 调整时间间隔以控制渲染速度
};
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

.box-card {
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