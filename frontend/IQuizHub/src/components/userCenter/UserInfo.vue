<script setup lang="ts">
import {computed, ref} from 'vue';
import {ElButton, ElIcon, ElMessage} from 'element-plus'
import {Connection, Edit, HelpFilled, UserFilled} from '@element-plus/icons'
import {useProfileStore} from '@/stores/profile'
import api from '@/api'

const profile = useProfileStore()
const username = ref(profile.username);
const email = ref(profile.email);
const imgPath = ref(profile.avatar);
const imgUploadUrl = computed(() => {
    return env.backEnd + `users/${profile.id}/avatar/upload/`
})
const headers = computed(() => {
    return {
        Authorization: `Bearer ${localStorage.getItem('token')}`
    }
})

// let selectedFile = ref(null);
//
// function onFileChange(e) {
//     selectedFile.value = e.target.files[0];
// }
//
// const uploadAvatar = async (id :number, avatar: File) => {
//   try {
//     const res = await api.uploadAvatar({id, avatar});
//     profile.updateProfile({avatar: res.avatar})
//   } catch (e) {
//     console.error('Error uploading avatar:', e);
//   }
// }
//
// const changeAvatar = async () => {
//   const input = document.createElement('input');
//   input.type = 'file';
//   input.onchange = onFileChange;
//   input.click();
//
//   await new Promise<void>((resolve) => {
//     input.onchange = () => {
//       resolve();
//     };
//   });
//
//   console.log('selectedFile:', selectedFile.value);
//   if (selectedFile.value) {
//     await uploadAvatar(Number(profile.id), selectedFile.value);
//   }
// };
import type {UploadInstance} from 'element-plus'
import env from "@/utils/env";
import axios from "axios";
import router from "@/router";

const uploadRef = ref<UploadInstance>()
const submitUpload = () => {
    uploadRef.value!.submit()
    // 刷新头像
}

function myCreateGroup() {
    console.log('my create group');
    //跳转对应网页
    router.push('/groupPage')
}

function myGroup() {
    console.log('my group');
}

const uploadAvatar = async (params: { file: File }) => {
    const formData = new FormData();
    formData.append('avatar', params.file);

    try {
        const res = await axios.post(imgUploadUrl.value, formData, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        });
        if (res.status === 200) {
            ElMessage.success('upload successfully');
            console.log('res.data->', res.data)
            console.log('res.data.url->', res.data.url)
            // 刷新头像
            profile.updateProfile({
                avatar: res.data.url,
                username: profile.username,
                id: profile.id,
                mobile: profile.mobile,
                email: profile.email,
                introduction: profile.introduction
            });
            router.push('userCenter')
        } else {
            ElMessage.error('upload failed');
        }
    } catch (error) {
        ElMessage.error('upload failed');
    }
};

</script>

<template>
    <div class="info-pic">
        <div class="info">
            <h2>User Info
                <el-icon :size="22">
                    <UserFilled/>
                </el-icon>
            </h2>
            <el-form label-width="80px">
                <el-form-item label="Name:">
                    <el-input v-model="username" disabled class="area"></el-input>
                </el-form-item>
                <el-form-item label="E-mails:">
                    <el-input v-model="email" disabled class="area"></el-input>
                </el-form-item>
                <div class="groupInfo">
                    <hr class="divider"/>
                    <h1 @click="myCreateGroup">My Group
                        <el-icon :size="18">
                            <Connection/>
                        </el-icon>
                    </h1>

                </div>
            </el-form>
        </div>
        <div class="picture">
            <el-image :src="imgPath" fit="cover" class="el-img"></el-image>
            <el-upload
                    ref="uploadRef"
                    class="upload-demo"
                    name="avatar"
                    :action="imgUploadUrl"
                    :auto-upload="false"
                    :headers="headers"
                    :http-request="uploadAvatar"
            >
                <template #trigger>
                    <el-button type="primary">Select</el-button>
                </template>
                <el-button class="ml-3" type="success" style="margin-left: 10px" @click="submitUpload">
                    Upload
                </el-button>
            </el-upload>
        </div>
    </div>
</template>

<style scoped>

.groupInfo {
    font-size: 20px;
    line-height: 50px;
    margin: 40px 10px 20px 30px;
}

h1 {
    color: rgba(121, 182, 204, 0.98);
    cursor: pointer;

}

h1:hover {
    text-decoration: underline;
}

h2 {
    font-size: 25px;
    margin: 20px 30px 30px 0;
}


.area {
    width: 250px;
}


.info-pic {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.picture {
    display: flex;
    flex-direction: column; /* 设置子元素垂直排列 */
    justify-content: center; /* 水平居中对齐 */
    align-items: center;
    margin: 5% 10% 0 0;
    width: 200px;
    height: 260px;
}

.el-img {
    width: 100%;
    height: 85%;
    border-radius: 10%;
    margin-bottom: 20px;
}

.edit {
    position: relative;
    margin-top: 20px;
    height: 15%;
}

.divider {
    border: none;
    height: 1px;
    background-color: #ccc;
    margin-bottom: 20px;
    margin-left: -35px;
    margin-right: -500px;
}
</style>