<template>
    <el-scrollbar
            height="400px"
    >
        <ul class="custom-scrollbar"
            v-infinite-scroll="load"
            :infinite-scroll-disabled="disabled"
            :infinite-scroll-distance="20"
        >
            <li v-for="i in count" :key="i" class="scrollbar-demo-item">{{ i }}</li>
        </ul>
        <p v-if="loading" class="loading">Loading...</p>
        <p v-if="noMore" class="noMore">No more</p>
    </el-scrollbar>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue';

const count = ref(10)
const loading = ref(false)
const noMore = computed(() => count.value >= 20)
const disabled = computed(() => loading.value || noMore.value)
const load = () => {
    loading.value = true
    setTimeout(() => {
        count.value += 2
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
