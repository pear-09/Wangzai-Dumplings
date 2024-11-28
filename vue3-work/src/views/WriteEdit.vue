<template>
  <div class="note-detail-container">
    <!-- 返回按钮 -->
    <button @click="goBack" class="back-button">返回</button>

    <!-- 文档标题 -->
    <h1 class="page-title"> 
      <input v-model="folderName" type="text" class="title-input" placeholder="请输入文档标题" />
    </h1>

    <!-- 文档内容编辑区 -->
    <div class="note-form">
      <div id="editor-container"></div>
    </div>

    <!-- 功能弹窗 -->
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <h3>{{ popupTitle }}</h3>
        <form @submit.prevent="handleFormSubmit">
          <div v-if="popupType === '段落美化'">
            <label for="text">Text</label>
            <input type="text" v-model="formData.text" id="text" placeholder="请输入文本" />
            <label for="length">Length</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入长度" />
          </div>

          <div v-if="popupType === '生成段落'">
            <label for="prompt">Prompt</label>
            <input type="text" v-model="formData.prompt" id="prompt" placeholder="请输入提示" />
            <label for="length">Length</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入段落长度" />
            <label for="tone">Tone</label>
            <select v-model="formData.tone" id="tone">
              <option value="formal">neutral</option>
              <option value="formal">formal</option>
              <option value="informal">informal</option>
              <option value="humorous">humorous</option>
              <option value="motivational">motivational</option>
              <option value="serious">serious</option>
              <option value="friendly">friendly</option>
              <option value="sarcastic">sarcastic</option>
              <option value="pessimistic">pessimistic</option>

            </select>
            <label for="style">Style</label>
            <select v-model="formData.style" id="style">
              <option value="default">默认</option>
              <option value="academic">学术</option>
              <option value="creative">创意</option>
              <option value="technical">技术</option>
              <option value="narrative">叙事</option>
              <option value="descriptive">描述性</option>
              <option value="concise">简洁</option>
              <option value="emotional">情感</option>
            </select>

          </div>

          <div v-if="popupType === '续写内容'">
            <label for="text">Text</label>
            <input type="text" v-model="formData.text" id="text" placeholder="请输入文本" />
            <label for="length">Length</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入续写长度" />
          </div>

          <div v-if="popupType === '写作提示'">
            <label for="prompt">Prompt</label>
            <input type="text" v-model="formData.prompt" id="prompt" placeholder="请输入提示" />
            <label for="length">Length</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入提示长度" />
            <label for="content_type">Content Type</label>
            <select v-model="formData.content_type" id="content_type">
              <option value="inspiration">生成写作灵感</option>
              <option value="outline">生成写作大纲</option>
              <option value="title">生成吸引人的标题</option>
              <option value="character_bio">生成角色设定</option>
              <option value="scene_description">生成场景描述</option>
              <option value="dialogue">生成对话内容</option>
              <option value="plot_twist">生成情节转折</option>
              <option value="setting">生成环境设定</option>
              <option value="synopsis">生成故事摘要</option>
            </select>

          </div>

          <div v-if="popupType === '文章分析'">
            <label for="text">Text:默认上传所有内容</label>
            <!-- <input type="text" v-model="formData.text" id="text" placeholder="将默认上传本编辑的所有文本" /> -->
            <label for="length">Length</label>
            <input type="number" v-model="formData.length" id="length" placeholder="请输入分析长度" />
            <label for="type">Type</label>
            <select v-model="formData.type" id="type">
              <option value="analysis">分析</option>
              <option value="evaluation">评价</option>
              <option value="correction">纠错</option>
            </select>

          </div>

          <button type="submit">提交</button>
          <button @click="closePopup" type="button">关闭</button>
        </form>
      </div>
    </div>
  </div>
  <div>
    <div v-if="showBeautifiedContent" class="popupbeauty">
      <textarea v-model="beautifiedText" class="editable-textarea"></textarea>
      <button @click="replaceWithBeautifiedContent">插入美化内容</button>
      <button @click="cancelBeautify">取消</button>
    </div>
  </div>

  <div v-if="showPopupcontent" class="popcontent">
    <div class="popcontent-body">
      <textarea v-model="popInputContent" class="popcontent-textarea" placeholder="请输入内容"></textarea>
      <div class="popcontent-buttons">
        <button @click="handleInsert">插入</button>
        <button @click="closePopContent">取消</button>
      </div>
    </div>
  </div>
  <!-- 选择文本后的操作按钮 -->
