<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

// 导入接口定义
import type { GetNotesResponse, Note } from '@/types/api/getNotelist';

// 获取路由中的 folderId 参数
const route = useRoute();
const folderId = route.params.id as string;



// 当前文件夹的数据
const currentFolder = ref<any>(null);

// 所有笔记数据（从后端接口获取）
const notes = ref<Note[]>([]);

// 管理模式状态
const isManaging = ref(false);

// 路由
const router = useRouter();

// 获取笔记列表
// const getNotes = async () => {
//   try {
//     // 假设 API URL 配置正确
//     const response = await axios.get<GetNotesResponse>(`${import.meta.env.VITE_API_URL}/ez-note/note/query-all`);
    
//     if (response.data.code === 0) {
//       // 筛选出当前文件夹的笔记
//       const filteredNotes = response.data.data.filter(note => {
//         console.log('note.folder_id:', note.folder_id);
//         console.log('folderId:', folderId);
//         return note.folder_id.toString() === folderId
//     });
      
//       if (filteredNotes.length > 0) {
//         notes.value = filteredNotes;  // 更新笔记列表
//         currentFolder.value = {
//           id: folderId,
//           name: `文件夹 ${folderId}`, // 如果需要的话，这里可以动态获取文件夹名称
//           notes: notes.value
//         };
//       } else {
//         alert('没有找到该文件夹中的笔记');
//         // console.log(folderId)
//         // console.log(notes)

//       }
//     } else {
//       alert(response.data.msg);
//     }
//   } catch (error) {
//     console.error("获取笔记列表失败:", error);
//     alert('请求失败，请稍后重试');
//   }
// };


// !!!!!!暂时不进行筛选，直接渲染所有笔记!!!!!!!
const getNotes = async () => {
  try {
    const response = await axios.get<GetNotesResponse>(`${import.meta.env.VITE_API_URL}/ez-note/note/query-all`);

    if (response.data.code === 0) {
      // 暂时不进行筛选，直接渲染所有笔记
      notes.value = response.data.data;
      currentFolder.value = {
        id: folderId,
        name: `文件夹 ${folderId}`,
        notes: notes.value
      };
    } else {
      alert(response.data.msg);
    }
  } catch (error) {
    console.error("获取笔记列表失败:", error);
    alert('请求失败，请稍后重试');
  }
};

// 根据文件夹 ID 获取相应的文件夹信息
onMounted(() => {
  getNotes();
});

// 切换管理模式
const toggleManaging = () => {
  isManaging.value = !isManaging.value;
};

// 跳转到笔记详情页
const goToNoteDetail = (id: string) => {
  router.push({ name: 'noteDetail', params: { id } });
};

// 跳转到新建笔记页面
const goToNewNote = () => {
  router.push({ name: 'newNote' });
};

// 删除笔记
const deleteNote = (event: Event, noteId: string) => {
  // 阻止事件冒泡，防止点击删除按钮时触发跳转
  event.stopPropagation();

  // 确认删除操作
  if (confirm('确定要删除这篇笔记吗？')) {
    // 删除笔记
    const noteIndex = notes.value.findIndex(note => note.id.toString() === noteId);
    if (noteIndex !== -1) {
      notes.value.splice(noteIndex, 1);  // 删除该笔记
    }

    // 更新 currentFolder 中的笔记数据（确保页面更新）
    currentFolder.value.notes = notes.value;
  }
};
</script>


<template>
  <div class="note-list-container">
    <h1 class="page-title">我的笔记</h1>
    <button class="view-button" @click="goToNewNote">新建笔记</button>
    <button class="view-button" @click="toggleManaging">{{ isManaging ? '确定' : '管理笔记' }}</button>
    
    <!-- 确保 currentFolder 存在，再渲染笔记列表 -->
    <div v-if="currentFolder" class="note-list">
      <div v-for="note in currentFolder.notes" :key="note.id" class="note-item" @click="goToNoteDetail(note.id.toString())">
        <div class="note-header">
          <h2 class="note-title">{{ note.title }}</h2>
          <span class="note-date">{{ note.created_at }}</span>
        </div>
        <p class="note-content">{{ note.content }}</p>
  
        <!-- 根据 isManaging 显示编辑和删除按钮 -->
        <div v-show="isManaging" class="note-actions">
          <button class="view-button" @click="deleteNote($event, note.id.toString())">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

  

<style scoped>
/* 页面布局 */
.note-list-container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

/* 笔记列表 */
.note-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

/* 单个笔记项 */
.note-item {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.note-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* 笔记标题 */
.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.note-date {
  font-size: 0.875rem;
  color: #888;
}

/* 笔记内容 */
.note-content {
  font-size: 1rem;
  color: #555;
  margin: 10px 0;
  line-height: 1.5;
}

/* 查看按钮 */
.view-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  margin-right: 10px;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.view-button:hover {
  background-color: #0056b3;
}

</style>
