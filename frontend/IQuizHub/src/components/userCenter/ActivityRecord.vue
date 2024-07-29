<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { List } from '@element-plus/icons'
import { useProfileStore } from '@/stores/profile'
import api from '@/api'

const icon = ref({
  type: 'el-icon-chat-line-round',
  color: '#8eb0e4'
});

const profile = useProfileStore();
interface History {
  id: number;
  create_time: string;
  correct: boolean;
  question: string;
}

const history = ref<History[]>([]);

const getHistory = async () => {
  try {
    const profile = useProfileStore();
    const id = profile.id;
    const res = await api.getHistory({id});
    history.value = res;
    console.log('history:', history.value);
    for (let i = 0; i < history.value.length; i++) {
      history.value[i].create_time = formatDate(history.value[i].create_time);
    }
  } catch (e) {
    console.error('Error fetching history:', e);
  }
}

onMounted(() => {
  getHistory();
});

function formatDate(time: string) {
    const date = new Date(time);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    return `${year}-${month}-${day} ${hour}:${minute}`;
}

const tableData = ref([
  {
    date: '2021-09-01',
    name: '第一题',
    type: '选择题',
    behavior: 'right'
  },
  {
    date: '2021-09-02',
    name: '第二题',
    type: '填空题',
    behavior: 'wrong'
  },
  {
    date: '2021-09-03',
    name: '第三题',
    type: '判断题',
    behavior: 'upload'
  },
  {
    date: '2021-09-04',
    name: '第四题',
    type: '选择题',
    behavior: 'right'
  }
]);
const username = profile.username;

</script>

<template>
  <h2>Activity Record <el-icon size="22px"><List /></el-icon></h2>
  <div class="block" v-for="item in history" :key="item.id">
    <el-timeline >
        <el-timeline-item :timestamp="item.create_time" :color="icon.color" placement="top">
          <el-card shadow="always" class="card">
            <p v-if="item.correct">{{username}} did {{item.question}} correctly</p>
            <p v-else>{{username}} did {{item.question}}, but is was wrong</p>
          </el-card>
        </el-timeline-item>
    </el-timeline>
  </div>
</template>

<style scoped>
h2 {
  font-size: 25px;
  margin: 30px 30px 30px 0;
}

.card{
  color: #121212;
  font-size: 18px;
}

.card:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}

</style>