<div v-if="showSelectionButtons" class="selection-buttons">
  <button @click="handleSelectionChoice(true)">√</button>
  <button @click="handleSelectionChoice(false)">×</button>
</div>
<div v-if="showParagraphPopup" class="popcontent">
  <div class="popcontent-body">
    <textarea v-model="popInputContent" class="popcontent-textarea" placeholder="请输入内容"></textarea>
    <div class="popcontent-buttons">
      <button @click="handleInsert">插入</button>
      <button @click="closeParagraphPopup">取消</button>
    </div>
  </div>
</div>
</template>


<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Quill from 'quill';
import request from '@/utils/request';

const route = useRoute();
const router = useRouter();

const isNew = Number(route.query.isNew) === 1;
const docId = isNew ? null : route.params.id;

const folderId = route.query.folder_id || 0;
const folderName = ref(route.query.docName || '无标题');

let saveInterval: any = null;  // 用于存储定时器ID
const showPopup = ref(false);
const showPopupcontent = ref(false);
const popupTitle = ref('');
const popupType = ref('');
const formData = ref<{
  text: string;
  length: number;
  prompt: string;
  tone: string;
  style: string;
  content_type: string;
  type: string;
  AI_model: number;  // 显式定义为 number 类型
}>({
  text: '',
  length: 0,
  prompt: '',
  tone: '',
  style: '',
  content_type: '',
  type: '',
  AI_model: 0  // 默认值为 0
});




// 定义响应式状态
const showParagraphPopup = ref(false);  // 用来控制弹窗是否显示
const popInputContent = ref('');  // 用于输入框的双向绑定

// 弹窗打开的函数
const openParagraphPopup = () => {
  showParagraphPopup.value = true;
};

// 弹窗关闭的函数
const closeParagraphPopup = () => {
  showParagraphPopup.value = false;
};

const quillEditor = ref(null);  // 这里 quillEditor 的类型是 `Ref<Quill | null>`
// 插入弹窗编辑器的内容到 Quill 编辑器中
const insertIntoQuill = () => {
  console.log('insertIntoQuill called'); // 检查函数是否被调用

  if (quillEditor.value && popInputContent.value) {
    console.log(quillEditor.value);

    // 获取文档的总长度，作为插入位置
    const insertPosition = quillEditor.value.getLength(); // 获取文章末尾位置

    // 插入弹窗内容到文章末尾
    quillEditor.value.insertText(insertPosition, popInputContent.value);

    // 隐藏弹窗
    showParagraphPopup.value = false;
  }
};

const handleInsert = () => {
  insertIntoQuill();
};


onMounted(async () => {
  quillEditor.value = new Quill('#editor-container', {
    theme: 'snow',
    placeholder: '编辑你的文档...',
    modules: {
      toolbar: [
        ['bold', 'italic', 'underline', 'strike'],        // 加粗、斜体、下划线、删除线
        [{ 'header': [1, 2, 3, false] }],                // 标题大小
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],   // 列表
        ['link', 'image'],                               // 链接和图片
        [{ 'model': [] }, { '功能': [] }],               // 自定义工具
      ],
    },
  });

  const toolbar = quillEditor.value.getModule('toolbar');

  // 添加 "model" 工具
  const modelButton = document.createElement('span');
  modelButton.classList.add('ql-model');
  modelButton.innerHTML = '📦';
  modelButton.title = '选择模型';
  const modelDropdown = document.createElement('select');
  ['无','openAI', 'Kimi'].forEach(option => {
    const item = document.createElement('option');
    item.value = option;
    item.innerText = option;
    modelDropdown.appendChild(item);
  });
  toolbar.container.appendChild(modelButton);
  toolbar.container.appendChild(modelDropdown);

  // 添加 "功能" 工具
  const featureButton = document.createElement('span');
  featureButton.classList.add('ql-功能');
  featureButton.innerHTML = '🔧';
  featureButton.title = '功能';
  const featureDropdown = document.createElement('select');
  [
    '无',
    '段落美化',
    '生成段落',
    '续写内容',
    '写作提示',
    '文章分析',
  ].forEach(option => {
    const item = document.createElement('option');
    item.value = option;
    item.innerText = option;
    featureDropdown.appendChild(item);
  });
  toolbar.container.appendChild(featureButton);
  toolbar.container.appendChild(featureDropdown);

  // 添加功能逻辑（根据需要处理选择事件）
  modelDropdown.addEventListener('change', handleModelChange);
  featureDropdown.addEventListener('change', handleFeatureChange);

  if (!isNew && docId) {
    await fetchDocumentContent();
  }

  // 设置定时自动保存，每3秒保存一次
  saveInterval = setInterval(saveNote, 300000);
  quillEditor.value.on('selection-change', function (range) {
    if (range && range.length > 0) {
      // 文本被选中，显示操作按钮
      showTextSelectionOptions(range);
    } else {
      // 没有文本被选中，隐藏按钮
      hideTextSelectionOptions();
    }
  });


});

