<template>
    <QSHeader/>
    <div class="question-sheet-container">
      <QSNav @updateSearchStatus="onUpdateSearchStatus"
             @updateSearchQuery="onUpdateSearchQuery"
             @updateSearchType="onUpdateSearchType"
             @createQuestionSheet="onCreateQuestionSheet" :total="total"></QSNav>
      <QSList :tableData="tableData" @page-change="pageChange" :total="total" @delete-row="deleteRow"></QSList>

      <el-dialog v-model="isCreate" width="500" title="Create Question Sheet" class="custom-dialog">
        <el-form :model="form">
          <el-form-item label="name">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item label="description">
            <el-input v-model="form.content"></el-input>
          </el-form-item>
          <el-form-item label="Visible users">
            <el-select v-model="form.users" multiple placeholder="Select" :disabled="form.is_all">
              <el-option v-for="item in allUsers" :key="item.id" :label="item.username" :value="item.id"></el-option>
            </el-select>
            <el-checkbox v-model="form.is_all">All</el-checkbox>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer" >
          <el-button @click="close">cancel</el-button>
          <el-button type="primary" @click="submit">submit</el-button>
        </span>
    </el-dialog>
    </div>
</template>

<script setup lang="ts">

import QSHeader from "@/components/QuestionSheet/QSHeader.vue";

import api from '@/api'
import { onMounted, ref, watch } from 'vue'

import QSNav from '@/components/QuestionSheet/QSNav.vue'
import QSList from '@/components/QuestionSheet/QSList.vue'
import { ElLoading } from 'element-plus'

const tableData = ref([]);
const total = ref(0);


interface Form {
  users: number[];
  title: string;
  content: string;
  is_all: boolean;
}

const form = ref<Form>({
  users: [],
  title: '',
  content: '',
  is_all: false
});

const getAllQuestionSheet = async (pageNumber: number) => {
    try {
        const res = await api.getAllQuestionSheet({pageNumber}); // Use pageNumber in the request
        tableData.value = res.results;
        total.value = res.count;
        console.log('total:', total.value)
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
    if (isSearching.value.value == true) {
        searchQuestionSheet(currentPage,  query.value, type.value);
    } else {
        getAllQuestionSheet(currentPage);
        console.log('total:', total.value)
    }
}

onMounted(() => {
    loadPage(1);
    getAllUsers();
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
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day} ${hour}:${minute}`;
}

const deleteRow = async (id: number) => {
    try {
        await api.deleteQuestionGroup({id});
        loadPage(currentPage.value);
    } catch (e) {
        console.error('Error deleting question sheet:', e);
    }
}


const isCreate = ref(false);
const allUsers = ref();
const onCreateQuestionSheet = (beginCreate : boolean) => {
    console.log('beginCreate:', beginCreate)
    isCreate.value = beginCreate;
}

const close = () => {
  isCreate.value = false;
};

const submit = async () => {
  try {
    console.log(form.value)
    await api.uploadQuestionGroup(form.value);
    loadPage(currentPage.value);
    close();
    const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
    })
    setTimeout(() => {
        loading.close()
    }, 500)
  } catch (e) {
    console.error('Error creating question sheet:', e);
  }
};

const getAllUsers = async () => {
    try {
        const res = await api.getAllUsers();
        allUsers.value = res;
        console.log('allUsers:', allUsers.value)
        return res;
    } catch (e) {
        console.error('Error fetching all users:', e);
    }
};

watch(() => form.value.is_all, (newVal) => {
  if (newVal) {
    form.value.users = [];
  }
});

</script>


<style scoped>
.question-sheet-container {
    width: 1200px;
    margin: 0 auto;
}

.custom-dialog {
    display: flex;
    flex-direction: column;
    padding: 20px;
}

.dialog-footer {
    display: flex;
    justify-content: center;
    margin-top: 50px;
}

.el-checkbox {
    margin-top: 5px;

}
</style>