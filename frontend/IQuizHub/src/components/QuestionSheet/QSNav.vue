<template>
    <el-container class="qs-nav-container">
        <el-header class="header">
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-input v-model="searchQuery" placeholder="查找题单" @keyup.enter="search">
                      <template #prepend >
                        <div class="search-icon-container">
                          <el-icon size="20px"><Search /></el-icon>
                        </div>
                      </template>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" @click="search">搜索</el-button>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="6">
                    <span>题单类型</span>
                </el-col>
                <el-col :span="12">
                    <el-button-group>
                        <el-button :type="selectedType === 'all' ? 'primary' : ''" @click="selectType('all')">
                            全部题单
                        </el-button>
                        <el-button :type="selectedType === 'official' ? 'primary' : ''" @click="selectType('official')">
                            官方精选
                        </el-button>
                        <el-button :type="selectedType === 'user' ? 'primary' : ''" @click="selectType('user')">
                            用户分享
                        </el-button>
                    </el-button-group>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="24">
                    <span>共计 {{ total }} 条结果</span>
                </el-col>
            </el-row>
        </el-header>
    </el-container>
</template>

<script setup>
import { defineEmits, ref } from 'vue'
import {ElMessage} from 'element-plus';
import { Search } from '@element-plus/icons'

const searchQuery = ref('');
const selectedType = ref('all');
const isSearch = ref(false);
const emit = defineEmits(['updateSearchStatus', 'updateSearchQuery', 'updateSearchTags', 'updateSearchType']);
const props = defineProps({
    total: Number
});

const search = () => {
    ElMessage.success(`搜索关键词: ${searchQuery.value}`);
    isSearch.value = true;
    emit('updateSearchQuery', searchQuery);
    emit('updateSearchStatus', isSearch);
};

const selectType = (type) => {
    selectedType.value = type;
    console.log(selectedType.value);
    emit('updateSearchType', selectedType);
};
</script>

<style scoped>
.qs-nav-container {
    height: 170px;
    background: linear-gradient(to right, #d7e9ff, #b3d1ff);
    opacity: 0.85;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 0 0 0 rgba(0, 0, 0, 0.1);
    border-radius: 12px;
}

.header {
    padding: 20px;
    border-radius: 4px;
    height: 100%;
    box-sizing: border-box;
}

.search-icon-container {
  width: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
