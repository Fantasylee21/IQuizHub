<template>
    <QSHeader/>
    <div class="question-sheet-container">
        <QSNav></QSNav>
        <QSList></QSList>
    </div>
</template>

<script setup lang="ts">

import QSHeader from "@/components/QuestionSheet/QSHeader.vue";
import QSNav from "@/components/QuestionSheet/QSNav.vue";
import QSList from "@/components/QuestionSheet/QSList.vue";
</script>


<style scoped>
.question-sheet-container {
    width: 1200px;
    margin: 0 auto;
}
</style>