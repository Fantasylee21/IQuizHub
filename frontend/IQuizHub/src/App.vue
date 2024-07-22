<template>
    <div class="common-layout">
        <transition name="slide-fade">
            <el-header class="header" v-if="showNav && isMouseNearTop">
                <GlobalMenu/>
            </el-header>
        </transition>
        <el-container class="main-container">
            <el-aside :width="isCollapse ? '200px' : '64px'" v-show="showNav" style="margin-top: 50px">
                <GlobalSidebar @toggleCollapse="toggleCollapse"/>
            </el-aside>
            <el-main class="main-content">
                <router-view/>
            </el-main>
        </el-container>
    </div>
</template>

<script setup lang="ts">
import {computed, ref, onMounted, onBeforeUnmount} from 'vue';
import {useRoute} from 'vue-router';

import GlobalSidebar from "@/components/GlobalComponents/GlobalSidebar.vue";
import GlobalMenu from "@/components/GlobalComponents/GlobalMenu.vue";
import router from "@/router";

const isCollapse = ref(false);
const route = useRoute();
const showNav = computed(() => {
    return route.path !== '/loginRegister';
});

const isMouseNearTop = ref(false);

const handleMouseMove = (event: MouseEvent) => {
    isMouseNearTop.value = event.clientY <= 60;
};

const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
};

onMounted(() => {
    window.addEventListener('mousemove', handleMouseMove);
});

onBeforeUnmount(() => {
    window.removeEventListener('mousemove', handleMouseMove);
});

router.push('/loginRegister');
</script>

<style scoped>
.common-layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow-y: hidden;
}

.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: white;
    border-bottom: 1px solid var(--el-menu-border-color);
    transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.main-container {
    flex: 1;
    display: flex;
    height: 100%;
}

.el-aside {
    transition: width 0.3s;
}

.main-content {
    flex: 1;
    padding: 0;
}

.slide-fade-enter-active, .slide-fade-leave-active {
    transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.slide-fade-enter, .slide-fade-leave-to /* .slide-fade-leave-active in <2.1.8 */
{
    transform: translateY(-100%);
    opacity: 0;
}
</style>
