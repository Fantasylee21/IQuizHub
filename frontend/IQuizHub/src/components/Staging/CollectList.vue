<template>
    <div class="favorites-container">
        <div class="header">
            <span>Collected question sheets</span>
        </div>
        <el-row :gutter="20">
            <el-col :span="8" v-for="doc in documents" :key="doc.questiongroup.id" class="col">
                <el-card class="document-card" @click="navigateToLink(doc.questiongroup.id)">
                    <div class="card-content">
                        <img :src="env.backEnd + doc.questiongroup.avatar.slice(1)" alt="document image"
                             class="card-image"/>
                        <div class="card-text">
                            <h3 class="card-title">{{ doc.questiongroup.title }}</h3>
                            <p class="card-description" v-html="doc.questiongroup.content"></p>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts">
import {onBeforeMount, ref} from 'vue';
import api from "@/api";
import {useProfileStore} from "@/stores/profile";
import env from "@/utils/env";

const profile = useProfileStore()
const documents = ref<any[]>([]);

onBeforeMount(async () => {
    console.log('profile.id->', profile.id)
    const response = await api.getCollects({id: profile.id})
    if (response) {
        documents.value = response
    }
})


const navigateToLink = (id: number) => {
    window.location.href = `/question-sheet/${id}`;
};
</script>

<style scoped>
.favorites-container {
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
    background-color: #f5f7fa;
    border-radius: 10px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header span {
    font-size: 20px;
    font-weight: bold;
    color: #1f2d3d;
}

.view-all-btn {
    font-size: 14px;
    text-decoration: none;
    color: #1890ff;
}

.document-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 5px;
    border-radius: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    background-color: #ffffff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.document-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.2);
}

.card-content {
    display: flex;
    flex-direction: row;
}

.card-image {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 50%;
    margin-right: 20px;
}

.card-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: calc(100% - 100px);
}

.card-title {
    margin: 0;
    font-size: 16px;
    font-weight: bold;
    color: #1f2d3d;
}

.card-description {
    margin: 5px 0 0 0;
    font-size: 14px;
    color: #666;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 2.6em;
    line-height: 1.3em;
}

.col {
    padding: 0 !important;
}
</style>
