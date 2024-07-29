<template>
    <header class="header">
        <div class="header-info">
            <div class="header-content">
                <div class="creator_avatar">
                    <img :src="avatar" alt="avatar">
                </div>
                <div class="content">
                    <div class="content-title">
                        <span>Hello</span>
                        <span>，</span>
                        <span class="text-red">{{ username }}</span>
                        <span>，</span>
                        <span class="welcome-text">Wishing you happiness every day</span>
                        <span>！</span>
                    </div>
                    <div class="content-bottom text-self-gray">
                        {{ introduction }}
                    </div>
                </div>
                <div class="stats">
                    <el-row style="width: 100%">
                        <el-col :span="8">
                            <el-statistic title="Correct" :value="correctCnt"/>
                        </el-col>
                        <el-col :span="8">
                            <el-statistic title="Wrong" :value="wrongCnt"/>
                        </el-col>
                        <el-col :span="8">
                            <el-statistic title="All" :value="correctCnt + wrongCnt"/>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useProfileStore} from '@/stores/profile'

const profile = useProfileStore()
const username = ref(profile.username);
const avatar = ref(profile.avatar);
const introduction = ref(profile.introduction);
const history = profile.historys;
const correctCnt = ref(0);
const wrongCnt = ref(0);
for (let i = 0; i < history.length; i++) {
    if (history[i].correct) {
        correctCnt.value++;
    } else {
        wrongCnt.value++;
    }
}

</script>

<style scoped>
.text-self-gray {
    color: #595959;
}

.text-red {
    color: #2d63c8;
    font-size: larger;
}

.header {
    display: flex;
    margin-left: 100px;
    flex-wrap: wrap;
    justify-content: center;
    width: 1200px;

    .header-info {
        padding: 16px 24px;
        display: flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
        border-radius: 8px;
    }

    .header-content {
        display: flex;
    }

    .creator_avatar {
        flex: 0 1 72px;
        transition: transform 0.3s;
    }

    .creator_avatar > img {
        width: 72px;
        height: 72px;
        border-radius: 50%;
    }

    .creator_avatar:hover {
        transform: scale(1.1);
    }

    .content {
        position: relative;
        top: 4px;
        flex: 1 1 auto;
        margin-left: 24px;
        line-height: 22px;

        .content-title {
            margin-bottom: 12px;
            font-weight: 500;
            font-size: 20px;
            line-height: 28px;
            box-sizing: border-box;

            .welcome-text {
                box-sizing: border-box;
            }
        }

        .content-bottom {
            box-sizing: border-box;
            padding-bottom: 10px;
        }
    }

    .stats {
        width: 400px;
        margin-left: 400px;
        display: flex;
        align-items: center;
        text-align: center;
    }
}

</style>