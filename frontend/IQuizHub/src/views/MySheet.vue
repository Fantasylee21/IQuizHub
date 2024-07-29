<template>
    <div class="my-sheet-container">
        <h1 style="font-size: 30px; font-weight: bold; margin-bottom: 20px">Created by myself</h1>
        <el-table :data="listData" style="width: 100%">
            <el-table-column prop="id" label="ID"></el-table-column>
            <el-table-column prop="title" label="Title"></el-table-column>
            <el-table-column label="Description">
                <template v-slot="scope">
                    <div v-html="scope.row.content"></div>
                </template>
            </el-table-column>
            <el-table-column label="Operations">
                <template #default="scope">
                    <el-button size="large" @click="handleEdit(scope.row.id)">
                        Edit
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup lang="ts">
import {onBeforeMount, onMounted, ref, watch} from "vue";
import api from "@/api";
import router from "@/router";

const listData = ref<{
    id: number,
    title: string
    avatar: string
    content: string
}[]>([])

onBeforeMount(async () => {
    try {
        const response = await api.getMySheets()
        listData.value = response
    } catch (error) {
        console.error("Failed to fetch sheet list:", error);
    }
})

const handleEdit = (id: number) => {
    const url = `/sheet-editor/${id}`
    router.push(url)
}

</script>


<style scoped>
.my-sheet-container {
    margin: 70px auto 0;
    width: 1200px;
}
</style>