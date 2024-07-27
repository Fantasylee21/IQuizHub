<template>
    <div class="nav-container">
        <el-menu
                :default-active="activeIndex"
                class="el-menu-demo"
                mode="horizontal"
                :ellipsis="false"
                @select="handleSelect"
        >
            <img
                    style="width: 120px; margin-left: 60px"
                    src="@/assets/logo.png"
                    alt="Element logo"
            />
            <div class="flex-grow"/>
            <el-menu-item>
                <el-avatar :src="profile.avatar" @click="router.push('/userCenter')"></el-avatar>
            </el-menu-item>

        </el-menu>
    </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import {useProfileStore} from "@/stores/profile";
import router from "@/router";

const profile = useProfileStore()
const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style>
.nav-container {
    margin: 0 auto;
    width: 1200px;
}

.flex-grow {
    flex-grow: 1;
}
</style>