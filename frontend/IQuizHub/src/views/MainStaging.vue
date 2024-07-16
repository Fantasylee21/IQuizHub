<template>
    <div class="staging-container">
        <div class="staging-header">
            <StagingInformation/>
        </div>
        <div class="staging-body">
            <div class="staging-left">
                <CollectList/>
            </div>
            <div class="staging-right"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import StagingInformation from "@/components/Staging/StagingInformation.vue";
import CollectList from "@/components/Staging/CollectList.vue";
</script>

<style scoped>
.staging-container {
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.staging-header {
    width: 100%;
}

.staging-body {
    width: 100%;
    height: 400px;
    display: flex;
    margin-top: 10px;
}

.staging-left {
    width: 70%;
    display: flex;
    flex-direction: column;
    padding: 20px;
}

.staging-right {
    width: 30%;
    padding-right: 40px;
    display: flex;
    flex-direction: column;
}


</style>