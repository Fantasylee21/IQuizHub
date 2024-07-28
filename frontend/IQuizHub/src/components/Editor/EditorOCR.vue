<template>
    <div class="container">
        <p style="font-weight: bold; font-size: 20px; margin-bottom: 20px">OCR识别</p>
        <el-upload
                class="upload-demo"
                action="#"
                :on-change="handleFileUpload"
                :show-file-list="false"
                accept="image/*"
        >
            <el-button size="small" type="primary">点击上传图片</el-button>
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
                title="识别结果"
                width="500"
                draggable
        >
            <p v-for="text in texts" :key="text" style="margin: 10px 0">
                {{ text }}
            </p>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="copyAllTexts">复制所有</el-button>
                    <el-button @click="dialogVisible = false">关闭</el-button>
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
            ElMessage.success('ocr识别成功')
        } catch (e) {
            ElMessage.error('ocr识别失败，是不是没有文字内容呢？')
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
            ElMessage.success('复制成功')
        }).catch(() => {
            ElMessage.error('复制失败')
        });
    } else {
        // 对于不支持navigator.clipboard的浏览器
        ElMessage.warning('复制失败')
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