<template>
    <el-container class="qs-nav-container">
        <el-header class="header">
            <el-row :gutter="20">
<!--                <el-col :span="5">-->
<!--                    <el-select-->
<!--                      v-model="difficultyValue"-->
<!--                      placeholder="题目难度"-->
<!--                      size="default"-->
<!--                      style="width: 200px"-->
<!--                    >-->
<!--                      <el-option-->
<!--                        v-for="item in difficulty"-->
<!--                        :key="item.value"-->
<!--                        :label="item.label"-->
<!--                        :value="item.value"-->
<!--                      />-->
<!--                    </el-select>-->
<!--                </el-col>-->
                <el-col :span="5">
                    <el-select
                    v-model="typeValue"
                    placeholder="Question Type"
                    size="default"
                    style="width: 200px"
                  >
                  <el-option
                    v-for="item in type"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                  </el-select>
                </el-col>
                <el-col :span="8">
                    <el-input v-model="searchQuery" placeholder="Please enter the content or keywords" @keyup.enter="search">
                      <template #prepend >
                        <div class="search-icon-container">
                          <el-icon size="20px"><Search /></el-icon>
                        </div>
                      </template>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" @click="search">Search</el-button>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="1.5" style="margin-top: 1px" >
                    <span style="font-size: 19px">label</span>
                </el-col>
                <el-col :span="12">
                    <div class="flex gap-2">
                    <el-tag
                      v-for="tag in dynamicTags"
                      :key="tag.name"
                      closable
                      :disable-transitions="false"
                      @close="handleClose(tag)"
                      :type="tag.type"
                    >
                      {{ tag.name }}
                    </el-tag>
                    <el-input
                      v-if="inputVisible"
                      ref="InputRef"
                      v-model="inputValue"
                      class="w-20"
                      size="default"
                      @keyup.enter="handleInputConfirm"
                      @blur="handleInputConfirm"
                      style="margin-top: 4px"
                    />
                    <el-button v-else class="button-new-tag" size="small" @click="showInput">
                      + New Tag
                    </el-button>
                  </div>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="24">
                    <span> totally {{ total }} results</span>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="24">
                    <p @click="cleanAll" class="cleanAll">Clear all criteria</p>
                </el-col>
            </el-row>
        </el-header>
    </el-container>
</template>

<script setup>
import { Search } from '@element-plus/icons'
import { nextTick, ref, defineEmits} from 'vue'
import { ElInput ,ElMessage} from 'element-plus'

const searchQuery = ref('');
const isSearch = ref(false);
const emit = defineEmits(['updateSearchStatus', 'updateSearchQuery', 'updateSearchTags', 'updateSearchType']);
const props = defineProps({
    total: Number
});
const search = async () => {
    if (searchQuery.value ==='') {
        ElMessage.error('The search keyword cannot be empty');
        return;
    }
    ElMessage.success(`Search keywords: ${searchQuery.value}`);
    isSearch.value = true;
    emit('updateSearchQuery', searchQuery);
    emit('updateSearchTags', dynamicTags);
    emit('updateSearchType', typeValue);
    emit('updateSearchStatus', isSearch);
};


const difficulty = ref([
    {
      value: 'easy',
      label: '简单'
    },
    {
      value: 'medium',
      label: '中等'
    },
    {
      value: 'hard',
      label: '困难'
    },
    {
      value: 'all',
      label: '全部'
    }
  ]);
const type = ref([
    {
      value: 'single_choice',
      label: 'Single Choice'
    },
    {
      value: 'multiple_choice',
      label: 'Multiple Choice'
    },
    {
      value: 'fill_in_the_blank',
      label: 'Filling Blank'
    },
    {
      value: 'true_false',
      label: 'True or False'
    },
    {
      value: 'all',
      label: 'All'
    },
  ]);
const difficultyValue = ref('');
const typeValue = ref('');

const inputValue = ref('');
const dynamicTags = ref([]);
const inputVisible = ref(false);
const tagType = ref(['success', 'info', 'warning', 'danger', '']);

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {

  })
}

const handleClose = (tag) => {
  dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    const randomIndex = Math.floor(Math.random() * 5);
    const tagColor = tagType.value[randomIndex];
    dynamicTags.value.push({name: inputValue.value, type: tagColor})
  }
  inputVisible.value = false
  inputValue.value = ''
}


function cleanAll() {
  difficultyValue.value = ''
  typeValue.value = ''
  searchQuery.value = ''
  dynamicTags.value = []
  isSearch.value = false
  ElMessage.success(`Clear keywords and tags`);
  emit('updateSearchStatus', isSearch);
  emit('updateSearchQuery', searchQuery);
  emit('updateSearchTags', dynamicTags);
  emit('updateSearchType', typeValue);
}

</script>

<style scoped>
.qs-nav-container {
    height: 100%;
    background: linear-gradient(to right, #d7e9ff, #b3d1ff);
    opacity: 0.85;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 0 0 0 rgba(0, 0, 0, 0.1);
    border-radius: 12px;
}

.header {
    padding: 20px;
    border-radius: 4px;
    height: 100%;
    box-sizing: border-box;
}

.search-icon-container {
  width: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cleanAll {
  color: #409eff;
  cursor: pointer;
  margin-left: 85%;
}

.cleanAll:hover {
  text-decoration: underline;
}

</style>