const beautifiedText = ref<string>(''); // 用来存储后端返回的段落美化内容
const showBeautifiedContent = ref(false);  // 控制是否显示美化后的内容
const selectedRange = ref(null);
const showSelectionButtons = ref(false);
let lastAIModel = formData.value.AI_model;  // 初始化 lastAIModel 来保存上次的值


const showTextSelectionOptions = (range) => {
  selectedRange.value = range;
  showSelectionButtons.value = true;
};

const hideTextSelectionOptions = () => {
  showSelectionButtons.value = false;
};

const handleSelectionChoice = (isAccepted) => {
  if (isAccepted && selectedRange.value) {
    // 获取选中的文本内容
    const selectedText = quillEditor.value.getText(selectedRange.value.index, selectedRange.value.length);
    formData.value.text = selectedText; // 将选中的文本存储在 text 中
  }
  hideTextSelectionOptions(); // 隐藏按钮
};

onBeforeUnmount(() => {
  // 清除定时器
  if (saveInterval) {
    clearInterval(saveInterval);
  }
});
const handleModelChange = (event) => {
  const selectedModel = event.target.value;
  console.log('Selected model:', selectedModel);

  // 根据选择的模型设置 formData 的 AI_model 字段
  switch (selectedModel) {
    case 'openAI':
      formData.value.AI_model = 0;  // 选择 openAI 时设置为 0
      break;
    case 'Kimi':
      formData.value.AI_model = 1;  // 选择 Kimi 时设置为 1
      break;
    case '无':
      formData.value.AI_model = -1;  // 选择 "无" 时不发起 AI 请求
      break;
    default:
      formData.value.AI_model = -1;  // 默认不发起 AI 请求
      break;
  }

  console.log('AI Model saved to formData:', formData.value.AI_model);
};


const handleFeatureChange = (event) => {
  const selectedFeature = event.target.value;
  console.log('Selected feature:', selectedFeature);
  switch (selectedFeature) {
    case '段落美化':
      showPopupDetails('段落美化', '段落美化');
      break;
    case '生成段落':
      showPopupDetails('生成段落', '生成段落');
      break;
    case '续写内容':
      showPopupDetails('续写内容', '续写内容');
      break;
    case '写作提示':
      showPopupDetails('写作提示', '写作提示');
      break;
    case '文章分析':
      showPopupDetails('文章分析', '文章分析');
      break;
    default:
      console.log('功能未定义');
  }
};

const showPopupDetails = (title, type) => {
  popupTitle.value = title;
  popupType.value = type;
  showPopup.value = true;
};

const closePopup = () => {
  showPopup.value = false;
  // 保持上次的 AI_model 值
  formData.value.AI_model = lastAIModel;
  formData.value = {
    text: '',
    length: 0,
    prompt: '',
    tone: '',
    style: '',
    content_type: '',
    type: '',
    AI_model:lastAIModel,
  };
};

const handleFormSubmit = () => {
  // 提交逻辑
  console.log('Form submitted:', formData.value);
  switch (popupType.value) {
    case '段落美化':
      beautifyParagraph();
      break;
    case '生成段落':
      generateParagraph();
      break;
    case '续写内容':
      continueContent();
      break;
    case '写作提示':
      provideWritingTips();
      break;
    case '文章分析':
      // 在选择文章分析时，将编辑器内容保存到 text
      formData.value.text = quillEditor.value.root.innerHTML;  // 保存编辑器内容到 formData.text
      analyzeArticle();
      break;
    default:
      console.log('未知功能');
  }
  closePopup();  // 提交后关闭弹窗
};


