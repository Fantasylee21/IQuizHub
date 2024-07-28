<template>
    <div class="table-container">
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="id" label="编号">
            </el-table-column>
            <el-table-column label="题目名称">
                <template v-slot="scope">
                    <el-link @click.prevent="navigateToDetail(scope.row.id)" type="primary" underline>{{
                            scope.row.title
                        }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column label="题目作者">
                <template v-slot="scope">
                    <el-link :href="scope.row.url" type="info" underline>{{ scope.row.author }}</el-link>
                </template>
            </el-table-column>
            <el-table-column label="题目类型">
                <template v-slot="scope">
                    <el-tag v-if="scope.row.type =='True/False' ">判断题</el-tag>
                    <el-tag v-else-if="scope.row.type =='single_choice' ">单选题</el-tag>
                    <el-tag v-else-if="scope.row.type =='multiple_choice' ">多选题</el-tag>
                    <el-tag v-else-if="scope.row.type =='fill_blanks' ">填空题</el-tag>
                </template>
            </el-table-column>
            <el-table-column>
                <template v-slot="scope">
                    <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
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
const handleDelete = (id: number) => {

}

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
