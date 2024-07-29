<template>
    <div class="table-container">
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="id" label="id">
            </el-table-column>
            <el-table-column prop="create_time" label="create time">
            </el-table-column>
            <el-table-column label="name">
                <template v-slot="scope">
                    <el-link @click.prevent="navigateToDetail(scope.row.id)" type="primary" underline>{{
                            scope.row.title
                        }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label="author">
                <template v-slot="scope">
                    <el-link :href="scope.row.url" type="info" underline>{{ scope.row.author }}</el-link>
                </template>
            </el-table-column>
            <el-table-column label="type">
                <template v-slot="scope">
                    <el-tag v-if="scope.row.type =='True/False' ">True or False</el-tag>
                    <el-tag v-else-if="scope.row.type =='single_choice' ">Signal Choice</el-tag>
                    <el-tag v-else-if="scope.row.type =='multiple_choice' ">Multiple Choice</el-tag>
                    <el-tag v-else-if="scope.row.type =='fill_blanks' ">Filling Blank</el-tag>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup lang="ts">
import {defineProps, ref, defineEmits, onMounted} from 'vue'
import router from '@/router'

const props = defineProps({
    tableData: Array
});

const navigateToDetail = (id: number) => {
    router.push(`/question-detail/${id}`);
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