const beautifyParagraph = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('text', formData.value.text);  // 添加文本内容
    formDataToSend.append('length', formData.value.length.toString());  // 添加文本长度，确保是字符串类型
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型，确保是字符串类型

    // 请求后端段落美化接口
    const response = await request.post('/ez-note/AI/beauty', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      beautifiedText.value = response.translation;  // 存储后端返回的段落美化后的文本
      showBeautifiedContent.value = true;  // 显示美化后的内容
    } else {
      console.log('段落美化失败');
    }
  } catch (error) {
    console.error('段落美化请求失败:', error);
  }
};
// 替换选中的内容为段落美化后的文本
const replaceWithBeautifiedContent = () => {
  if (selectedRange.value && beautifiedText.value) {
    // 替换选中文本为用户编辑后的美化内容
    quillEditor.value.deleteText(selectedRange.value.index, selectedRange.value.length);
    quillEditor.value.insertText(selectedRange.value.index, beautifiedText.value);
    // 关闭弹窗
    showBeautifiedContent.value = false;
    selectedRange.value = null;
  }
};

// 取消操作
const cancelBeautify = () => {
  // 隐藏弹窗
  showBeautifiedContent.value = false;
  selectedRange.value = null;
};
// // 隐藏选中文本操作按钮
// const hideSelectionButtons = () => {
//   showSelectionButtons.value = false;
//   selectedRange.value = null;
// };

// 生成段落的函数
const generateParagraph = async () => {
      try {
        // 创建 FormData 对象
        const formDataToSend = new FormData();
        formDataToSend.append('prompt', formData.value.prompt);  // 添加生成段落的提示语
        formDataToSend.append('length', formData.value.length.toString());  // 添加段落的长度
        formDataToSend.append('tone', formData.value.tone);  // 添加写作的语气
        formDataToSend.append('style', formData.value.style);  // 添加写作风格
        formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

        // 请求后端生成段落接口
        const response = await request.post('/ez-note/AI/generate', formDataToSend, {
          headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
        });

        if (response.code === 0) {
          console.log('生成段落成功', response.data);
          const generatedContent = response.paragraph; // 假设后端返回的段落内容字段名为 `paragraph`

          // 设置弹窗编辑器的内容
          popInputContent.value = generatedContent;

          // 显示弹窗
          showParagraphPopup.value = true;
          openParagraphPopup();
        } else {
          console.log('生成段落失败');
        }
      } catch (error) {
        console.error('生成段落请求失败:', error);
      }
    };



const continueContent = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('text', formData.value.text);  // 添加当前文本内容
    formDataToSend.append('length', formData.value.length.toString());  // 添加续写内容的长度
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

    // 请求后端续写内容接口
    const response = await request.post('/ez-note/AI/continue', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      console.log('续写内容成功', response.data);
      const generatedContent = response.continuation; // 假设后端返回的段落内容字段名为 `paragraph`

      // 设置弹窗编辑器的内容
      popInputContent.value = generatedContent;

      // 显示弹窗
      showParagraphPopup.value = true;
      openParagraphPopup();
    } else {
      console.log('续写内容失败');
    }
  } catch (error) {
    console.error('续写内容请求失败:', error);
  }
};


const provideWritingTips = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('prompt', formData.value.prompt);  // 添加写作提示的提示词
    formDataToSend.append('content_type', formData.value.content_type);  // 添加内容类型
    formDataToSend.append('length', formData.value.length.toString());  // 添加提示内容的长度
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

    // 请求后端写作提示接口
    const response = await request.post('/ez-note/AI/inspiration', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      console.log('写作提示成功', response.data);
      const generatedContent = response.inspiration; // 假设后端返回的段落内容字段名为 `paragraph`

      // 设置弹窗编辑器的内容
      popInputContent.value = generatedContent;

      // 显示弹窗
      showParagraphPopup.value = true;
      openParagraphPopup();
    } else {
      console.log('写作提示失败');
    }
  } catch (error) {
    console.error('写作提示请求失败:', error);
  }
};


const analyzeArticle = async () => {
  try {
    // 创建 FormData 对象
    const formDataToSend = new FormData();
    formDataToSend.append('text', formData.value.text);  // 添加文章内容
    formDataToSend.append('type', formData.value.type);  // 添加文章类型
    formDataToSend.append('length', formData.value.length.toString());  // 添加分析的长度
    formDataToSend.append('AI_model', formData.value.AI_model.toString());  // 添加选择的 AI 模型

    // 请求后端文章分析接口
    const response = await request.post('/ez-note/AI/analysis', formDataToSend, {
      headers: { 'Content-Type': 'multipart/form-data' }  // 设置请求头为 multipart/form-data
    });

    if (response.code === 0) {
      console.log('文章分析成功', response.data);
      const generatedContent = response.analysis||response.correction||response.evaluation; 

      // 设置弹窗编辑器的内容
      popInputContent.value = generatedContent;

      // 显示弹窗
      showParagraphPopup.value = true;
      openParagraphPopup();
    } else {
      console.log('文章分析失败');
    }
  } catch (error) {
    console.error('文章分析请求失败:', error);
  }
};




