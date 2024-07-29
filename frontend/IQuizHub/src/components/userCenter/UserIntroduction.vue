<script setup lang="ts">
import { ref } from 'vue';
import { ElButton, ElIcon, ElLoading } from 'element-plus'
import { Comment, Delete, Edit, Finished } from '@element-plus/icons'
import api from '@/api';
import { useProfileStore } from '@/stores/profile'
const profile = useProfileStore()
const id = Number(profile.id);
const inputText = ref(profile.introduction);
const isEditing = ref(false);
const isLoading = ref(false);


function updateText(event: Event) {
  const target = event.target as HTMLTextAreaElement;
  inputText.value = target.value;
}

function inputAreaAppear() {
    const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  setTimeout(() => {
    loading.close()
    isEditing.value = true;
    isLoading.value = false;
  }, 300)
}

const uploadIntroduction = async (id : number , introduction : string) => {
    try {
        const res = await api.uploadIntroduction({id, introduction});
        console.log('uploadIntroduction:', res);
    } catch (e) {
        console.error('Error uploading introduction:', e);
    }
};


function saveEdit() {
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  uploadIntroduction(id, inputText.value);
  profile.updateProfile({introduction: inputText.value})
  setTimeout(() => {
    loading.close()
    isEditing.value = false;
    isLoading.value = false;
  }, 500)
}

function cancelEdit() {
    const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  setTimeout(() => {
    loading.close()
    isEditing.value = false;
    isLoading.value = false;
  }, 500)
}

</script>

<template>
      <div v-if="isEditing" class="content">
        <h2>Edit Your Description <el-icon :size="22"><Comment /></el-icon></h2>
        <textarea v-model="inputText" @input="updateText" ></textarea>
        <p>Max: 200</p>
        <el-button type="success" @click="saveEdit">save<el-icon :size="20"><Finished /></el-icon></el-button>
        <el-button type="danger" @click="cancelEdit">cancel<el-icon :size="20"><Delete /></el-icon></el-button>
      </div>
    <!-- 当不处于编辑状态时显示简介文本 -->
      <div v-if="!isEditing" class="content">
        <h2>Description  <el-button type="primary" @click="inputAreaAppear">Edit<el-icon :size="20"><Edit /></el-icon></el-button></h2>
        <p>{{ inputText }}</p>
      </div>
</template>

<style scoped>



.content {
  max-width: 100%;
}


textarea {
  width: 100%;
  min-height: 150px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  border-radius: 4px;
  font-size: 18px;
  padding: 10px;
}

p{
  font-size: 16px;
  color: #666;
  margin: 10px;
  line-height: 1.5;
}

h2 {
  font-size: 24px;
  margin: 10px;
}

</style>