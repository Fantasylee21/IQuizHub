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

const search = async (keyword: string, Tags: string[]) => {
    try {
        const res = await api.search({keyword, Tags});
        tableData.value = res.results;
        console.log(res.results);
    } catch (e) {
        console.error('Error searching questions:', e);
    }

}

const currentPage = ref(1);

const pageChange = (pageNew: number) => {
    loadPage(pageNew)
    currentPage.value = pageNew;
};

const loadPage = (currentPage: number) => {
    getAllQuestion(currentPage);
}

onMounted(() => {
    loadPage(1);
})

const searchStatus = ref(false);
const searchQuery = ref('');
const dynamicTags = ref([]);

const updateSearchQuery = (query) => {
  searchQuery.value = query;
};

const updateSearchTags = (dynamicTags) => {
  dynamicTags.value = dynamicTags;
};

const handleSearchStatus = (status) => {
  searchStatus.value = status;
  if (status) {
    search(searchQuery.value, dynamicTags.value);
  } else {
    loadPage(1);
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

<template>
  <QBHeader />
    <div class="question-bank-container">
      <QBNav @updateSearchStatus="handleSearchStatus"></QBNav>
      <QBList :tableData="tableData" @page-change="pageChange" :total="total"></QBList>
  </div>
</template>

<style scoped>
.question-bank-container {
    width: 1200px;
    margin: 0 auto;
}
</style>