<template>
    <header class="header">
        <div class="header-info">
            <div class="header-content">
                <div class="avatar">
                    <img src="@/assets/avatar.jpg" alt="avatar">
                </div>
                <div class="content">
                    <div class="content-title">
                        <span>早安</span>
                        <span>，</span>
                        <span class="text-red">Poseidon</span>
                        <span>，</span>
                        <span class="welcome-text">祝你开心每一天</span>
                        <span>！</span>
                    </div>
                    <div class="content-bottom text-self-gray">
                        这里写点啥捏？？？
                    </div>
                </div>
                <div class="stats">
                    <el-row style="width: 100%">
                        <el-col :span="8">
                            <el-statistic title="统计数据一" :value="statisticVal"/>
                        </el-col>
                        <el-col :span="8">
                            <el-statistic title="统计数据二" :value="statisticVal"/>
                        </el-col>
                        <el-col :span="8">
                            <el-statistic title="统计数据三" :value="statisticVal"/>
                        </el-col>
                    </el-row>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts">
import {ref} from "vue";

const statisticVal = ref(10000);

</script>

<style scoped>
.text-self-gray {
    color: #595959;
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

    .avatar {
        flex: 0 1 72px;
        transition: transform 0.3s;
    }

    .avatar > img {
        width: 72px;
        height: 72px;
        border-radius: 50%;
    }

    .avatar:hover {
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