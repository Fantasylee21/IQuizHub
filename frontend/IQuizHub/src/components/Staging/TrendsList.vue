<template>
    <el-scrollbar
            height="400px"
    >
        <ul class="custom-scrollbar"
            v-infinite-scroll="load"
            :infinite-scroll-disabled="disabled"
            :infinite-scroll-distance="profile.historys.length"
        >
            <li v-for="i in count" :key="i" class="scrollbar-demo-item">
                {{ formatDate(history[i].create_time) }}
                {{ getContent(i) }}
            </li>
        </ul>
        <p v-if="loading" class="loading">Loading...</p>
        <p v-if="noMore" class="noMore">No more</p>
    </el-scrollbar>
</template>

<script setup lang="ts">
import {computed, onBeforeMount, ref} from 'vue';
import {useProfileStore} from '@/stores/profile'

const count = ref(10)
const loading = ref(false)
const noMore = computed(() => count.value >= 20)
const disabled = computed(() => loading.value || noMore.value)
const profile = useProfileStore()
const history = profile.historys;

function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function getContent(i: number) {
    if (history[i].correct === true) {
        return '你做对了题目 ' + history[i].question
    } else {
        return '你做错了题目 ' + history[i].question + '，看仔细了！！！'
    }
}


const load = () => {
    loading.value = true
    setTimeout(() => {
        count.value += 5
        loading.value = false
    }, 1000)
}
</script>

<style scoped>
.custom-scrollbar {
    list-style: none;
    padding: 0;
    margin: 0;
}

.scrollbar-demo-item {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
    margin: 10px;
    text-align: center;
    border-radius: 4px;
    background: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
}

.loading, .noMore {
    width: 100%;
    height: 50px;
    text-align: center;
    align-items: center;
    line-height: 50px;
}
</style>
