<script setup lang="ts">
import { ref } from 'vue'
import { ChatDotRound, Menu, Search } from '@element-plus/icons'
import router from '@/router'
const groupTable = ref([
  {
    id: 1,
    date: '2021-09-01',
    name: 'Group1',
    lastReplyTime: '2021-9-8',
    lastReplyUser: '李国庆先生',
    Type: '学术版',
    picture: 'https://www.baidu.com/img/flexible/logo/pc/result.png',
    creator: '李国庆先生',
    commentCount: 10
  },
  {
    id: 2,
    date: '2022-08-2',
    name: 'Group2',
    lastReplyTime: '2023-9-8',
    lastReplyUser: '李国庆先生',
    Type: '科研版',
    picture: 'https://www.baidu.com/img/flexible/logo/pc/result.png',
    creator: '李国庆先生',
    commentCount: 13
  },
  {
    id: 3,
    date: '2023-07-3',
    name: 'Group3',
    lastReplyTime: '2024-9-8',
    lastReplyUser: '李国庆先生',
    Type: '生活版',
    picture: 'src/assets/avatar.png',
    creator: '李国庆先生',
    commentCount: 15
  },
  {
    id: 4,
    date: '2024-06-4',
    name: 'Group4',
    lastReplyTime: '2025-9-8',
    lastReplyUser: '李国庆先生',
    Type: '学术版',
    picture: 'src/assets/avatar.png',
    creator: '李国庆先生',
    commentCount: 20
  }
]);
const tagInfo = ref([
  {
    id: 1,
    name: 'Academic',
    color: '#e84444',
  },
  {
    id: 2,
    name: 'Research',
    color: '#d6b663',
  },
  {
    id: 3,
    name: 'Life',
    color: '#352806',
  }
]);
const selectedTagId = ref('');
function getTagColor (typeName : any) {
  const tag = tagInfo.value.find(tag => tag.name === typeName);
  return tag ? tag.color : 'danger';
}
const searchQuery = ref('');
const search = () => {
  console.log(searchQuery.value);
}

function openGroup() {

}

interface TableData {
  title: string;
  content: string;
  id: number;
  create_time: string;
  update_time: string;
  author: {
    id: number;
    username: string;
    avatar: string;
    introduction: string;
  };
  type: string;
  count: number;
}

const tableData = ref<TableData[]>([]);

defineProps({
    tableData: Array
})

</script>

<template>
    <div class="searchDiv">
          <el-input v-model="searchQuery" placeholder="Search" @keyup.enter="search">
            <template #prepend >
              <div class="search-icon-container">
                <el-icon size="20px"><Search /></el-icon>
              </div>
            </template>
          </el-input>
          <div>
              <el-button type="primary" @click="search">Search</el-button>
          </div>
      </div>
    <div class="top">
      <div class="moduleSelect">
        <div class="tagTitle">
        <el-icon size="23"><Menu /></el-icon>
        <h6 @click="selectedTagId = 0" style="cursor: pointer">All</h6>
        </div>
        <div class="tagAll" v-for="item in tagInfo" :key="item.id" @click="selectedTagId = item.id" :class="{ selected: item.id === selectedTagId }">
          <el-tag effect="light" round="round" :color="item.color">&nbsp;</el-tag> {{item.name}}
        </div>
      </div>
      <div class="groupSelect">
        <el-button type="success" style="margin-top: 20px" class="elb">All Group</el-button>
        <el-button type="info" style="margin-top: 20px" class="elb">Group Created by myself</el-button>
        <el-button type="primary" style="margin-top: 20px" class="elb">Joined Group</el-button>
        <el-button color="#666" style="margin-top: 20px" class="elb">Create My Group</el-button>
      </div>
    </div>
    <div class="allBlock"
         v-for="item in tableData"
         :key="item.id"
    >
      <div class="block" @click="openGroup">
        <el-container>
<!--          <el-aside width="100px">-->
<!--            <div class="picture">-->
<!--              <el-image :src="item.picture">-->
<!--              </el-image>-->
<!--            </div>-->
<!--          </el-aside>-->
          <el-main>
            <div class="side">
              <div class="side1">
                <h2>{{item.title}}</h2>
                <div class="word">
                  <p>{{item.author.name}}</p> created in {{item.date}}
                </div>
              </div>
              <div class="side2">
                <el-tag effect="light" round="round" :color="getTagColor(item.Type)">&nbsp;</el-tag> {{item.Type}}
                <el-button type="primary" style="margin-left: 160px">Join</el-button>
                <div class="word">
                  <div class="comment">
                    <el-icon size="13px"><ChatDotRound /></el-icon>{{item.commentCount}}
                  </div>
                  last replied in {{item.lastReplyTime}}
                </div>
              </div>
            </div>
          </el-main>
        </el-container>
      </div>
    </div>
</template>

<style scoped>

.side{
  display: flex;
  justify-content: space-between;
}

.el-aside {
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.word {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.block {
  width: 96%;
  background: linear-gradient(to right, #d7e9ff, #b3d1ff);
  padding: 20px;
  margin: 20px 0 20px 5px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.block:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.picture {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  margin: auto;
}

h2{
  font-size: 25px;
  color: #409eff;
}

p {
  font-size: 20px;
  color: #4a1010;
  cursor: pointer;
}

.tagTitle {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.tagAll {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
  cursor: pointer;
}

.selected {
  font-size: large;
  color: #636cbc;
  font-weight: bolder;
}

.top {
  display: flex;
  justify-content: space-between;
  background: linear-gradient(to right, #d7e9ff, #b3d1ff);
  padding: 20px;
  margin: 20px 0 20px 5px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.top:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.elb {
  width: 150px;
  margin-left: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.elb:hover {
  background-color: #254e0f;

}

.search-icon-container {
  width: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.searchDiv {
  display: flex;
  align-items: center;
  gap: 10px;

}
</style>