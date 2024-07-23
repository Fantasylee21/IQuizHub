<template>
    <QSHeader/>
    <div class="question-sheet-container">
      <QSNav @updateSearchStatus="onUpdateSearchStatus" @updateSearchQuery="onUpdateSearchQuery" @updateSearchType="onUpdateSearchType" :total="total"></QSNav>
      <QSList :tableData="tableData" @page-change="pageChange" :total="total"></QSList>
    </div>
</template>

<script setup lang="ts">

import QSHeader from "@/components/QuestionSheet/QSHeader.vue";

import api from '@/api'
import { onMounted, ref } from 'vue'
import QSNav from '@/components/QuestionSheet/QSNav.vue'
import QSList from '@/components/QuestionSheet/QSList.vue'

const tableData = ref([]);
const total = ref(0);

const getAllQuestionSheet = async (pageNumber: number) => {
    try {
        const res = await api.getAllQuestionSheet({pageNumber}); // Use pageNumber in the request
        tableData.value = res.results;
        total.value = res.count;
        tableData.value.forEach((item) => {
            item.create_time = formatDate(item.create_time);
        });
    } catch (e) {
        console.error('Error fetching question sheets:', e);
    }
}

const searchQuestionSheet = async (pageNumber: number, keyword: string, type: number) => {
    try {
        const res = await api.searchQuestionSheet({
            'pageNumber': pageNumber,
            'keyword': keyword,
            'type': type
        });
        tableData.value = res.results;
        total.value = res.count;
        console.log('search result:', tableData.value)
        tableData.value.forEach((item) => {
            item.create_time = formatDate(item.create_time);
        });
    } catch (e) {
        console.error('Error searching question sheets:', e);
    }
}

const currentPage = ref(1);
const query = ref('');
const isSearching = ref(false);
const type = ref(0);
const pageChange = (pageNew: number) => {
    loadPage(pageNew)
    currentPage.value = pageNew;
};

const loadPage = (currentPage: number) => {
    console.log('----->isSearching:', isSearching.value, currentPage)
    if (isSearching.value.value == true) {
        searchQuestionSheet(currentPage,  query.value, type.value);
    } else {
        getAllQuestionSheet(currentPage);
    }
}

onMounted(() => {
    loadPage(1);
})

const onUpdateSearchStatus = (isSearch : boolean) => {
    isSearching.value = isSearch;
    console.log('isSearching:', isSearching.value, currentPage.value);
    loadPage(currentPage.value);
};

const onUpdateSearchQuery = (searchQuery : string) => {
    query.value = searchQuery.value;
};

const onUpdateSearchType = (selectedType : string) => {
    console.log('selectedType:', selectedType.value)
    if (selectedType.value == 'all') {
        type.value = 0;
    } else if (selectedType.value == 'official') {
        type.value = 1;
    } else if (selectedType.value == 'user') {
        type.value = 2;
    }
};

function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    return `${year}-${month}-${day} ${hour}:${minute}`;
}

</script>


<style scoped>
.question-sheet-container {
    width: 1200px;
    margin: 0 auto;
}
</style>