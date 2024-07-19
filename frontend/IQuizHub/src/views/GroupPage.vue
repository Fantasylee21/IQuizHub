<script setup lang="ts">

import GroupBlock from '@/components/GroupPage/GroupBlock.vue'
import GPHeader from '@/components/GroupPage/GPHeader.vue'
</script>

<template>
  <GPHeader></GPHeader>
  <div class="GroupPage">
    <GroupBlock></GroupBlock>
  </div>
</template>

<style scoped>
.GroupPage {
    width: 1200px;
    margin: 0 auto;
}
</style>