<template>
    <div class="table-container">
        <el-table :data="paginatedData" style="width: 100%">
            <el-table-column prop="编号" label="编号">
            </el-table-column>
            <el-table-column label="名称">
                <template v-slot="scope">
                    <el-link :href="scope.row.url" type="primary" underline>{{ scope.row.名称 }}</el-link>
                </template>
            </el-table-column>
            <el-table-column prop="题目数" label="题目数">
            </el-table-column>
            <el-table-column prop="收藏数" label="收藏数">
            </el-table-column>
        </el-table>
        <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize"
                :total="tableData.length"
                layout="prev, pager, next"
                @current-change="handlePageChange"
        >
        </el-pagination>
    </div>
</template>

<script>
import {ref, computed} from 'vue';

export default {
    name: 'TableComponent',
    setup() {
        const tableData = ref([
            {编号: 100, 名称: '【入门1】顺序结构', 题目数: 15, 收藏数: 22779, url: '#'},
            {编号: 101, 名称: '【入门2】分支结构', 题目数: 18, 收藏数: 9119, url: '#'},
            {编号: 102, 名称: '【入门3】循环结构', 题目数: 21, 收藏数: 7930, url: '#'},
            {编号: 103, 名称: '【入门4】数组', 题目数: 20, 收藏数: 6635, url: '#'},
            {编号: 104, 名称: '【入门5】字符串', 题目数: 15, 收藏数: 5097, url: '#'},
            {编号: 105, 名称: '【入门6】函数与结构体', 题目数: 15, 收藏数: 4566, url: '#'},
            {编号: 106, 名称: '【算法1-1】模拟与精度', 题目数: 16, 收藏数: 5094, url: '#'},
            {编号: 107, 名称: '【算法1-2】排序', 题目数: 13, 收藏数: 4147, url: '#'},
            {编号: 108, 名称: '【算法1-3】暴力枚举', 题目数: 14, 收藏数: 3422, url: '#'},
            {编号: 109, 名称: '【算法1-4】递推与归', 题目数: 15, 收藏数: 4027, url: '#'}, {
                编号: 100,
                名称: '【入门1】顺序结构',
                题目数: 15,
                收藏数: 22779,
                url: '#'
            },
            {编号: 101, 名称: '【入门2】分支结构', 题目数: 18, 收藏数: 9119, url: '#'},
            {编号: 102, 名称: '【入门3】循环结构', 题目数: 21, 收藏数: 7930, url: '#'},
            {编号: 103, 名称: '【入门4】数组', 题目数: 20, 收藏数: 6635, url: '#'},
            {编号: 104, 名称: '【入门5】字符串', 题目数: 15, 收藏数: 5097, url: '#'},
            {编号: 105, 名称: '【入门6】函数与结构体', 题目数: 15, 收藏数: 4566, url: '#'},
            {编号: 106, 名称: '【算法1-1】模拟与精度', 题目数: 16, 收藏数: 5094, url: '#'},
            {编号: 107, 名称: '【算法1-2】排序', 题目数: 13, 收藏数: 4147, url: '#'},
            {编号: 108, 名称: '【算法1-3】暴力枚举', 题目数: 14, 收藏数: 3422, url: '#'},
            {编号: 109, 名称: '【算法1-4】递推与归', 题目数: 15, 收藏数: 4027, url: '#'}, {
                编号: 100,
                名称: '【入门1】顺序结构',
                题目数: 15,
                收藏数: 22779,
                url: '#'
            },
            {编号: 101, 名称: '【入门2】分支结构', 题目数: 18, 收藏数: 9119, url: '#'},
            {编号: 102, 名称: '【入门3】循环结构', 题目数: 21, 收藏数: 7930, url: '#'},
            {编号: 103, 名称: '【入门4】数组', 题目数: 20, 收藏数: 6635, url: '#'},
            {编号: 104, 名称: '【入门5】字符串', 题目数: 15, 收藏数: 5097, url: '#'},
            {编号: 105, 名称: '【入门6】函数与结构体', 题目数: 15, 收藏数: 4566, url: '#'},
            {编号: 106, 名称: '【算法1-1】模拟与精度', 题目数: 16, 收藏数: 5094, url: '#'},
            {编号: 107, 名称: '【算法1-2】排序', 题目数: 13, 收藏数: 4147, url: '#'},
            {编号: 108, 名称: '【算法1-3】暴力枚举', 题目数: 14, 收藏数: 3422, url: '#'},
            {编号: 109, 名称: '【算法1-4】递推与归', 题目数: 15, 收藏数: 4027, url: '#'},
        ]);

        const currentPage = ref(1);
        const pageSize = ref(20);

        const paginatedData = computed(() => {
            const start = (currentPage.value - 1) * pageSize.value;
            const end = start + pageSize.value;
            return tableData.value.slice(start, end);
        });

        const handlePageChange = (page) => {
            currentPage.value = page;
        };

        return {
            tableData,
            currentPage,
            pageSize,
            paginatedData,
            handlePageChange,
        };
    },
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
