<template>
    <p style="font-size: 20px; font-weight: bold; margin: 10px">Record</p>
    <el-scrollbar
            height="400px"
    >
        <ul class="custom-scrollbar"
            v-infinite-scroll="load"
            :infinite-scroll-disabled="disabled"
            :infinite-scroll-distance="history.length"
        >
            <li v-for="i in count" :key="i" class="scrollbar-demo-item">
                {{ getTime(i) }}:
                {{ getContent(i) }}
            </li>
        </ul>
        <p v-if="loading" class="loading">Loading...</p>
        <p v-if="noMore" class="noMore">No more</p>
    </el-scrollbar>
</template>

<script setup lang="ts">
import {computed, onBeforeMount, onMounted, ref} from 'vue'
import {useProfileStore} from '@/stores/profile'
import api from '@/api'

const count = ref(10)
const loading = ref(false)
const noMore = computed(() => count.value >= history.value.length)
const disabled = computed(() => loading.value || noMore.value)

interface History {
    id: number;
    create_time: string;
    correct: boolean;
    question: string;
}

const history = ref<any[]>([]);

const props = defineProps({
    historys: Array
})

const profile = useProfileStore()

onBeforeMount(() => {
    if (props.historys) {
        history.value = props.historys
    } else {
        api.getHistory({id: profile.id}).then((res) => {
            history.value = res
        })
    }
    console.log(history.value.length)
})


function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function getContent(i: number) {
    if (history.value[i] && history.value[i].correct != undefined && history.value[i].correct === true) {
        return 'You did ' + history.value[i].question + ' right!!!'
    } else {
        return 'You did ' + history.value[i]?.question + ' wrong! , better luck next time!'
    }
}

const getTime = (i: number) => {
    if (history.value[i]) {
        return formatDate(history.value[i].create_time);
    } else {
        return 'Invalid date';
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
