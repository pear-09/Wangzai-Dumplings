<template>
  <div class="note-detail-container">
    <h1 class="page-title">编辑文档 - {{ folder.name }}</h1>

    <div class="note-form">
      <!-- 文档内容编辑区 -->
      <div id="editor-container"></div>

      <div class="actions">
        <button @click="saveNote">保存内容</button>
        <button @click="cancelEdit">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import request from '@/utils/request';
import Quill from 'quill'; // 引入 Quill 编辑器

import type { Notefiles } from '@/types/api/getNotefiles';

const route = useRoute();
const router = useRouter();
const folderId = route.params.id;  // 获取文档 ID

const folder = ref<Notefiles>({ id: 0, name: '', created_at: '', updated_at: '' });
const quillEditor = ref<any>(null);

// 获取文件夹信息和文档内容
const fetchFolderContent = async () => {
  try {
    // 获取所有文件夹信息
    const folderResponse = await request.get('/ez-note/folder/get-all');
    const targetFolder = folderResponse.data.find(f => f.id === Number(folderId));

    if (targetFolder) {
      folder.value = targetFolder;

      // 获取文件夹对应的文档内容
      const contentResponse = await request.get(`/ez-note/note/query`, {
        params: { folder_id: folderId }  // 假设通过 folderId 获取文档内容
      });

      if (contentResponse.code === 0) {
        // 获取到文档内容
        const { content } = contentResponse.data;  // 从响应数据中解构出 content 字段
        
        // 初始化 Quill 编辑器内容
        quillEditor.value.root.innerHTML = content;  // 将文档内容填充到编辑器
      } else {
        alert('获取文档内容失败');
      }
    } else {
      alert('文件夹未找到');
      router.push({ name: 'xiezuo' });  // 跳转回写作界面
    }
  } catch (error) {
    console.error('获取文档内容失败:', error);
    alert('获取文档内容失败，请稍后重试');
  }
};



// 保存文档内容
const saveNote = async () => {
  try {
    // 获取编辑器的内容
    const content = quillEditor.value.root.innerHTML;
    const title = folder.value.name;  // 假设文档的标题是文件夹名称（你可以根据实际情况修改）
    
    // 准备请求数据
    const formData = new FormData();
    formData.append('note_id', folder.value.id.toString());  // 使用文件夹的 ID 或文档 ID
    formData.append('content', content);  // 文档内容
    formData.append('title', title);  // 文档标题
    formData.append('folder_id', folder.value.id.toString());  // 文件夹 ID

    // 请求修改文档内容的接口
    const response = await request.post('/ez-note/note/update/content', formData);

    if (response.code === 0) {
      alert('文档内容保存成功');
      router.push({ name: 'xiezuo' });  // 保存成功后跳转回写作页面
    } else {
      alert(`保存失败：${response.msg}`);
    }
  } catch (error) {
    console.error('保存文档内容失败:', error);
    alert('保存失败，请稍后重试');
  }
};


// 取消编辑
const cancelEdit = () => {
  router.push({ name: 'xiezuo' });
};

onMounted(() => {
  fetchFolderContent();  // 获取文档内容
  quillEditor.value = new Quill('#editor-container', {
    theme: 'snow', 
    placeholder: '编辑你的文档...',
  });
});
</script>

<style scoped>
.note-detail-container {
  padding: 20px;
}
.page-title {
  font-size: 24px;
  margin-bottom: 20px;
}
.note-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
#editor-container {
  height: 400px;
}
.actions {
  margin-top: 20px;
}
.actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