const fetchDocumentContent = async () => {
  if (!docId) return;
  try {
    const response = await request.get(`/ez-note/note/query`, { params: { note_id: docId } });
    if (response.code === 0) {
      folderName.value = response.data.title;
      quillEditor.value.root.innerHTML = response.data.content;
    } else {
      alert('获取文档内容失败');
    }
  } catch (error) {
    console.error('获取文档内容失败:', error);
  }
};

const saveNote = async () => {
  try {
    const content = quillEditor.value.root.innerHTML;

    const formData = new FormData();
    formData.append(isNew ? 'title' : 'note_id', isNew ? folderName.value : docId);
    formData.append('content', content);
    formData.append('folder_id', folderId.toString());

    const endpoint = isNew ? `/ez-note/note/create` : `/ez-note/note/update/content`;
    const response = await request.post(endpoint, formData, { headers: { 'Content-Type': 'multipart/form-data' } });

    if (response.code === 0) {
      console.log(isNew ? '文档新建成功' : '文档更新成功');
    } else {
      console.error(isNew ? '新建失败' : '更新失败');
    }
  } catch (error) {
    console.error('保存文档内容失败:', error);
  }
};

const goBack = () => {
  // 返回到 Write.vue 页面
  router.push({ name: 'xiezuo' });
};

</script>

<style scoped>
.popup {
  position: absolute;  /* 使弹窗可以自由移动 */
  top: 50px;  /* 设置初始位置 */
  left: 100px;
  width: 300px;  /* 设置宽度 */
  padding: 20px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.popup-content {
  padding: 10px;
}

.popup-header {
  cursor: grab; /* 设置鼠标在标题栏时为抓取状态 */
}


.popcontent-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.popcontent-textarea {
  width: 100%;
  height: 100px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.popcontent-buttons {
  display: flex;
  justify-content: space-between;
}

.popcontent-buttons button {
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.popcontent-buttons button:first-child {
  background-color: #4caf50;
  color: white;
}

.popcontent-buttons button:last-child {
  background-color: #f44336;
  color: white;
}

.popupbeauty {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50%; /* 设置宽度为50% */
  background: white;
  border: 1px solid #ccc;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-width: 800px; /* 最大宽度限制 */
  cursor: move; /* 鼠标悬停时显示拖动光标 */
}

.editable-textarea {
  width: 100%;
  height: 150px;
  margin-bottom: 10px;
  font-size: 14px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.selection-buttons {
  position: absolute;
  top: 300px;
  left: 300px;
  z-index: 9999;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}

.selection-buttons button {
  margin-right: 10px;
  padding: 5px 10px;
}

/* 弹窗内容 */
.popup-content {
  margin-bottom: 20px;
}
.popup {
  position: fixed;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  width: 200px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  padding: 20px;
  z-index: 9999;
  display: block;  /* 弹窗显示时为 block */
}

/* 弹窗头部样式 */
.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.analysis-settings {
  margin-top: 20px;
}
.prompt-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border: 1px solid #ccc;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 600px; /* 设置弹窗宽度 */
  max-height: 90vh; /* 限制高度 */
  overflow-y: auto; /* 超出滚动 */
}

.large-textarea {
  width: 500px;
  height: 300px; /* 输入框高度 */
  margin-bottom: 20px;
  padding: 10px;
  font-size: 16px; /* 增大字体 */
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.ql-model, .ql-功能 {
  padding: 5px;
  margin-right: 10px;
  cursor: pointer;
  font-size: 18px;
}
.ql-toolbar select {
  margin-right: 10px;
  padding: 5px;
}

.note-detail-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-input {
  font-size: 24px;
  border: none;
  border-bottom: 1px solid #ddd;
  outline: none;
  padding: 5px;
  text-align: center;
}

.note-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#editor-container {
  width: 60%;
  margin: 0 auto;
  height: 800px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
}

/* Quill 工具栏样式调整 */
.ql-toolbar {
  margin: 0 auto;
  width: 70%;
  border-radius: 4px 4px 0 0;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.ql-container {
  height: calc(100% - 42px); /* 调整容器高度，避开工具栏 */
}

.actions {
  margin-top: 20px;
}

.actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
}

.actions button:hover {
  background-color: #45a049;
}

/* 返回按钮样式 */
.back-button {
  position: absolute;
  top: 120px;
  left: 20px;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #45a049;
}

</style>
