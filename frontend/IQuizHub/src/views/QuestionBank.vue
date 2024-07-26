<script setup lang="ts">

import QBHeader from '@/components/QuestionBank/QBHeader.vue'
import QBNav from '@/components/QuestionBank/QBNav.vue'
import QBList from '@/components/QuestionBank/QBList.vue'

import api from '@/api'
import { onMounted, ref } from 'vue'

const tableData = ref([]);
const total = ref(0);
const getAllQuestion = async (pageNumber: number) => {
    try {
        const res = await api.getAllQuestions({pageNumber}); // Use pageNumber in the request
        tableData.value = res.results;
        total.value = res.count;
        tableData.value.forEach((item) => {
            item.create_time = formatDate(item.create_time);
        });
    } catch (e) {
        console.error('Error fetching questions:', e);
    }
}

const currentPage = ref(1);

const pageChange = (pageNew: number) => {
    loadPage(pageNew)
    currentPage.value = pageNew;
};

const loadPage = (currentPage: number) => {
    console.log('----->isSearching:', isSearching.value, currentPage)
    if (isSearching.value.value == true) {
        search(currentPage, tags.value, query.value);
    } else {
        getAllQuestion(currentPage);
    }
}

onMounted(() => {
    loadPage(1);
})

const search = async (pageNumber: number, Tags: string[], keyword: string) => {
    try {
        const res = await api.search({
            'pageNumber': pageNumber,
            'Tags': Tags,
            'keyword': keyword
        });
        tableData.value = res.results;
        total.value = res.count;
        console.log('search result:', tableData.value)
        tableData.value.forEach((item) => {
            item.create_time = formatDate(item.create_time);
        });
    } catch (e) {
        console.error('Error searching questions:', e);
    }
}

const query = ref('');
const tags = ref<string[]>([]);
const isSearching = ref(false);

const onUpdateSearchStatus = (isSearch : boolean) => {
    isSearching.value = isSearch;
    console.log('isSearching:', isSearching.value, currentPage.value);
    loadPage(currentPage.value);
};

const onUpdateSearchQuery = (searchQuery : string) => {
    query.value = searchQuery.value;
};

const onUpdateSearchTags = (dynamicTags : []) => {
    tags.value = dynamicTags.value.map((tag: { name: string; }) => tag.name);
    console.log('dynamicTags:', dynamicTags.value)
    console.log('tags:', tags.value);
};

function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    //把时间格式定为2位不够补0

    return `${year}-${month}-${day} ${hour}:${minute}`;
}

const deleteRow = async (id: number) => {
    try {
        await api.deleteQuestion({id});
        loadPage(currentPage.value);
    } catch (e) {
        console.error('Error deleting question sheet:', e);
    }
}

</script>

<template>
  <QBHeader />
    <div class="question-bank-container">
      <QBNav @updateSearchStatus="onUpdateSearchStatus" @updateSearchQuery="onUpdateSearchQuery" @updateSearchTags="onUpdateSearchTags" :total="total"></QBNav>
      <QBList :tableData="tableData" @page-change="pageChange" @delete-row="deleteRow" :total="total"></QBList>
  </div>
</template>

<style scoped>
.question-bank-container {
    width: 1200px;
    margin: 0 auto;
}
</style>