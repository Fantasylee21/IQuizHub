<script setup lang="ts">

import GPHeader from '@/components/GroupPage/GPHeader.vue'
import {computed, onBeforeMount, onMounted, ref} from 'vue'
import api from '@/api'
import {ChatDotRound, Menu, Search} from '@element-plus/icons'
import {ElLoading, ElMessage} from 'element-plus'
import {useProfileStore} from '@/stores/profile'
import router from '@/router'


const tagInfo = ref([
    {
        id: '1',
        name: 'Academic',
        color: '#e84444',
    },
    {
        id: 2,
        name: 'Research',
        color: '#d6b663',
    },
    {
        id: 3,
        name: 'Life',
        color: '#352806',
    }
]);
const selectedTagId = ref(0);

function getTagColor(typeName: any) {
    const tag = tagInfo.value.find(tag => tag.name === typeName);
    return tag ? tag.color : 'danger';
}

const searchQuery = ref('');

const searchGroupDetail = async () => {
    console.log('searchQuery:', searchQuery.value, selectedTagId)
    try {
        const res = await api.searchGroupDetail({title: searchQuery.value, type: selectedTagId.value.toString()});
        tableData.value = res.results;
        ElMessage.success(`Search keyword: ${searchQuery.value}`);
        console.log('res:', res)
    } catch (e) {
        console.error('Error fetching group detail:', e);
        ElMessage.error('The search keyword cannot be empty');
    }
}

onMounted(() => {
    getAllGroups()
})

interface TableData {
    title: string;
    content: string;
    id: number;
    create_time: string;
    update_time: string;
    author: {
        id: number;
        username: string;
        avatar: string;
        introduction: string;
    };
    type: string;
    cnt: number;
    is_in: boolean;
}

const tableData = ref<TableData[]>([]);

const getAllGroups = async () => {
    try {
        const res = await api.getAllGroups();
        console.log('-======res:', res)
        for (let i = 0; i < res.results.length; i++) {
            res.results[i].create_time = formatDate(res.results[i].create_time);
            res.results[i].update_time = formatDate(res.results[i].update_time);
        }
        tableData.value = res.results;
        console.log('res:', res)
    } catch (e) {
        console.error('Error fetching groups:', e);
    }
}

function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    //把时间格式定为2位不够补0

    return `${year}-${month}-${day} ${hour}:${minute}`;
}

const createGroup = async (groupData: { title: string; content: string; type: string }) => {
    try {
        const res = await api.createGroup(groupData);
        if (res) {
            await getAllGroups();
        }
    } catch (e) {
        console.error('Error creating group:', e);
    }
};
const createGroupModalVisible = ref(false);

interface Form {
    title: string;
    content: string;
    type: string;
}

const form = ref<Form>({
    title: '',
    content: '',
    type: ''
});
const submit = async () => {
    await createGroup(form.value)
    await getAllGroups()
    close();
    const loading = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
    })
    setTimeout(() => {
        loading.close()
    }, 500)
};
const close = () => {
    createGroupModalVisible.value = false;
};

const lgq = ref(0);

const profile = useProfileStore()
const username = profile.username;

const filteredTableData = computed(() => {
    console.log('username:', username)
    console.log('lgq:', lgq.value)
    if (lgq.value === 0) {
        return tableData.value;
    } else if (lgq.value === 1) {
        return tableData.value.filter(item => item.author.username == username);
    } else if (lgq.value === 2) {
        return tableData.value.filter(item => item.author.username != username);
    }
    return tableData.value;
});

const navigateToDetail = (id: number) => {
    router.push(`/groupDetail/${id}`);
};

const joinGroup = async (id: number) => {
    try {
        const res = await api.joinGroup({usergroup_id: id});
        if (res) {
            ElMessage.success('Succeed');
        }
    } catch (e) {
        console.error('Error joining group:', e);
        ElMessage.error('Failed');
    }
};

</script>

