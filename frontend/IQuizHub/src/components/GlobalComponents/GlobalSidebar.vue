<template>
    <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            @open="handleOpen"
            @close="handleClose"
            :router="true"
    >
        <el-menu-item @click="toggleCollapse">
            <el-icon>
                <component :is="isCollapse ? ArrowRight : ArrowLeft"/>
            </el-icon>
            <template #title>Toggle Collapse</template>
        </el-menu-item>
        <el-sub-menu index="1">
            <template #title>
                <el-icon>
                    <location/>
                </el-icon>
                <span>Navigator One</span>
            </template>
            <el-menu-item-group>
                <template #title><span>Group One</span></template>
                <el-menu-item index="1-1">item one</el-menu-item>
                <el-menu-item index="1-2">item two</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group Two">
                <el-menu-item index="1-3">item three</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu index="1-4">
                <template #title><span>item four</span></template>
                <el-menu-item index="1-4-1">item one</el-menu-item>
            </el-sub-menu>
        </el-sub-menu>
        <el-menu-item index="/loginRegister">
            <el-icon>
                <icon-menu/>
            </el-icon>
            <template #title>Navigator Two</template>
        </el-menu-item>
        <el-menu-item index="/staging">
            <el-icon>
                <document/>
            </el-icon>
            <template #title>Navigator Three</template>
        </el-menu-item>
        <el-menu-item index="/question-sheet">
            <el-icon>
                <setting/>
            </el-icon>
            <template #title>Navigator Four</template>
        </el-menu-item>
        <el-menu-item index="/questionnaire">
            <el-icon>
                <Grid />
            </el-icon>
            <template #title>题单广场</template>
        </el-menu-item>
        <el-menu-item index="/userCenter">
            <el-icon>
                <setting/>
            </el-icon>
            <template #title>个人中心</template>
        </el-menu-item>
    </el-menu>
</template>

<script lang="ts" setup>
import {ref, defineEmits} from 'vue';
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
} from '@element-plus/icons-vue';
import {ArrowLeft, ArrowRight} from '@element-plus/icons-vue';
import {Grid} from '@element-plus/icons-vue';

const isCollapse = ref(true);
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath);
};
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath);
};
const emit = defineEmits(['toggleCollapse']);
const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value;
    emit('toggleCollapse');
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu-vertical-demo.el-menu--collapse {
    width: 64px;
}
</style>
