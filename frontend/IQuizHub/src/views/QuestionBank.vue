<script setup lang="ts">

import QBHeader from '@/components/QuestionBank/QBHeader.vue'
import QBNav from '@/components/QuestionBank/QBNav.vue'
import QBList from '@/components/QuestionBank/QBList.vue'
</script>

<template>
  <QBHeader />
    <div class="question-bank-container">
      <QBNav></QBNav>
      <QBList></QBLIst>
  </div>
</template>

<style scoped>
.question-bank-container {
    width: 1200px;
    margin: 0 auto;
}
</style>