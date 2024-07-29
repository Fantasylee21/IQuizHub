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
                <div class="chart" style="margin-top: 40px">
                    <LineChart :historys="historys"/>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import StagingInformation from "@/components/Staging/StagingInformation.vue";
import CollectList from "@/components/Staging/CollectList.vue";
import TrendsList from "@/components/Staging/TrendsList.vue";
import LineChart from "@/components/Staging/LineChart.vue";
import {onBeforeMount, ref} from "vue";
import api from "@/api";
import {useProfileStore} from "@/stores/profile";

const profile = useProfileStore()
const historys = ref([]);

onBeforeMount(async () => {
    const res = await api.getNowUser({
        id: profile.id
    })
    historys.value = res.historys
    console.log('res->', res)
    console.log('res.data.historys->', res.data.historys)
})
</script>

<style scoped>
.staging-container {
    margin: 25px auto 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 20px;
    box-sizing: border-box;
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