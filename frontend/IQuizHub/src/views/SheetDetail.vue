<template>
    <div class="sheet-editor-header">
        <div class="se-header-container">
            <el-breadcrumb separator="/" class="breadcrumb">
                <el-breadcrumb-item :to="{ path: '/staging' }">staging</el-breadcrumb-item>
                <el-breadcrumb-item :to="{ path: '/question-sheet' }">question-sheet</el-breadcrumb-item>
                <el-breadcrumb-item>
                    <a href="#">sheet-detail</a>
                </el-breadcrumb-item>
            </el-breadcrumb>
            <h1>{{ sheetData?.title }}</h1>
            <div class="info-container">
                <div class="collect-button">
                    <el-button v-show="!is_collect" type="primary" @click="collect">收藏题单</el-button>
                    <el-button v-show="is_collect" type="danger" @click="collect">取消收藏</el-button>
                </div>
                <div class="info-statistic" style="display: flex">
                    <el-statistic title="题目总数" :value="sheetData?.questionCnt"
                                  style="margin-right: 20px"></el-statistic>
                    <el-statistic title="收藏数" :value="sheetData?.favoriteCnt"></el-statistic>
                </div>

            </div>
        </div>
    </div>
    <div class="sheet-detail-container">
        <div class="sheet-detail-nav">
            <el-tabs v-model="activeName" class="demo-tabs">
                <el-tab-pane label="题单简介" name="first">
                    <div class="sheet-description">
                        <div class="description-left">
                            <el-card>
                                <h2>题单简介</h2>
                                <div v-html="sheetData?.content"></div>
                            </el-card>
                        </div>
                        <div class="description-right">
                            <el-card class="detail-card">
                                <div class="sheet-id">
                                    <p>题单编号</p>
                                    <p style="padding-right: 15px">{{ sheetData?.id }}</p>
                                </div>
                                <div class="sheet-creator">
                                    <p>创建者</p>
                                    <el-popover
                                            placement="top-start"
                                            width="300"
                                            :title="sheetData?.author.username"
                                            trigger="hover"
                                    >
                                        <template #reference>
                                            <el-button>{{ sheetData?.author.username }}</el-button>
                                        </template>
                                        <div class="creator_profile">
                                            <div class="creator_avatar_description">
                                                <el-avatar size="50"
                                                           :src="env.backEnd + sheetData?.author.avatar.slice(1)"
                                                           style="float: left"/>
                                                <p>{{ sheetData?.author.introduction }}</p>
                                            </div>
                                            <div class="creator_details">
                                                <p style="margin-bottom: 10px">
                                                    关注 <span>0</span> 粉丝 <span>32k</span> 排名 <span>19k</span>
                                                </p>
                                                <el-button type="primary" size="small">关注</el-button>
                                                <el-button size="small">私信</el-button>
                                            </div>
                                        </div>
                                    </el-popover>
                                </div>
                                <div class="sheet-type">
                                    <p>题单类型</p>
                                    <el-tag type="info" style="width: 60px; height: 32px">{{ questionType }}</el-tag>
                                </div>
                            </el-card>
                            <el-card class="detail-progress">
                                <h3 style="margin-bottom: 20px">我通过的题目 {{ sheetData?.passedCnt }} /
                                    {{ sheetData?.questionCnt }}</h3>
                                <el-progress
                                        :percentage="(sheetData?.passedCnt / sheetData?.questionCnt * 100)"
                                        :stroke-width="15"
                                        striped
                                        striped-flow
                                />
                            </el-card>
                        </div>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="题目列表" name="second">
                    <div class="sheet-list">
                        <SDList :tableData="sheetData?.questions"/>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script setup lang="ts">
import {onBeforeMount, ref} from "vue";
import SDList from "@/components/SheetDetail/SDList.vue"
import api from "@/api";
import env from "@/utils/env";
import {ElMessage} from "element-plus";

const collect = async () => {
    const response = await api.collect({questiongroup: props.id});
    if (response) {
        console.log(response);
        if (is_collect.value)
            ElMessage.success('取消成功')
        else ElMessage.success('收藏成功')
        is_collect.value = !is_collect.value
    } else {
        ElMessage.error('操作失败')
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

const props = defineProps<{
    id: string
}>()

const sheetData = ref<null | {
    title: string,
    content: string,
    id: number,
    questionCnt: number,
    favoriteCnt: number,
    passedCnt: number,
    author: {
        id: number,
        username: string,
        avatar: string,
        introduction: string
    },
    questions: {
        id: number,
        title: string,
        content: string,
        type: string,
        create_time: string
    }[],
    is_collect: boolean
}>(null)
onBeforeMount(async () => {
    try {
        const res = await api.getSheetDetail(props.id);
        sheetData.value = res
        sheetData.value?.questions.forEach((item) => {
            item.create_time = formatDate(item.create_time);
        });
        is_collect.value = res.is_collect
    } catch (error) {
        console.error("Failed to fetch sheet detail:", error);
    }
})

const is_collect = ref(false)

const activeName = ref('first')

const questionId = ref(100)
const creator = ref('洛谷')
const questionType = ref('官方题单')

</script>

<style scoped>
.sheet-editor-header {
    background-color: #f5f7fa;
    height: 150px;
    margin: 70px 20px 20px;
    border-radius: 20px;
    box-shadow: #595959 0 0 2px;
}

.se-header-container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
}

.breadcrumb {
    margin-top: 20px;
    margin-bottom: 15px;
}

h1 {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin-bottom: .5em;
    font-family: inherit;
    font-weight: bold;
    line-height: 1.2;
    color: inherit;
    font-size: 1.75em;
}

.info-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sheet-detail-container {
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
}

.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

.sheet-description {
    display: flex;
    width: 100%;
    height: 100%;
}

.description-left {
    width: 70%;
    padding: 10px;
}

.description-right {
    width: 30%;
}

h2 {
    font-size: 20px;
    margin-bottom: 2em;
    font-weight: bold;
    line-height: 1.2;
}

.detail-card {
    padding: 10px 10px 0;
    display: flex;
    flex-direction: column;
}

.sheet-id, .sheet-creator, .sheet-type {
    margin: 10px 0 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.creator_avatar_description {
    display: flex;
    flex-wrap: wrap;
}

.creator_avatar_description p {
    margin-left: 10px;
    flex: 1;
}

.creator_details {
    clear: both;
    margin-top: 10px;
}

.detail-progress {
    margin-top: 10px;
    padding-right: 10px;
}
</style>


