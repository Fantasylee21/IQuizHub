<template>
    <div class="common-layout">
        <el-container>
            <el-header class="header" v-show="showNav">
                <GlobalMenu/>
            </el-header>
            <el-container>
                <el-aside :width="isCollapse ? '200px' : '64px'" v-show="showNav">
                    <GlobalSidebar @toggleCollapse="toggleCollapse"/>
                </el-aside>
                <el-main class="main-content">
                    <router-view/>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue';
import {useRoute} from 'vue-router'

import GlobalSidebar from "@/components/GlobalComponents/GlobalSidebar.vue";
import GlobalMenu from "@/components/GlobalComponents/GlobalMenu.vue";

const isCollapse = ref(false);
const route = useRoute();
const showNav = computed(() => {
    return route.path !== '/loginRegister'
});

const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
};
</script>

<style scoped>
.common-layout {

}

.header {
    border-bottom: 1px solid var(--el-menu-border-color);
}

.el-container {
    height: 100%;
}

.el-aside {
    transition: width 0.3s;
}

.main-content {
    flex: 1;
    padding: 0;
    /*padding: 20px;*/
}

</style>
