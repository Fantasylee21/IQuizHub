<template>
    <div class="table-container">
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="id" label="编号">
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间">
            </el-table-column>
            <el-table-column label="题单名称">
                <template v-slot="scope">
                    <el-link @click.prevent="navigateToDetail(scope.row.id)" type="primary" underline>{{
                            scope.row.title
                        }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column prop="questionCnt" label="题目数">
            </el-table-column>
            <el-table-column prop="author" label="题单作者">
            </el-table-column>
            <el-table-column label="简介">
                <template v-slot="scope">
                    <div v-html="scope.row.content"></div>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template v-slot="scope">
                    <el-button type="danger" @click="deleteRow(scope.row.id)" size="small">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
                @current-change="pageChange"
                :current-page="currentPage"
                :page-size="pageSize"
                :total="total"
                layout="prev, pager, next">
        </el-pagination>
    </div>
</template>

<script setup lang="ts">
import {defineProps, ref, defineEmits} from 'vue'
import router from '@/router'

const emit = defineEmits(['pageChange', 'deleteRow']);
const props = defineProps({
    tableData: Array,
    total: Number
});

const currentPage = ref(1);
const pageSize = ref(20);


const pageChange = (pageNew: number) => {
    emit('pageChange', pageNew);
    currentPage.value = pageNew;
};

const navigateToDetail = (id: number) => {
    router.push(`/sheet-detail/${id}`);
};

const deleteRow = (deleteId: number) => {
    emit('deleteRow', deleteId);
};


</script>

<style scoped>
.table-container {
    margin-top: 20px;
    margin-bottom: 40px;
    background: linear-gradient(to right, #e6f7ff, #d4e8ff);
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-table th,
.el-table td {
    text-align: center;
}

.el-link {
    font-weight: bold;
}

.el-pagination {
    margin-top: 20px;
    text-align: center;
}
</style>