<template>
    <GPHeader></GPHeader>
    <div class="GroupPage">
        <div class="searchDiv">
            <el-input v-model="searchQuery" placeholder="Search" @keyup.enter="searchGroupDetail">
                <template #prepend>
                    <div class="search-icon-container">
                        <el-icon size="20px">
                            <Search/>
                        </el-icon>
                    </div>
                </template>
            </el-input>
            <div>
                <el-button type="primary" @click="searchGroupDetail">Search</el-button>
            </div>
        </div>
        <div class="top">
            <div class="moduleSelect">
                <div class="tagTitle">
                    <el-icon size="23">
                        <Menu/>
                    </el-icon>
                    <h6 @click="selectedTagId = 0" style="cursor: pointer">All</h6>
                </div>
                <div class="tagAll" v-for="item in tagInfo" :key="item.id" @click="selectedTagId = item.id"
                     :class="{ selected: item.id === selectedTagId }">
                    <el-tag effect="light" round="round" :color="item.color">&nbsp;</el-tag>
                    {{ item.name }}
                </div>
            </div>
            <div class="groupSelect">
                <el-button type="success" style="margin-top: 20px" class="elb" @click="lgq = 0">All Group</el-button>
                <el-button type="info" style="margin-top: 20px" class="elb" @click="lgq = 1">Created by myself</el-button>
                <el-button type="primary" style="margin-top: 20px" class="elb" @click="lgq = 2">Joined Group</el-button>
                <el-button color="#666" style="margin-top: 20px" class="elb" @click="createGroupModalVisible = true">
                    Create my Group
                </el-button>
            </div>
        </div>
        <div class="allBlock"
             v-for="item in filteredTableData"
             :key="item.id"
        >
            <div class="block" @click="navigateToDetail(item.id)">
                <el-container>
                    <el-aside width="100px">
                        <div class="picture">
                            <el-image
                                    src="https://pic2.zhimg.com/v2-0dda71bc9ced142bf7bb2d6adbebe4f0_r.jpg?source=1940ef5c">
                            </el-image>
                        </div>
                    </el-aside>
                    <el-main>
                        <div class="side">
                            <div class="side1">
                                <h2>{{ item.title }}</h2>
                                <div class="word">
                                    <p>{{ item.author.username }}</p> created in {{ item.create_time }}
                                </div>
                            </div>
                            <div class="side2">
                                <el-tag effect="light" round="round" :color="getTagColor(item.type)">&nbsp;</el-tag>
                                {{ item.type }}
                                <el-button type="primary" style="margin-left: 160px" @click="joinGroup(item.id)"
                                           :disabled="item.is_in">Join
                                </el-button>
                                <div class="word">
                                    <div class="comment">
                                        <el-icon size="13px">
                                            <ChatDotRound/>
                                        </el-icon>
                                        {{ item.cnt }}
                                    </div>
                                    last replied in {{ item.update_time }}
                                </div>
                            </div>
                        </div>
                    </el-main>
                </el-container>
            </div>
        </div>
        <el-dialog v-model="createGroupModalVisible" width="500" title="Create my group" class="custom-dialog">
            <el-form :model="form">
                <el-form-item label="group name">
                    <el-input v-model="form.title"></el-input>
                </el-form-item>
                <el-form-item label="description">
                    <el-input v-model="form.content"></el-input>
                </el-form-item>
                <el-form-item label="group type">
                    <el-select v-model="form.type" placeholder="Select">
                        <el-option label="Academic" value="Academic"></el-option>
                        <el-option label="Research" value="Research"></el-option>
                        <el-option label="Life" value="Life"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
          <el-button @click="close">cancel</el-button>
          <el-button type="primary" @click="submit">submit</el-button>
        </span>
        </el-dialog>
    </div>
</template>

<style scoped>
.GroupPage {
    width: 1200px;
    margin: 0 auto;
}

.side {
    display: flex;
    justify-content: space-between;
}

.el-aside {
    display: flex;
    justify-content: center;
    align-items: center;
}

.el-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.word {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}

.block {
    width: 96%;
    background: linear-gradient(to right, #d7e9ff, #b3d1ff);
    padding: 20px;
    margin: 20px 0 20px 5px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    cursor: pointer;
}

.block:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.picture {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100px;
    height: 100px;
    margin: auto;
}

h2 {
    font-size: 25px;
    color: #409eff;
}

p {
    font-size: 20px;
    color: #4a1010;
    cursor: pointer;
}

.tagTitle {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}

.tagAll {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 16px;
    cursor: pointer;
}

.selected {
    font-size: large;
    color: #636cbc;
    font-weight: bolder;
}

.top {
    display: flex;
    justify-content: space-between;
    background: linear-gradient(to right, #d7e9ff, #b3d1ff);
    padding: 20px;
    margin: 20px 0 20px 5px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.top:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.elb {
    width: 150px;
    margin-left: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.elb:hover {
    background-color: #254e0f;
}

.elb:focus {
    background-color: #655fcd;
}

.search-icon-container {
    width: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.searchDiv {
    display: flex;
    align-items: center;
    gap: 10px;

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