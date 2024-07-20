<template>
    <div class="staging-container">
        <div class="staging-header">
            <StagingInformation/>
        </div>
        <div class="staging-body">
            <div class="staging-left">
                <CollectList/>
            </div>
            <div class="staging-right">
                <TrendsList/>
                <StagingChart/>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import StagingInformation from "@/components/Staging/StagingInformation.vue";
import CollectList from "@/components/Staging/CollectList.vue";
import TrendsList from "@/components/Staging/TrendsList.vue";
import StagingChart from "@/components/Staging/StagingChart.vue";
</script>

<style scoped>
.staging-container {
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 20px;
}

.staging-header {
    width: 100%;
}

.staging-body {
    width: 100%;
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
    padding: 20px 100px 20px 20px;
    display: flex;
    flex-direction: column;
}


</style>