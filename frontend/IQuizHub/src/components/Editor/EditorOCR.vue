<template>
    <div class="container">
        <p style="font-weight: bold; font-size: 20px; margin-bottom: 20px">OCR Recognition</p>
        <el-upload
                class="upload-demo"
                action="#"
                :on-change="handleFileUpload"
                :show-file-list="false"
                accept="image/*"
        >
            <el-button size="small" type="primary">Click to upload image</el-button>
        </el-upload>
        <el-skeleton :loading="loading" animated style="margin-top: 20px">
            <template #default>
                <el-image v-if="imageUrl"
                          style="width: 100%; margin-top: 20px;"
                          :src="imageUrl"
                          :zoom-rate="1.2"
                          :max-scale="7"
                          :min-scale="0.2"
                          :preview-src-list="srcList"
                          :initial-index="4"
                          fit="cover"
                />
            </template>
        </el-skeleton>
        <el-dialog
                v-model="dialogVisible"
                title="Identification results"
                width="500"
                draggable
        >
            <p v-for="text in texts" :key="text" style="margin: 10px 0">
                {{ text }}
            </p>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="copyAllTexts">Copy all</el-button>
                    <el-button @click="dialogVisible = false">Close</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import {ref} from 'vue';
import api from "@/api";
import {ElMessage} from "element-plus";

const dialogVisible = ref(false)
const imageUrl = ref('');
const srcList = ref([])
const loading = ref(false)
const texts = ref([])

const handleFileUpload = (file) => {
    const reader = new FileReader();

    reader.onload = async () => {
        loading.value = true
        try {
            const base64_img = reader.result.split(',')[1] // 去掉前缀
            // 调用 OCR 接口
            const ocrResponse = await api.ocr({
                base64_img,
            })

            const ocrImageUrl = ocrResponse.data.image_url
            const ocrTexts = ocrResponse.data.texts
            imageUrl.value = ocrImageUrl
            srcList.value.push(ocrImageUrl)
            texts.value = ocrTexts
            dialogVisible.value = true
            ElMessage.success('OCR recognition succeeded!')
        } catch (e) {
            ElMessage.error('OCR recognition failed, is there no text content?')
        }
        loading.value = false
    };

    if (file.raw) {
        reader.readAsDataURL(file.raw);
    }
};

function copyAllTexts() {
    // 合并所有文本为一个字符串
    const allTexts = texts.value.join('\n');

    // 尝试复制到剪贴板
    if (navigator.clipboard) {
        navigator.clipboard.writeText(allTexts).then(() => {
            ElMessage.success('copy succeeded!')
        }).catch(() => {
            ElMessage.error('copy failed!')
        });
    } else {
        // 对于不支持navigator.clipboard的浏览器
        ElMessage.warning('copy failed, please copy manually!')
    }
}
</script>

<style scoped>
.upload-demo {
    border: 1px dashed #409EFF;
    border-radius: 6px;
    padding: 20px;
    text-align: center;
    color: #666;
    cursor: pointer;
}
</style>